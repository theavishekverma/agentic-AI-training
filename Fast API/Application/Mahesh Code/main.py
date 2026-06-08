from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import json
import os
# API Key for validation

app = FastAPI(title="Employee Management API",
              summary="Complete CRUD operations for Employee products using Depends for API Key validation",
              version="2.0.0")

class Employee(BaseModel):
    employee_id: int
    employee_name: str
    employee_email: str
    employee_age: int
    employee_department: str
    employee_salary: float

FILE_NAME = "EmployeeDetails.json"

# Valid API Keys (in production, store in database with encryption)
VALID_API_KEYS = ["your-secure-api-key-123", "test-key-456", "production-key-789"]

# Ensure the JSON file exists and is initialized with an empty list
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w') as f:
        json.dump([], f)

app.get("/")
def home():
        return {"message": "Welcome to the Employee Management API!"}

def read_employees() -> List[Employee]:
    """Read employee data from JSON file"""
    with open(FILE_NAME, 'r') as f:
        data = json.load(f)
    return [Employee(**item) for item in data]

def write_employees(employees: List[Employee]):
    """Write employee data to JSON file"""
    with open(FILE_NAME, 'w') as f:
        json.dump([employee.dict() for employee in employees], f, indent=4)