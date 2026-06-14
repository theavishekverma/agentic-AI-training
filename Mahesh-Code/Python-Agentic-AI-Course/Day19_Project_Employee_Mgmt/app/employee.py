from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from services.employee_service import EmployeeService
from pydantic import BaseModel
from typing import Optional
from config.logger import get_logger

logger = get_logger('employee')

router = APIRouter(prefix="/employees", tags=["Employees"])

class EmployeeModel(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    department: str

@router.get("/")
def read_employees():
    logger.info("Fetching all employees")
    try:
        service = EmployeeService()
        employees = service.read_employees()
        logger.info(f"Successfully fetched {len(employees)} employees")
        return JSONResponse(content={"employees": employees}, status_code=200)
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        raise
    

@router.get("/{employee_id}")
def read_employee(employee_id: int):
    logger.info(f"Fetching employee with ID: {employee_id}")
    try:
        service = EmployeeService()
        employees = service.read_employees()
        employee = next((emp for emp in employees if emp["id"] == employee_id), None)
        if not employee:
            logger.warning(f"Employee with ID {employee_id} not found")
            raise HTTPException(status_code=404, detail="Employee not found")
        logger.info(f"Successfully fetched employee: {employee_id}")
        return JSONResponse(content={"employee": employee}, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching employee {employee_id}: {str(e)}")
        raise

@router.post("/")
def create_employee(employee: EmployeeModel):
    logger.info(f"Creating new employee: {employee.name}")
    try:
        service = EmployeeService()
        employees = service.read_employees()
        employee.id = max(emp["id"] for emp in employees) + 1 if employees else 1
        logger.debug(f"Assigned ID {employee.id} to new employee")
        employees.append(employee.model_dump())
        service.write_employees(employees)
        logger.info(f"Employee created successfully with ID: {employee.id}, Name: {employee.name}")
        return JSONResponse(content={"message": "Employee created successfully", "employee": employee.model_dump()}, status_code=201)
    except Exception as e:
        logger.error(f"Error creating employee: {str(e)}")
        raise

@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    logger.warning(f"Deleting employee with ID: {employee_id}")
    try:
        service = EmployeeService()
        employees = service.read_employees()
        employee = next((emp for emp in employees if emp["id"] == employee_id), None)
        if not employee:
            logger.warning(f"Employee with ID {employee_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Employee not found")
        employees.remove(employee)
        service.write_employees(employees)
        logger.info(f"Employee deleted successfully: ID {employee_id}")
        return JSONResponse(content={"message": "Employee deleted successfully"}, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting employee {employee_id}: {str(e)}")
        raise


@router.put("/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeModel):
    service = EmployeeService()
    employees = service.read_employees()
    existing_employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    existing_employee.update(employee.model_dump())
    service.write_employees(employees)
    return JSONResponse(content={"message": "Employee updated successfully", "employee": existing_employee}, status_code=200)

@router.get("/search/")
def search_employees(name: str = None, department: str = None):
    service = EmployeeService()
    employees = service.read_employees()
    if name:
        employees = [emp for emp in employees if name.lower() in emp["name"].lower()]
    if department:
        employees = [emp for emp in employees if department.lower() in emp["department"].lower()]
    return JSONResponse(content={"employees": employees}, status_code=200)
