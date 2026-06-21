import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG
from fastapi import HTTPException, status


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


def update_employee_in_db(emp_id: int, name: str, salary: float, department: str):
    """Update an employee in database"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        update_query = "UPDATE employees SET name = %s, salary = %s, department = %s WHERE emp_id = %s"
        cursor.execute(update_query, (name, salary, department, emp_id))
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0
    except Error as e:
        print(f"Error updating employee: {e}")
        return False


def delete_employee_from_db(emp_id: int):
    """Delete an employee from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        delete_query = "DELETE FROM employees WHERE emp_id = %s"
        cursor.execute(delete_query, (emp_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0
    except Error as e:
        print(f"Error deleting employee: {e}")
        return False


def get_employees_by_department(department: str):
    """Fetch all employees from a specific department"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM employees WHERE department = %s ORDER BY name"
        cursor.execute(query, (department,))
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return employees
    except Error as e:
        print(f"Error fetching employees by department: {e}")
        return []
    
def get_employee_by_name(name: str):
    """Fetch an employee by name from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM employees WHERE name = %s ORDER BY emp_id"
        cursor.execute(query, (name,))
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return employees
    except Error as e:
        print(f"Error fetching employee by name: {e}")
        return []
    
