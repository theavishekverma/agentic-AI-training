from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from db_config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def initialize_database():
    from app.models import EmployeeModel  # noqa: F401 — registers model with Base
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== EMPLOYEE CRUD OPERATIONS ====================

def get_all_employees(db: Session):
    from app.models import EmployeeModel
    return db.query(EmployeeModel).all()


def get_employee_by_id(emp_id: int, db: Session):
    from app.models import EmployeeModel
    return db.query(EmployeeModel).filter(EmployeeModel.emp_id == emp_id).first()


def add_employee_to_db(name: str, salary: float, department: str, db: Session):
    from app.models import EmployeeModel
    employee = EmployeeModel(name=name, salary=salary, department=department)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee_in_db(emp_id: int, name: str, salary: float, department: str, db: Session):
    from app.models import EmployeeModel
    employee = db.query(EmployeeModel).filter(EmployeeModel.emp_id == emp_id).first()
    if not employee:
        return False
    employee.name = name
    employee.salary = salary
    employee.department = department
    db.commit()
    return True


def delete_employee_from_db(emp_id: int, db: Session):
    from app.models import EmployeeModel
    employee = db.query(EmployeeModel).filter(EmployeeModel.emp_id == emp_id).first()
    if not employee:
        return False
    db.delete(employee)
    db.commit()
    return True


def get_employees_by_department(department: str, db: Session):
    from app.models import EmployeeModel
    return (
        db.query(EmployeeModel)
        .filter(EmployeeModel.department == department)
        .order_by(EmployeeModel.name)
        .all()
    )


def get_employee_by_name(name: str, db: Session):
    from app.models import EmployeeModel
    return (
        db.query(EmployeeModel)
        .filter(EmployeeModel.name == name)
        .order_by(EmployeeModel.emp_id)
        .all()
    )
