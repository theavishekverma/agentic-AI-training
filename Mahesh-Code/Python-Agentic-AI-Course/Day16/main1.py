from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Student API", summary="This API developed for student management system", version="1.0")

class Student(BaseModel):
    student_id: int
    student_name: str
    student_course: str
    student_fees: float

FILE_NAME = "students.json"

# Create the json file if it doesn't exist   
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w') as f:
        json.dump([], f)



def read_students():
    with open(FILE_NAME, 'r') as f:
        return json.load(f)
    
def write_students(students):
    with open(FILE_NAME, 'w') as f:
        json.dump(students, f, indent=4)    


@app.get("/students")
def get_students():
    students = read_students()
    return JSONResponse(status_code=200, content={"students": students})

@app.post("/students")
def add_student(student: Student):
    students = read_students()
    students.append(student.dict())
    write_students(students)
    return JSONResponse(status_code=201, content={"message": "Student added successfully"})

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    students = read_students()
    for student in students:
        if student["student_id"] == student_id:
            student.update(updated_student.dict())
            write_students(students)
            return JSONResponse(status_code=200, content={"message": "Student updated successfully"})
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = read_students()
    for student in students:
        if student["student_id"] == student_id:
            students.remove(student)
            write_students(students)
            return JSONResponse(status_code=200, content={"message": "Student deleted successfully"})
    raise HTTPException(status_code=404, detail="Student not found")


@app.patch("/students/{student_id}")
def patch_student(student_id: int, student_fees: float):
    students = read_students()
    for student in students:
        if student["student_id"] == student_id:
            student["student_fees"] = student_fees
            write_students(students)
            return JSONResponse(status_code=200, content={"message": "Student updated successfully"})
    raise HTTPException(status_code=404, detail="Student not found")