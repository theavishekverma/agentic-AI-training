# main.py
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from auth import verify_api_key
from pydantic import BaseModel, Field
from typing import Optional

# ─── IMPORT YOUR CRUD FUNCTION HERE ───
# "from crud" refers to crud.py, "import create_student_record" is the specific function
from crud_file import create_student_record
from crud_file import read_student_records
from crud_file import update_student_record
from crud_file import delete_student_record
from crud_file import update_student_name
from crud_file import update_student_grade
from crud_file import update_student_email
from crud_file import update_student_address
from crud_file import find_students_by_name
from crud_file import find_students_by_grade
from crud_file import count_student_records    
from crud_file import clear_all_records


app = FastAPI(
    title="Student CRUD API with API Key Validation",
    description="Complete CRUD operations for Student Data using Depends for API Key validation",
    version="2.0.0",
    dependencies=[Depends(verify_api_key)]  # Global dependency for API Key validation
)


# Define the Pydantic schema for validation
class StudentSchema(BaseModel):
    id: str
    name: str
    grade: str
    email: Optional[str] = Field(None, description="Student's email address")
    address: Optional[str] = Field(None, description="Student's home address")

@app.post("/students/", status_code=201)
def add_new_student(student: StudentSchema):
    try:
        # Convert Pydantic model to a standard dictionary
        student_dict = student.model_dump()
        
        # ─── CALL THE CRUD FUNCTION HERE ───
        result = create_student_record(student_dict)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.get("/students/", status_code=200)
def get_all_students():
    try:
        # ─── CALL THE CRUD FUNCTION TO READ STUDENTS HERE ───
        from crud_file import read_student_records
        students = read_student_records()
        
        return {"status": "success", "data": students}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.put("/students/{student_id}", status_code=200)
def update_student(student_id: str, student: StudentSchema):
    try:
        student_dict = student.model_dump()
        
        # ─── CALL THE CRUD FUNCTION TO UPDATE STUDENT HERE ───
        from crud_file import update_student_record
        result = update_student_record(student_id, student_dict)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@app.delete("/students/{student_id}", status_code=200)
def delete_student(student_id: str):
    try:
        # ─── CALL THE CRUD FUNCTION TO DELETE STUDENT HERE ───
        from crud_file import delete_student_record
        result = delete_student_record(student_id)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.put("/students/{student_id}/name", status_code=200)
def update_student_name_endpoint(student_id: str, new_name: str):
    try:
        from crud_file import update_student_name
        result = update_student_name(student_id, new_name)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        

@app.put("/students/{student_id}/grade", status_code=200)
def update_student_grade_endpoint(student_id: str, new_grade: str):
    try:
        from crud_file import update_student_grade
        result = update_student_grade(student_id, new_grade)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.put("/students/{student_id}/email", status_code=200)
def update_student_email_endpoint(student_id: str, new_email: str):
    try:
        from crud_file import update_student_email
        result = update_student_email(student_id, new_email)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.put("/students/{student_id}/address", status_code=200)
def update_student_address_endpoint(student_id: str, new_address: str):
    try:
        from crud_file import update_student_address
        result = update_student_address(student_id, new_address)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.get("/students/search/", status_code=200)
def find_students_by_name(name: str):
    try:
        from crud_file import find_students_by_name
        result = find_students_by_name(name)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.get("/students/search_by_grade/", status_code=200)
def find_students_by_grade(grade: str):
    try:
        from crud_file import find_students_by_grade
        result = find_students_by_grade(grade)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.get("/students/count", status_code=200)
def count_students():
    try:
        from crud_file import count_students
        result = count_students()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

    
