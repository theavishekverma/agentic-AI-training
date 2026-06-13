import re
import os
from django.shortcuts import render, redirect
from django.conf import settings
from functools import wraps
from . import api_service


# ── Auth helpers ─────────────────────────────────────────────────────────────

def login_required(view_fn):
    """Redirect to /login/ if the session is not authenticated."""
    @wraps(view_fn)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("authenticated"):
            return redirect(f"/login/?next={request.path}")
        return view_fn(request, *args, **kwargs)
    return wrapper


def _get_users():
    """Return the live PORTAL_USERS dict (always fresh from settings)."""
    return getattr(settings, "PORTAL_USERS", {})


def _persist_new_user(username, password):
    """
    Append the new user to settings.py on disk so it survives restarts,
    and also inject it into the live settings object for the current process.
    """
    # 1. Update the in-memory settings so this request sees it immediately
    if not hasattr(settings, "PORTAL_USERS"):
        settings.PORTAL_USERS = {}
    settings.PORTAL_USERS[username] = password

    # 2. Write to settings.py on disk
    settings_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "student_portal", "settings.py"
    )
    with open(settings_path, "r") as f:
        content = f.read()

    # Find the PORTAL_USERS dict closing brace and insert before it
    pattern = r'(PORTAL_USERS\s*=\s*\{[^}]*)(})'
    replacement = r'\g<1>    "' + username + r'": "' + password + r'",\n\g<2>'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(settings_path, "w") as f:
        f.write(new_content)


# ── Auth views ───────────────────────────────────────────────────────────────

def login_view(request):
    if request.session.get("authenticated"):
        return redirect("/")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        users = _get_users()
        if username in users and users[username] == password:
            request.session["authenticated"] = True
            request.session["username"] = username
            return redirect(request.GET.get("next", "/"))
        else:
            error = "Invalid username or password."

    return render(request, "students/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("/login/")


def register_view(request):
    """Register a new portal user and persist to settings.py."""
    if request.session.get("authenticated"):
        return redirect("/")

    error = None
    success = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm  = request.POST.get("confirm_password", "")

        users = _get_users()

        if not username or not password:
            error = "Username and password are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Passwords do not match."
        elif username in users:
            error = f'Username "{username}" is already taken.'
        else:
            _persist_new_user(username, password)
            success = username

        if success:
            return render(request, "students/register.html", {"success": success})

    return render(request, "students/register.html", {"error": error})


# ── Protected views ──────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """Main dashboard — shows student list + stats."""
    search_name  = request.GET.get("search_name", "").strip()
    search_grade = request.GET.get("search_grade", "").strip()

    error    = None
    students = []

    if search_name:
        students, error = api_service.search_by_name(search_name)
        search_type = f'name "{search_name}"'
    elif search_grade:
        students, error = api_service.search_by_grade(search_grade)
        search_type = f'grade "{search_grade}"'
    else:
        students, error = api_service.get_all_students()
        search_type = None

    count, count_err = api_service.get_student_count()

    return render(request, "students/dashboard.html", {
        "students":    students,
        "total_count": count,
        "error":       error or count_err,
        "search_name":  search_name,
        "search_grade": search_grade,
        "search_type":  search_type,
    })


@login_required
def add_student(request):
    if request.method == "POST":
        student = {
            "id":      request.POST.get("id", "").strip(),
            "name":    request.POST.get("name", "").strip(),
            "grade":   request.POST.get("grade", "").strip(),
            "email":   request.POST.get("email", "").strip() or None,
            "address": request.POST.get("address", "").strip() or None,
        }
        if not student["id"] or not student["name"] or not student["grade"]:
            return render(request, "students/add_student.html", {
                "error": "ID, Name, and Grade are required.", "form_data": student,
            })
        result, err = api_service.add_student(student)
        if err:
            return render(request, "students/add_student.html", {
                "error": err, "form_data": student,
            })
        return redirect("/?success=added")
    return render(request, "students/add_student.html", {})


@login_required
def edit_student(request, student_id):
    students, _ = api_service.get_all_students()
    student = next((s for s in students if str(s.get("id")) == str(student_id)), None)

    if request.method == "POST":
        updated = {
            "id":      student_id,
            "name":    request.POST.get("name", "").strip(),
            "grade":   request.POST.get("grade", "").strip(),
            "email":   request.POST.get("email", "").strip() or None,
            "address": request.POST.get("address", "").strip() or None,
        }
        result, err = api_service.update_student(student_id, updated)
        if err:
            return render(request, "students/edit_student.html", {
                "error": err, "student": updated,
            })
        return redirect("/?success=updated")

    return render(request, "students/edit_student.html", {"student": student})


@login_required
def delete_student(request, student_id):
    if request.method == "POST":
        result, err = api_service.delete_student(student_id)
        if err:
            return redirect(f"/?error={err}")
    return redirect("/?success=deleted")


@login_required
def quick_update(request, student_id, field):
    FIELD_MAP = {
        "name":    api_service.update_name,
        "grade":   api_service.update_grade,
        "email":   api_service.update_email,
        "address": api_service.update_address,
    }
    if request.method == "POST" and field in FIELD_MAP:
        value = request.POST.get("value", "").strip()
        result, err = FIELD_MAP[field](student_id, value)
        if err:
            return redirect(f"/?error={err}")
    return redirect("/?success=updated")
