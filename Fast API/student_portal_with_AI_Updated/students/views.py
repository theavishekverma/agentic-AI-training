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

    import json as _json
    return render(request, "students/dashboard.html", {
        "students":      students,
        "students_json": _json.dumps(students),
        "total_count":   count,
        "error":         error or count_err,
        "search_name":   search_name,
        "search_grade":  search_grade,
        "search_type":   search_type,
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


# ── AI views ─────────────────────────────────────────────────────────────────

import json
import urllib.request
import urllib.error
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def _call_claude(system_prompt, user_message, api_key, max_tokens=1024):
    """Call Claude claude-sonnet-4-6 via plain urllib (no extra dependencies)."""
    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data["content"][0]["text"]


@login_required
@require_POST
def ai_chat(request):
    """Answer a natural-language question about the current student data."""
    try:
        body        = json.loads(request.body)
        question    = body.get("question", "").strip()
        students    = body.get("students", [])
        api_key     = getattr(settings, "ANTHROPIC_API_KEY", "")

        if not question:
            return JsonResponse({"error": "No question provided."}, status=400)
        if not api_key or api_key == "your-anthropic-api-key-here":
            return JsonResponse({"error": "ANTHROPIC_API_KEY not set in settings.py."}, status=400)

        system = (
            "You are a helpful school data assistant. "
            "You are given a JSON list of student records and must answer questions about them clearly and concisely. "
            "Keep answers short (2-4 sentences max). Use bullet points only when listing multiple items. "
            "Never make up data that isn't in the records."
        )
        user_msg = f"Student data:\n{json.dumps(students, indent=2)}\n\nQuestion: {question}"
        answer = _call_claude(system, user_msg, api_key, max_tokens=512)
        return JsonResponse({"answer": answer})

    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return JsonResponse({"error": f"Anthropic API error: {body}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_POST
def ai_insights(request):
    """Generate a structured insight summary of all students."""
    try:
        body     = json.loads(request.body)
        students = body.get("students", [])
        api_key  = getattr(settings, "ANTHROPIC_API_KEY", "")

        if not api_key or api_key == "your-anthropic-api-key-here":
            return JsonResponse({"error": "ANTHROPIC_API_KEY not set in settings.py."}, status=400)

        if not students:
            return JsonResponse({"answer": "No student records found. Add some students first!"})

        system = (
            "You are a school data analyst. Analyse the student records and return a JSON object with exactly these keys:\n"
            "- summary: 1 sentence overview\n"
            "- grade_breakdown: short string e.g. 'A: 3 students, B: 2 students'\n"
            "- missing_data: list of strings describing missing fields (email / address), or empty list\n"
            "- top_insight: 1 interesting observation about the data\n"
            "- action_items: list of 2-3 short recommended actions for the admin\n"
            "Return ONLY valid JSON, no markdown, no explanation."
        )
        answer = _call_claude(system, json.dumps(students), api_key, max_tokens=600)
        # Parse and re-send as structured JSON
        parsed = json.loads(answer)
        return JsonResponse({"insights": parsed})

    except json.JSONDecodeError:
        return JsonResponse({"insights": {"summary": answer, "grade_breakdown": "", "missing_data": [], "top_insight": "", "action_items": []}})
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return JsonResponse({"error": f"Anthropic API error: {body}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_POST
def ai_student_report(request, student_id):
    """Generate a written profile report for a single student."""
    try:
        body     = json.loads(request.body)
        student  = body.get("student", {})
        api_key  = getattr(settings, "ANTHROPIC_API_KEY", "")

        if not api_key or api_key == "your-anthropic-api-key-here":
            return JsonResponse({"error": "ANTHROPIC_API_KEY not set in settings.py."}, status=400)

        system = (
            "You are a school administrator writing brief student profile notes. "
            "Given a student record, write a short 3-4 sentence professional profile note "
            "suitable for an internal school report. Mention their grade performance, "
            "note any missing information that should be collected, and end with a positive remark."
        )
        report = _call_claude(system, json.dumps(student), api_key, max_tokens=300)
        return JsonResponse({"report": report})

    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return JsonResponse({"error": f"Anthropic API error: {body}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ── Gemini AI views ───────────────────────────────────────────────────────────

def _call_gemini(prompt, api_key, max_tokens=1024):
    """
    Call Google Gemini via REST.
    Supports both key formats:
      - AIza...  → passed as ?key= query parameter
      - AQ...    → passed as Authorization: Bearer header
    """
    models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest"]

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.7,
        },
    }).encode()

    last_error = None
    for model in models_to_try:
        # Choose auth style based on key prefix
        if api_key.startswith("AQ"):
            url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{model}:generateContent"
            )
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
        else:
            # Legacy AIza key — query param
            url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{model}:generateContent?key={api_key}"
            )
            headers = {"Content-Type": "application/json"}

        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            try:
                err_json = json.loads(err_body)
                msg = err_json.get("error", {}).get("message", err_body)
                code = err_json.get("error", {}).get("code", e.code)
            except Exception:
                msg = err_body
                code = e.code
            # 401/403 = auth issue, no point trying other models
            if code in (401, 403):
                raise Exception(
                    f"Gemini authentication failed ({code}): {msg}. "
                    f"Make sure your GEMINI_API_KEY in settings.py is correct."
                )
            # 404 = model not available, try next
            if e.code == 404:
                last_error = msg
                continue
            raise Exception(f"Gemini API error: {msg}")

    raise Exception(f"All Gemini models unavailable. Last error: {last_error}")


@login_required
@require_POST
def gemini_chat(request):
    """Gemini-powered conversational assistant about student data."""
    try:
        body        = json.loads(request.body)
        question    = body.get("question", "").strip()
        students    = body.get("students", [])
        history     = body.get("history", [])
        api_key     = getattr(settings, "GEMINI_API_KEY", "")

        if not question:
            return JsonResponse({"error": "No question provided."}, status=400)
        if not api_key or api_key == "your-gemini-api-key-here" or len(api_key) < 10:
            return JsonResponse({"error": "GEMINI_API_KEY not set in settings.py."}, status=400)

        history_text = ""
        for turn in history[-6:]:
            role = "User" if turn["role"] == "user" else "Assistant"
            history_text += f"{role}: {turn['text']}\n"

        prompt = (
            "You are Gemini, an intelligent school data assistant. "
            "Answer questions about the student records below clearly and concisely. "
            "Use bullet points when listing items. Never fabricate data.\n\n"
            f"STUDENT DATA:\n{json.dumps(students, indent=2)}\n\n"
            + (f"CONVERSATION SO FAR:\n{history_text}\n" if history_text else "")
            + f"User: {question}\nAssistant:"
        )
        answer = _call_gemini(prompt, api_key, max_tokens=512)
        return JsonResponse({"answer": answer.strip()})

    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()
            err_json = json.loads(err_body)
            msg = err_json.get("error", {}).get("message", err_body)
        except Exception:
            msg = str(e)
        return JsonResponse({"error": f"Gemini API error: {msg}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_POST
def gemini_smart_summary(request):
    """Gemini generates a rich narrative summary + grade chart data."""
    try:
        body     = json.loads(request.body)
        students = body.get("students", [])
        api_key  = getattr(settings, "GEMINI_API_KEY", "")

        if not api_key or api_key == "your-gemini-api-key-here" or len(api_key) < 10:
            return JsonResponse({"error": "GEMINI_API_KEY not set in settings.py."}, status=400)
        if not students:
            return JsonResponse({"error": "No students to summarise."}, status=400)

        prompt = (
            "Analyse the following student records and return ONLY a JSON object with these keys:\n"
            "- narrative: a 2-3 sentence engaging summary of the cohort\n"
            "- grade_counts: object mapping each grade letter to count e.g. {\"A\": 3, \"B\": 2}\n"
            "- strengths: list of 2 positive observations\n"
            "- concerns: list of up to 2 data quality concerns (missing fields etc.), empty list if none\n"
            "- fun_fact: one interesting or quirky observation about the data\n"
            "Return ONLY valid JSON, no markdown fences, no extra text.\n\n"
            f"STUDENT DATA:\n{json.dumps(students)}"
        )
        raw = _call_gemini(prompt, api_key, max_tokens=700)
        clean = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        parsed = json.loads(clean)
        return JsonResponse({"summary": parsed})

    except json.JSONDecodeError:
        return JsonResponse({"summary": {"narrative": raw, "grade_counts": {}, "strengths": [], "concerns": [], "fun_fact": ""}})
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()
            err_json = json.loads(err_body)
            msg = err_json.get("error", {}).get("message", err_body)
        except Exception:
            msg = str(e)
        return JsonResponse({"error": f"Gemini API error: {msg}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_POST
def gemini_student_report(request, student_id):
    """Gemini generates a detailed profile + recommendations for a single student."""
    try:
        body     = json.loads(request.body)
        student  = body.get("student", {})
        api_key  = getattr(settings, "GEMINI_API_KEY", "")

        if not api_key or api_key == "your-gemini-api-key-here" or len(api_key) < 10:
            return JsonResponse({"error": "GEMINI_API_KEY not set in settings.py."}, status=400)

        prompt = (
            "You are a school counsellor writing a student profile report.\n"
            "Given this student record, write a structured report with:\n"
            "1. A 2-sentence academic profile based on their grade\n"
            "2. One personalised recommendation for improvement\n"
            "3. A note on any missing profile data that should be collected\n"
            "4. A positive closing remark\n"
            "Keep it professional, warm, and under 120 words.\n\n"
            f"Student record: {json.dumps(student)}"
        )
        report = _call_gemini(prompt, api_key, max_tokens=350)
        return JsonResponse({"report": report.strip()})

    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()
            err_json = json.loads(err_body)
            msg = err_json.get("error", {}).get("message", err_body)
        except Exception:
            msg = str(e)
        return JsonResponse({"error": f"Gemini API error: {msg}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
