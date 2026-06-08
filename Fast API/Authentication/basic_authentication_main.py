from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI(title="Basic Authentication API",
              description="A Simple Basic Authentication API using FastAPI",
              version="1.0.0",
              contact={
                  "name": "Avishek Verma",
                  "email": "avishek@example.com"
              })

secret_key = HTTPBasic()

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin"
    },
    "user1": {
        "username": "vishal",
        "password": "vishal123"
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

    
@app.get("/", tags=["Welcome Message"])
def Print_Welcome_Message(credentials: HTTPBasicCredentials = Depends(secret_key)):
    for username, user in fake_users_db.items():
        print(f"Username: {user['username']}, Password: {user['password']}")
        if user["username"] == credentials.username and user["password"] == credentials.password:
            return JSONResponse(status_code=200, content={"message": "Welcome To Basic Authentication API!"})
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
@app.post("/employees/", tags=["Employees Details"])
def Create_New_Employee(employee: Employee, credentials: HTTPBasicCredentials = Depends(secret_key)):
    for username, user in fake_users_db.items():
        print(f"Username: {user['username']}, Password: {user['password']}")
        if user["username"] == credentials.username and user["password"] == credentials.password:
            with open(FILE_NAME, 'r') as f:
                employees = json.load(f)
                employees.append(employee.dict())
            
            with open(FILE_NAME, 'w') as f:
                write_data = json.dumps(employees, indent=4)
                f.write(write_data)
            
            #return JSONResponse(status_code=201, content={"message": "Employee created successfully!"})
            return JSONResponse(
                status_code=201, 
                content={"message": "Employee created successfully!", "employee": employee.dict()}, 
                headers={"Location": f"/employees/{employee.id}"}
                
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
@app.get("/employees/", response_model=List[Employee], tags=["Employees Details"])
def Display_All_Employees(credentials: HTTPBasicCredentials = Depends(secret_key)):
    for username, user in fake_users_db.items():
        print(f"Username: {user['username']}, Password: {user['password']}")
        if user["username"] == credentials.username and user["password"] == credentials.password:
            try:
                with open(FILE_NAME, 'r') as f:
                    employees = json.load(f)
            except FileNotFoundError:
                employees = []
            return employees
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/employees/{employee_id}", response_model=Employee, tags=["Employees Details"])
def Get_Employee_By_Id(employee_id: int, credentials: HTTPBasicCredentials = Depends(secret_key)):
    for username, user in fake_users_db.items():
        print(f"Username: {user['username']}, Password: {user['password']}")
        if user["username"] == credentials.username and user["password"] == credentials.password:
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

@app.patch("/employees/{employee_id}", tags=["Employees Details"])
def Update_Employee_By_Id(employee_id: int, employee: Employee, credentials: HTTPBasicCredentials = Depends(secret_key)):
    for username, user in fake_users_db.items():
        print(f"Username: {user['username']}, Password: {user['password']}")
        if user["username"] == credentials.username and user["password"] == credentials.password:
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
                        #json.dump(employees, f)
                    return JSONResponse(status_code=200, content={"message": "Employee updated successfully!"})
            raise HTTPException(status_code=404, detail="Employee not found")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

@app.delete("/employees/{employee_id}", tags=["Employees Details"])
def Delete_Employee_By_Id(employee_id: int, credentials: HTTPBasicCredentials = Depends(secret_key)):
    for username, user in fake_users_db.items():
        print(f"Username: {user['username']}, Password: {user['password']}")
        if user["username"] == credentials.username and user["password"] == credentials.password:
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
        