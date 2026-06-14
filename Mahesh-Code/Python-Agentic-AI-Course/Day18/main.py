from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json
import os

app = FastAPI(
    title="Employee Management API",
    summary="This API is developed for employee information management system",
    version="1.0")

security = HTTPBasic()



fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123"
    },
    "user1": {
        "username": "vishal",
        "password": "vishal123"
    }
}

class Employee(BaseModel):
    employee_id: int
    employee_name: str
    employee_email: str
    employee_age: int
    employee_department: str
    employee_salary: float

def read_employees():
    """Read all employees from the JSON file"""
    if not os.path.exists("employees.json"):
        return []
    with open("employees.json", 'r') as f:
        return json.load(f)    


def write_employees(employees):
    """Write employees to the JSON file"""
    with open("employees.json", 'w') as f:
        json.dump(employees, f, indent=4)


@app.get("/")
def home():
    """Welcome endpoint"""
    return {"message": "Welcome to Employee Management API"}


@app.get("/employees")
def get_all_employees(credentials: HTTPBasicCredentials = Depends(security)):
    for user in fake_users_db.values():
        if user["username"] == credentials.username and user["password"] == credentials.password:
            break
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    """Get all employees"""
    employees_list = read_employees()
    return JSONResponse(status_code=200, content={"employees": employees_list, "total": len(employees_list)})

@app.post("/employees")
def add_employee(employee: Employee):

    """Add a new employee"""
    employees_list = read_employees()
    for emp in employees_list:
        if emp["employee_id"] == employee.employee_id:
            raise HTTPException(status_code=400, detail="Employee with this ID already exists")
    employees_list.append(employee.dict())
    write_employees(employees_list)
    return JSONResponse(status_code=201, content={"message": "Employee added successfully", "employee": employee.dict()})