from django.shortcuts import render, redirect
from django.conf import settings
from functools import wraps
from . import api_service


# ── Auth helpers ────────────────────────────────────────────────────────────

def login_required(view_fn):
    """Redirect to /login/ if the session is not authenticated."""
    @wraps(view_fn)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("authenticated"):
            return redirect(f"/login/?next={request.path}")
        return view_fn(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.session.get("authenticated"):
        return redirect("/")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if (username == settings.PORTAL_USERNAME and
                password == settings.PORTAL_PASSWORD):
            request.session["authenticated"] = True
            request.session["username"] = username
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            error = "Invalid username or password."

    return render(request, "students/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("/login/")


# ── Protected views ─────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """Main dashboard — shows student list + stats."""
    search_name = request.GET.get("search_name", "").strip()
    search_grade = request.GET.get("search_grade", "").strip()

    error = None
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
        "students": students,
        "total_count": count,
        "error": error or count_err,
        "search_name": search_name,
        "search_grade": search_grade,
        "search_type": search_type,
    })


@login_required
def add_student(request):
    """Form to add a new student."""
    if request.method == "POST":
        student = {
            "id": request.POST.get("id", "").strip(),
            "name": request.POST.get("name", "").strip(),
            "grade": request.POST.get("grade", "").strip(),
            "email": request.POST.get("email", "").strip() or None,
            "address": request.POST.get("address", "").strip() or None,
        }
        if not student["id"] or not student["name"] or not student["grade"]:
            return render(request, "students/add_student.html", {
                "error": "ID, Name, and Grade are required.",
                "form_data": student,
            })

        result, err = api_service.add_student(student)
        if err:
            return render(request, "students/add_student.html", {
                "error": err,
                "form_data": student,
            })
        return redirect("/?success=added")

    return render(request, "students/add_student.html", {})


@login_required
def edit_student(request, student_id):
    """Full edit form for a student."""
    # Pre-populate from the list
    students, _ = api_service.get_all_students()
    student = next((s for s in students if str(s.get("id")) == str(student_id)), None)

    if request.method == "POST":
        updated = {
            "id": student_id,
            "name": request.POST.get("name", "").strip(),
            "grade": request.POST.get("grade", "").strip(),
            "email": request.POST.get("email", "").strip() or None,
            "address": request.POST.get("address", "").strip() or None,
        }
        result, err = api_service.update_student(student_id, updated)
        if err:
            return render(request, "students/edit_student.html", {
                "error": err,
                "student": updated,
            })
        return redirect("/?success=updated")

    return render(request, "students/edit_student.html", {"student": student})


@login_required
def delete_student(request, student_id):
    """Delete a student — POST only."""
    if request.method == "POST":
        result, err = api_service.delete_student(student_id)
        if err:
            return redirect(f"/?error={err}")
    return redirect("/?success=deleted")


@login_required
def quick_update(request, student_id, field):
    """Quick-update a single field (name / grade / email / address)."""
    FIELD_MAP = {
        "name": api_service.update_name,
        "grade": api_service.update_grade,
        "email": api_service.update_email,
        "address": api_service.update_address,
    }
    if request.method == "POST" and field in FIELD_MAP:
        value = request.POST.get("value", "").strip()
        fn = FIELD_MAP[field]
        result, err = fn(student_id, value)
        if err:
            return redirect(f"/?error={err}")
    return redirect("/?success=updated")

@login_required
def update_student_record(request, student_id):
    """Update all fields for a student."""
    if request.method == "POST":
        updated_data = {
            "name": request.POST.get("name", "").strip(),
            "grade": request.POST.get("grade", "").strip(),
            "email": request.POST.get("email", "").strip() or None,
            "address": request.POST.get("address", "").strip() or None,
        }
        result, err = api_service.update_student_record(student_id, updated_data)
        if err:
            return redirect(f"/?error={err}")
    return redirect("/?success=updated")
