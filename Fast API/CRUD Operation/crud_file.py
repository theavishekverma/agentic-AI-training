# crud.py
import json
import os
from fastapi.responses import JSONResponse

FILE_PATH = "studentsdata.json"

def create_student_record(student_data: dict) -> dict:
    """
    Appends a new student record to the local JSON storage file.
    """
    # 1. Initialize an empty list if file doesn't exist or is empty
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r") as file:
            try:
                current_data = json.load(file)
            except json.JSONDecodeError:
                current_data = []
    else:
        current_data = []

    # 2. Add the new record
    current_data.append(student_data)

    # 3. Save back to the file
    with open(FILE_PATH, "w") as file:
        json.dump(current_data, file, indent=4)

    return JSONResponse({"status": "success", "data": student_data})

def read_student_records() -> list:
    """
    Reads all student records from the local JSON storage file.
    """
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        with open(FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []   

def update_student_record(student_id: str, updated_data: dict) -> dict:
    """
    Updates an existing student record identified by student_id.
    """
    records = read_student_records()
    for record in records:
        if record.get("id") == student_id:
            record.update(updated_data)
            with open(FILE_PATH, "w") as file:
                json.dump(records, file, indent=4)
            return JSONResponse({"status": "success", "data": record})
    return {"status": "error", "message": "Student not found"}

def delete_student_record(student_id: str) -> dict:
    """
    Deletes a student record identified by student_id.
    """
    records = read_student_records()
    updated_records = [record for record in records if record.get("id") != student_id]
    
    if len(updated_records) == len(records):
        return {"status": "error", "message": "Student not found"}
    
    with open(FILE_PATH, "w") as file:
        json.dump(updated_records, file, indent=4)
    
    return {"status": "success", "message": f"Student with id {student_id} deleted"}

def get_student_record(student_id: str) -> dict:
    """
    Retrieves a student record by student_id.
    """
    records = read_student_records()
    for record in records:
        if record.get("id") == student_id:
            return {"status": "success", "data": record}
    return JSONResponse({"status": "error", "message": "Student not found"})


def get_all_student_records() -> dict:
    """
    Retrieves all student records.
    """
    records = read_student_records()
    return {"status": "success", "data": records}


def clear_all_records() -> dict:
  
    # Clears all student records from the storage file.
  
    with open(FILE_PATH, "w") as file:
        json.dump([], file, indent=4)
    return {"status": "success", "message": "All student records cleared"}

# def count_student_records() -> dict:
#     #Counts the total number of student records.
#     records = read_student_records()
#     return {"status": "success", "count": len(records)}

def count_student_records():
    with open(FILE_PATH, 'r') as file:
        data = json.load(file)
    
    if isinstance(data, list):
        total_records = len(data)
        print(f"Total student records: {total_records}")
        return total_records
    else:
        print("Invalid data format")
        return 0

    

def find_students_by_name(name: str) -> dict:
    """
    Finds student records that match the given name.
    """
    records = read_student_records()
    matching_students = [record for record in records if record.get("name") == name]
    return {"status": "success", "data": matching_students}

def find_students_by_grade(grade: str) -> dict:
    """
    Finds student records that match the given grade.
    """
    records = read_student_records()
    matching_students = [record for record in records if record.get("grade") == grade]
    return {"status": "success", "data": matching_students}

def update_student_grade(student_id: str, new_grade: str) -> dict:
    """
    Updates the grade of a student identified by student_id.
    """
    records = read_student_records()
    for record in records:
        if record.get("id") == student_id:
            record["grade"] = new_grade
            with open(FILE_PATH, "w") as file:
                json.dump(records, file, indent=4)
            return {"status": "success", "data": record}
    return {"status": "error", "message": "Student not found"}

def update_student_email(student_id: str, new_email: str) -> dict:
    """
    Updates the email of a student identified by student_id.
    """
    records = read_student_records()
    for record in records:
        if record.get("id") == student_id:
            record["email"] = new_email
            with open(FILE_PATH, "w") as file:
                json.dump(records, file, indent=4)
            return {"status": "success", "data": record}
    return {"status": "error", "message": "Student not found"}

def update_student_address(student_id: str, new_address: str) -> dict:
    """
    Updates the address of a student identified by student_id.
    """
    records = read_student_records()
    for record in records:
        if record.get("id") == student_id:
            record["address"] = new_address
            with open(FILE_PATH, "w") as file:
                json.dump(records, file, indent=4)
            return {"status": "success", "data": record}
    return {"status": "error", "message": "Student not found"}

def update_student_name(student_id: str, new_name: str) -> dict:
    """
    Updates the name of a student identified by student_id.
    """
    records = read_student_records()
    for record in records:
        if record.get("id") == student_id:
            record["name"] = new_name
            with open(FILE_PATH, "w") as file:
                json.dump(records, file, indent=4)
            return {"status": "success", "data": record}
    return {"status": "error", "message": "Student not found"}