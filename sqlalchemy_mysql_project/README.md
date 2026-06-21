# SQLAlchemy MySQL Project

A simple project demonstrating SQLAlchemy ORM with MySQL database connection.

## Project Structure

```
sqlalchemy_mysql_project/
├── database.py      # Database configuration and session setup
├── models.py        # Database models (Employee, Department)
├── main.py          # CRUD operations and demo
├── requirements.txt # Project dependencies
└── README.md        # This file
```

## Features

- **MySQL Database**: Connects to MySQL using PyMySQL
- **SQLAlchemy ORM**: Object-Relational Mapping for database operations
- **Models**: Two sample models (Employee and Department)
- **CRUD Operations**: Create, Read, Update, Delete functionality
- **Session Management**: Proper database session handling
- **Connection Pooling**: Auto-recycling connections and pre-ping checks

## Setup Instructions

1. **Prerequisites**:
   - MySQL server running on localhost
   - Database `employee_management` created
   - MySQL user: `root` with password: `Avishek@1312`

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the demo**:
   ```bash
   python main.py
   ```

## Database Configuration

- **Database URL**: `mysql+pymysql://root:Avishek%401312@localhost/employee_management`
- **Note**: The `@` in password is URL-encoded as `%40`

## Models

### Employee Model
- `emp_id`: Primary key (auto-increment)
- `name`: Employee name (required)
- `salary`: Employee salary (required)
- `department`: Department name (required)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Department Model
- `dept_id`: Primary key (auto-increment)
- `dept_name`: Department name (unique, required)
- `location`: Department location (required)
- `created_at`: Timestamp of creation

## CRUD Operations

### Employee Operations
- `create_employee(name, salary, department)`: Create a new employee
- `get_employee(emp_id)`: Get employee by ID
- `get_all_employees()`: Get all employees
- `update_employee(emp_id, name, salary, department)`: Update employee
- `delete_employee(emp_id)`: Delete employee

### Department Operations
- `create_department(dept_name, location)`: Create a new department
- `get_department(dept_id)`: Get department by ID
- `get_all_departments()`: Get all departments
- `update_department(dept_id, dept_name, location)`: Update department
- `delete_department(dept_id)`: Delete department

## Example Usage

```python
from main import create_employee, get_all_employees, create_department, init_db

# Initialize database
init_db()

# Create a department
create_department("Engineering", "New York")

# Create an employee
create_employee("John Doe", 85000.0, "Engineering")

# Get all employees
get_all_employees()

# Update employee salary
update_employee(1, salary=95000.0)
```

## Database Initialization

When you run `main.py`, it automatically:
1. Creates all tables if they don't exist
2. Inserts sample data
3. Demonstrates all CRUD operations

## Notes

- SQL queries are printed by default (set `echo=False` in `database.py` to disable)
- Connections are tested before use (`pool_pre_ping=True`)
- Connections are recycled after 1 hour (`pool_recycle=3600`)
- Each operation opens and closes its own session
- Includes error handling with proper rollback on failures

## Extending the Project

To add more models:
1. Define the model in `models.py` (inheriting from `Base`)
2. Create CRUD functions in `main.py`
3. Run `init_db()` to create the new tables
