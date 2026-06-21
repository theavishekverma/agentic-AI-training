import json
import os
import mysql.connector
from mysql.connector import Error

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse
from db_config import DB_CONFIG  # Import database configuration from separate file

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



# Initialize database and create table if it doesn't exist
def initialize_database():
    """Create database and employee table if they don't exist"""
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create employees table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary FLOAT NOT NULL,
            department VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except Error as e:
        print(f"Error initializing database: {e}")

# Initialize database on startup
initialize_database()


###############################
def get_db_connection():
    """Get a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_all_employees():
    """Fetch all employees from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees;")
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return employees
    except Error as e:
        print(f"Error fetching employees: {e}")
        return []


def add_employee_to_db(name: str, salary: float, department: str):
    """Add a new employee to database and return the employee data"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        insert_query = "INSERT INTO employees (name, salary, department) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, salary, department))
        conn.commit()
        emp_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        # Return the created employee
        return {
            "emp_id": emp_id,
            "name": name,
            "salary": salary,
            "department": department
        }
    except Error as e:
        print(f"Error adding employee: {e}")
        return None
###############################

Portfolio = []  # Simulated in-memory portfolio storage

@app.get("/employee")
async def get_employees():
    employees = get_all_employees()
    return JSONResponse(status_code=200, content={"employees": employees})

@app.get("/employee/{emp_id}")
async def get_employee(emp_id: int):
    employee = get_employee_by_id(emp_id)
    if employee:
        return JSONResponse(status_code=200, content={"employee": employee})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {emp_id} not found.")

@app.post("/employee", status_code=status.HTTP_201_CREATED)
async def add_employee(employee: EmployeeCreate):
    # Add employee to database
    employee_data = add_employee_to_db(employee.name, employee.salary, employee.department)
    
    if employee_data is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error adding employee to database")
    
    return JSONResponse(status_code=201, content={"message": "Employee added to portfolio!", "employee": employee_data})

# delete the employee by emp_id
@app.delete("/employee/{emp_id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_id: int):
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection error")
        
        cursor = conn.cursor()
        delete_query = "DELETE FROM employees WHERE emp_id = %s"
        cursor.execute(delete_query, (emp_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {emp_id} not found.")
        
        cursor.close()
        conn.close()
        
        return JSONResponse(status_code=200, content={"message": f"Employee with ID {emp_id} deleted successfully."})
    except Error as e:
        print(f"Error deleting employee: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting employee from database")
    
# get enploye by emp_id
def get_employee_by_id(emp_id: int):
    """Fetch an employee by emp_id from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
        employee = cursor.fetchone()
        cursor.close()
        conn.close()
        return employee
    except Error as e:
        print(f"Error fetching employee by ID: {e}")
        return None
    
# update employee details with employee id
@app.put("/employee/{emp_id}", status_code=status.HTTP_200_OK)
async def update_employee(emp_id: int, employee: EmployeeCreate):
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection error")
        
        cursor = conn.cursor()
        update_query = "UPDATE employees SET name = %s, salary = %s, department = %s WHERE emp_id = %s"
        cursor.execute(update_query, (employee.name, employee.salary, employee.department, emp_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {emp_id} not found.")
        
        cursor.close()
        conn.close()
        
        return JSONResponse(status_code=200, content={"message": f"Employee with ID {emp_id} updated successfully."})
    except Error as e:
        print(f"Error updating employee: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating employee in database")