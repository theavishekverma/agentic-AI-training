from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    name: str = Field(..., description="Name of the employee")
    salary: float = Field(..., gt=0, description="Salary associated with the employee")
    department: str = Field(..., description="Department associated with the employee")


class Employee(BaseModel):
    emp_id: int = Field(..., description="Employee ID associated with the employee (auto-generated)")
    name: str = Field(..., description="Name of the employee")
    salary: float = Field(..., gt=0, description="Salary associated with the employee")
    department: str = Field(..., description="Department associated with the employee")
