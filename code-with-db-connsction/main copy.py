import json
import os

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse

app = FastAPI(title="Stock AI API", 
              description="A simple FastAPI application to demonstrate Employee portfolio creation with update, delete and patch operations." , 
              version="1.0.0" , 
              contact={"name": "Avishek Verma", "email": "your.email@example.com"},
              )

class EmployeeCreate(BaseModel):
    name: str = Field(..., description="Name of the stock")
    salary: float = Field(..., gt=0, description="Salary associated with the stock")
    department: str = Field(..., description="Department associated with the stock")

class Employee(BaseModel):
    emp_id: int = Field(..., description="Employee ID associated with the stock (auto-generated)")
    name: str = Field(..., description="Name of the stock")
    salary: float = Field(..., gt=0, description="Salary associated with the stock")
    department: str = Field(..., description="Department associated with the stock")



FILE_NAME = "employeedetails.json"

# Valid API Keys (in production, store in database with encryption)
VALID_API_KEYS = ["your-secure-api-key-123", "test-key-456", "production-key-789"]

# Ensure the JSON file exists and is initialized with an empty list
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w') as f:
        json.dump([], f)


###############################
def read_employees():
    """Read employees from JSON file"""
    with open(FILE_NAME, 'r') as f:
        return json.load(f)

def write_employees(employees):
    """Write employees to JSON file"""
    with open(FILE_NAME, 'w') as f:
        json.dump(employees, f, indent=4)

def get_next_employee_id():
    """Generate the next employee ID by finding the max ID and incrementing"""
    employees = read_employees()
    if not employees:
        return 1
    max_id = max(emp.get('emp_id', 0) for emp in employees)
    return max_id + 1
###############################



Portfolio = []  # Simulated in-memory portfolio storage

@app.get("/employee")
async def get_employees():
    return JSONResponse(status_code=200, content={"employees": Portfolio})

@app.post("/employee", status_code=status.HTTP_201_CREATED)
async def add_employee(employee: EmployeeCreate):
    employees = read_employees()
    
    # Auto-generate emp_id
    emp_id = get_next_employee_id()
    
    # Create employee data with auto-generated ID
    employee_data = {
        "emp_id": emp_id,
        **employee.dict()
    }
    
    employees.append(employee_data)
    write_employees(employees)
    return JSONResponse(status_code=201, content={"message": "Employee added to portfolio!", "employee": employee_data})

