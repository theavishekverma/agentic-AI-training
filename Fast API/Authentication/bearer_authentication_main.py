from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials, HTTPBearer
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI(title="Bearer Token Authentication API",
              description="A Bearer Token Authentication API using FastAPI",
              version="1.0.0",
              contact={
                  "name": "Avishek Verma",
                  "email": "avishek@example.com"
              })

secret_key = HTTPBearer()

fake_users_db = {
    "admin": {
        "token": "admin-token"
    }

}

FILE_NAME = "Employee.json"


# Ensure the JSON file exists and is initialized with an empty list
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w') as f:
        json.dump([], f)

class Employee(BaseModel):
    id: int
    name: str
    age: int
    department: str
    salary: float 

    
@app.get("/", tags=["Authentication"])
def Print_Welcome_Message(credentials: HTTPAuthorizationCredentials = Depends(secret_key)):
            return JSONResponse(status_code=200, content={"message": "Welcome To Bearer Token Authentication API!"})
        
       
@app.get("/employees/", response_model=List[Employee], tags=["Employees"])
def Display_All_Employees(credentials: HTTPAuthorizationCredentials = Depends(secret_key)):
    print(f"Received token: {credentials.credentials}")
    for username in fake_users_db.values():
        if username["token"] == credentials.credentials:
            try:
                with open(FILE_NAME, 'r') as f:
                    employees = json.load(f)
            except FileNotFoundError:
                employees = []
            return employees
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
@app.post("/employees/", tags=["Employees"])
def Create_New_Employee(employee: Employee, credentials: HTTPAuthorizationCredentials = Depends(secret_key)):
    print(f"Received token: {credentials.credentials}")
    for username in fake_users_db.values():
        if username["token"] == credentials.credentials:
            with open(FILE_NAME, 'r') as f:
                employees = json.load(f)
                employees.append(employee.dict())   
                with open(FILE_NAME, 'w') as f:
                    write_data = json.dumps(employees, indent=4)
                    f.write(write_data)
            return JSONResponse(
                status_code=201,    
                content={"message": "Employee created successfully!", "employee": employee.dict()},
                headers={"Location": f"/employees/{employee.id}"}
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")  

@app.put("/employees/{employee_id}", tags=["Employees"])
def Update_Employee(employee_id: int, employee: Employee, credentials: HTTPAuthorizationCredentials = Depends(secret_key)):
    print(f"Received token: {credentials.credentials}")
    for username in fake_users_db.values():
        if username["token"] == credentials.credentials:
            try:
                with open(FILE_NAME, 'r') as f:
                    employees = json.load(f)
            except FileNotFoundError:
                employees = []
            
            for emp in employees:
                if emp["id"] == employee_id:
                    emp.update(employee.dict())
                    with open(FILE_NAME, 'w') as f:
                        write_data = json.dumps(employees, indent=4)
                        f.write(write_data)
                    return JSONResponse(status_code=200, content={"message": "Employee updated successfully!"})
            raise HTTPException(status_code=404, detail="Employee not found")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials") 
        
@app.delete("/employees/{employee_id}", tags=["Employees"])
def Delete_Employee(employee_id: int, credentials: HTTPAuthorizationCredentials = Depends(secret_key)):
    print(f"Received token: {credentials.credentials}")
    for username in fake_users_db.values():
        if username["token"] == credentials.credentials:
            try:
                with open(FILE_NAME, 'r') as f:
                    employees = json.load(f)
            except FileNotFoundError:
                employees = []
            
            for emp in employees:
                if emp["id"] == employee_id:
                    employees.remove(emp)
                    with open(FILE_NAME, 'w') as f:
                        write_data = json.dumps(employees, indent=4)
                        f.write(write_data)
                    return JSONResponse(status_code=200, content={"message": "Employee deleted successfully!"})
            raise HTTPException(status_code=404, detail="Employee not found")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials") 
        
@app.get("/employees/{employee_id}", response_model=Employee, tags=["Employees"])
def Get_Employee_By_Id(employee_id: int, credentials: HTTPAuthorizationCredentials = Depends(secret_key)):
    print(f"Received token: {credentials.credentials}")
    for username in fake_users_db.values():
        if username["token"] == credentials.credentials:
            try:
                with open(FILE_NAME, 'r') as f:
                    employees = json.load(f)
            except FileNotFoundError:
                employees = []
            for emp in employees:
                if emp["id"] == employee_id:
                    return emp
            raise HTTPException(status_code=404, detail="Employee not found")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
