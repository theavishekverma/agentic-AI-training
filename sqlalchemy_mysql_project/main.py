from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Employee, Department

# Create all tables in the database
def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully!")

# ==================== EMPLOYEE CRUD OPERATIONS ====================

def create_employee(name: str, salary: float, department: str) -> Employee:
    """Create a new employee"""
    db = SessionLocal()
    try:
        employee = Employee(name=name, salary=salary, department=department)
        db.add(employee)
        db.commit()
        db.refresh(employee)
        print(f"✓ Employee created: {employee}")
        return employee
    except Exception as e:
        db.rollback()
        print(f"✗ Error creating employee: {e}")
        return None
    finally:
        db.close()

def get_employee(emp_id: int) -> Employee:
    """Get an employee by ID"""
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
        if employee:
            print(f"✓ Employee found: {employee}")
        else:
            print(f"✗ Employee with id {emp_id} not found")
        return employee
    finally:
        db.close()

def get_all_employees() -> list:
    """Get all employees"""
    db = SessionLocal()
    try:
        employees = db.query(Employee).all()
        print(f"✓ Total employees: {len(employees)}")
        for emp in employees:
            print(f"  - {emp}")
        return employees
    finally:
        db.close()

def update_employee(emp_id: int, name: str = None, salary: float = None, department: str = None) -> Employee:
    """Update an employee"""
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
        if employee:
            if name:
                employee.name = name
            if salary is not None:
                employee.salary = salary
            if department:
                employee.department = department
            db.commit()
            db.refresh(employee)
            print(f"✓ Employee updated: {employee}")
            return employee
        else:
            print(f"✗ Employee with id {emp_id} not found")
            return None
    except Exception as e:
        db.rollback()
        print(f"✗ Error updating employee: {e}")
        return None
    finally:
        db.close()

def delete_employee(emp_id: int) -> bool:
    """Delete an employee"""
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
        if employee:
            db.delete(employee)
            db.commit()
            print(f"✓ Employee with id {emp_id} deleted")
            return True
        else:
            print(f"✗ Employee with id {emp_id} not found")
            return False
    except Exception as e:
        db.rollback()
        print(f"✗ Error deleting employee: {e}")
        return False
    finally:
        db.close()

# ==================== DEPARTMENT CRUD OPERATIONS ====================

def create_department(dept_name: str) -> Department:
    """Create a new department"""
    db = SessionLocal()
    try:
        department = Department(dept_name=dept_name)
        db.add(department)
        db.commit()
        db.refresh(department)
        print(f"✓ Department created: {department}")
        return department
    except Exception as e:
        db.rollback()
        print(f"✗ Error creating department: {e}")
        return None
    finally:
        db.close()

def get_department(dept_name: str) -> Department:
    """Get a department by name"""
    db = SessionLocal()
    try:
        department = db.query(Department).filter(Department.dept_name == dept_name).first()
        if department:
            print(f"✓ Department found: {department}")
        else:
            print(f"✗ Department '{dept_name}' not found")
        return department
    finally:
        db.close()

def get_all_departments() -> list:
    """Get all departments"""
    db = SessionLocal()
    try:
        departments = db.query(Department).all()
        print(f"✓ Total departments: {len(departments)}")
        for dept in departments:
            print(f"  - {dept}")
        return departments
    finally:
        db.close()

def delete_department(dept_name: str) -> bool:
    """Delete a department"""
    db = SessionLocal()
    try:
        department = db.query(Department).filter(Department.dept_name == dept_name).first()
        if department:
            db.delete(department)
            db.commit()
            print(f"✓ Department '{dept_name}' deleted")
            return True
        else:
            print(f"✗ Department '{dept_name}' not found")
            return False
    except Exception as e:
        db.rollback()
        print(f"✗ Error deleting department: {e}")
        return False
    finally:
        db.close()

# ==================== MAIN FUNCTION ====================

if __name__ == "__main__":
    # Initialize database
    print("\n" + "="*60)
    print("INITIALIZING DATABASE")
    print("="*60)
    init_db()
    
    print("\n" + "="*60)
    print("DEPARTMENT OPERATIONS")
    print("="*60)
    
    # Create departments
    print("\n--- Creating Departments ---")
    create_department("Engineering")
    create_department("Sales")
    create_department("HR")
    
    # Get all departments
    print("\n--- All Departments ---")
    get_all_departments()
    
    print("\n" + "="*60)
    print("EMPLOYEE OPERATIONS")
    print("="*60)
    
    # Create employees
    print("\n--- Creating Employees ---")
    create_employee("John Smith", 85000.0, "Engineering")
    create_employee("Sarah Johnson", 75000.0, "Sales")
    create_employee("Mike Chen", 95000.0, "Engineering")
    create_employee("Emily Davis", 70000.0, "HR")
    
    # Get all employees
    print("\n--- All Employees ---")
    get_all_employees()
    
    # Get specific employee
    print("\n--- Get Employee 1 ---")
    get_employee(1)
    
    # Update employee
    print("\n--- Update Employee 1 ---")
    update_employee(1, salary=90000.0)
    
    # Delete employee
    print("\n--- Delete Employee 4 ---")
    delete_employee(4)
    
    print("\n" + "="*60)
    print("FINAL STATE")
    print("="*60)
    
    print("\n--- Final Departments ---")
    get_all_departments()
    
    print("\n--- Final Employees ---")
    get_all_employees()
    
    print("\n✓ Demo completed successfully!")
