import json
import os

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse

app = FastAPI(title="Stock AI API", 
              description="A simple FastAPI application to demonstrate Stock portfolio creation with update, delete and patch operations." , 
              version="1.0.0" , 
              contact={"name": "Avishek Verma", "email": "your.email@example.com"},
              )

class Student(BaseModel):
    student_id: int = Field(..., gt=0, description="Unique identifier for the student")
    student_name: str = Field(..., min_length=2, max_length=100, description="Name of the student")
    student_age: int = Field(..., ge=0, description="Age of the student")
    student_email: str = Field(..., format="email", description="Email address of the student")

FILE_NAME = "students.json"

# Ensure the JSON file exists and is initialized with an empty list
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
async def get_students():
    students = read_students()
    return JSONResponse(status_code=200, content={"students": students})

@app.get("/students/{student_id}")
async def get_student(student_id: int): 
    students = read_students()
    for student in students:
        if student["student_id"] == student_id:
            return JSONResponse(status_code=200, content={"student": student})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found.")

@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):
    students = read_students()
    
    # Check for duplicate student_id
    if any(s["student_id"] == student.student_id for s in students):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student with this ID already exists.")
    
    students.append(student.dict())
    write_students(students)
    
    return JSONResponse(status_code=201, content={"message": "Student created successfully!", "student": student.dict()})

@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int):
    students = read_students()
    updated_students = [s for s in students if s["student_id"] != student_id]
    
    if len(updated_students) == len(students):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found.")
    
    write_students(updated_students)
    return JSONResponse(status_code=200, content={"message": f"Student with ID {student_id} deleted successfully!"})

@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
async def update_student(student_id: int, updated_student: Student):
    students = read_students()
    for i, s in enumerate(students):
        if s["student_id"] == student_id:
            students[i] = updated_student.dict()
            write_students(students)
            return JSONResponse(status_code=200, content={"message": f"Student with ID {student_id} updated successfully!", "student": updated_student.dict()})
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found.")

@app.patch("/students/{student_id}", status_code=status.HTTP_200_OK)
async def patch_student(student_id: int, student_email: str):
    students = read_students()
    for i, s in enumerate(students):
        if s["student_id"] == student_id:
            students[i]["student_email"] = student_email
            write_students(students)
            return JSONResponse(status_code=200, content={"message": f"Student with ID {student_id} email updated successfully!", "student": students[i]})
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found.")