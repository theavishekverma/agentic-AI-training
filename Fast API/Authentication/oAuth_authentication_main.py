from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import json
import os
import jwt
from datetime import datetime, timedelta
from jwt import InvalidTokenError, DecodeError

app = FastAPI(title="oAuth Authentication API",
              description="A oAuth Authentication API using FastAPI",
              version="1.0.0",
              contact={
                  "name": "Avishek Verma",
                  "email": "avishek@example.com"
              })


secret_key = "my_secret_token_key"
Algorithm = "HS256"
Access_Token_Expire_Minutes = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Using HTTPBearer for token authentication


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

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin"
    }
}

#Create JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Access_Token_Expire_Minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=Algorithm)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[Algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except (InvalidTokenError, DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token")

def read_employees():
    try:
        with open(FILE_NAME, 'r') as f:
            employees = json.load(f)
    except FileNotFoundError:
        employees = []
    return employees

def write_employees(employees):
    with open(FILE_NAME, 'w') as f:
        json.dump(employees, f, indent=4) 


@app.post("/login", tags=["Generate Access Token"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"} 

    
@app.get("/", tags=["Welcome Message"])
def Print_Welcome_Message(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
            return JSONResponse(status_code=200, content={"message": "Welcome To oAuth Authentication API!"})

        
@app.get("/employees/", response_model=List[Employee], tags=["Employees Details"])
def Display_All_Employees(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username:
        employees = read_employees()
        return employees
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.get("/employees/{employee_id}", response_model=Employee, tags=["Employees Details"])
def Get_Employee_By_Id(employee_id: int, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username:
        employees = read_employees()
        for emp in employees:
            if emp["id"] == employee_id:
                return emp
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

@app.post("/employees/", tags=["Employees Details"])
def Create_New_Employee(employee: Employee, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username:
        employees = read_employees()
        employees.append(employee.dict())
        write_employees(employees)
        return JSONResponse(
            status_code=201,    
            content={"message": "Employee created successfully!", "employee": employee.dict()},
            headers={"Location": f"/employees/{employee.id}"}
        )
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.put("/employees/{employee_id}", tags=["Employees Details"])
def Update_Employee(employee_id: int, employee: Employee, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username:
        employees = read_employees()
        for emp in employees:
            if emp["id"] == employee_id:
                emp.update(employee.dict())
                write_employees(employees)
                return JSONResponse(status_code=200, content={"message": "Employee updated successfully!"})
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.delete("/employees/{employee_id}", tags=["Employees Details"])
def Delete_Employee(employee_id: int, token: str = Depends(oauth2_scheme)): 
    username = verify_token(token)
    if username:
        employees = read_employees()
        for emp in employees:
            if emp["id"] == employee_id:
                employees.remove(emp)
                write_employees(employees)
                return JSONResponse(status_code=200, content={"message": "Employee deleted successfully!"})
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")  
    
