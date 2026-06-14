from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
import os
from datetime import datetime, timedelta
import jwt
from jwt import InvalidTokenError

app = FastAPI(
    title="Employee Management API",
    summary="This API is developed for employee information management system",
    version="1.0")

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Dummy user database
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


#create JWT Token
def create_access_token(data: dict):
    

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

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


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/employees")
def get_all_employees(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    """Get all employees"""
    employees_list = read_employees()
    return JSONResponse(status_code=200, content={"employees": employees_list, "total": len(employees_list)})