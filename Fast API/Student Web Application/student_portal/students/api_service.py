"""
api_service.py — All communication with the FastAPI backend lives here.
Django views call these functions; they never hit the FastAPI directly.
"""
import requests
from django.conf import settings

BASE_URL = settings.FASTAPI_BASE_URL
HEADERS = {
    "X-API-Key": settings.FASTAPI_API_KEY,
    "Content-Type": "application/json",
}


def _get(path, params=None):
    try:
        r = requests.get(f"{BASE_URL}{path}", headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server. Make sure it is running on port 8000."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return None, detail
    except Exception as e:
        return None, str(e)


def _post(path, data):
    try:
        r = requests.post(f"{BASE_URL}{path}", headers=HEADERS, json=data, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server. Make sure it is running on port 8000."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return None, detail
    except Exception as e:
        return None, str(e)


def _put(path, data=None, params=None):
    try:
        r = requests.put(f"{BASE_URL}{path}", headers=HEADERS, json=data, params=params, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server. Make sure it is running on port 8000."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return None, detail
    except Exception as e:
        return None, str(e)


def _delete(path):
    try:
        r = requests.delete(f"{BASE_URL}{path}", headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server. Make sure it is running on port 8000."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return None, detail
    except Exception as e:
        return None, str(e)


# ── Public API ─────────────────────────────────────────────────────────────

def get_all_students():
    data, err = _get("/students/")
    if err:
        return [], err
    return data.get("data", []), None


def get_student_count():
    data, err = _get("/students/count")
    if err:
        return 0, err
    # FastAPI returns the integer directly
    count = data if isinstance(data, int) else data.get("count", 0)
    return count, None


def add_student(student_dict):
    return _post("/students/", student_dict)


def update_student(student_id, student_dict):
    return _put(f"/students/{student_id}", data=student_dict)


def delete_student(student_id):
    return _delete(f"/students/{student_id}")


def update_name(student_id, new_name):
    return _put(f"/students/{student_id}/name", params={"new_name": new_name})


def update_grade(student_id, new_grade):
    return _put(f"/students/{student_id}/grade", params={"new_grade": new_grade})


def update_email(student_id, new_email):
    return _put(f"/students/{student_id}/email", params={"new_email": new_email})


def update_address(student_id, new_address):
    return _put(f"/students/{student_id}/address", params={"new_address": new_address})


def search_by_name(name):
    data, err = _get("/students/search/", params={"name": name})
    if err:
        return [], err
    return data.get("data", []), None


def search_by_grade(grade):
    data, err = _get("/students/search_by_grade/", params={"grade": grade})
    if err:
        return [], err
    return data.get("data", []), None

def update_student_record(student_id, updated_data):
    return _put(f"/students/update_student/{student_id}", data=updated_data)
