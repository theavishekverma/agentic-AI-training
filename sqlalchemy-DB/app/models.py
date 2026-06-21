from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class EmployeeModel(Base):
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    salary = Column(Float, nullable=False)
    department = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Employee(emp_id={self.emp_id}, name='{self.name}', salary={self.salary}, department='{self.department}')>"
