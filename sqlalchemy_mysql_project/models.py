from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Employee(Base):
    """Employee model for MySQL database"""
    __tablename__ = "employees"
    
    emp_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    department = Column(String(100), ForeignKey('department.dept_name', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f"<Employee(id={self.emp_id}, name='{self.name}', salary={self.salary}, department='{self.department}')>"

class Department(Base):
    """Department model for MySQL database"""
    __tablename__ = "department"
    
    dept_name = Column(String(100), primary_key=True)
    
    def __repr__(self):
        return f"<Department(name='{self.dept_name}')>"
