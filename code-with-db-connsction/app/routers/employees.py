from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import EmployeeCreate, Employee
from app.database import (
    get_all_employees,
    get_employee_by_id,
    add_employee_to_db,
    update_employee_in_db,
    delete_employee_from_db,
    get_employees_by_department,
    get_employee_by_name
)

router = APIRouter(
    prefix="/employee",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[Employee])
async def get_employees():
    """Get all employees"""
    employees = get_all_employees()
    return JSONResponse(status_code=200, content={"employees": employees})


@router.get("/department/{department}")
async def get_employees_by_dept(department: str):
    """Get all employees from a specific department"""
    employees = get_employees_by_department(department)
    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No employees found in department '{department}'."
        )
    return JSONResponse(status_code=200, content={"employees": employees})


@router.get("/{emp_id}", response_model=Employee)
async def get_employee(emp_id: int):
    """Get a specific employee by ID"""
    employee = get_employee_by_id(emp_id)
    if employee:
        return JSONResponse(status_code=200, content={"employee": employee})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee with ID {emp_id} not found."
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_employee(employee: EmployeeCreate):
    """Create a new employee"""
    employee_data = add_employee_to_db(
        employee.name,
        employee.salary,
        employee.department
    )
    
    if employee_data is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding employee to database"
        )
    
    return JSONResponse(
        status_code=201,
        content={"message": "Employee added to portfolio!", "employee": employee_data}
    )


@router.put("/{emp_id}", status_code=status.HTTP_200_OK)
async def update_employee(emp_id: int, employee: EmployeeCreate):
    """Update an employee by ID"""
    try:
        success = update_employee_in_db(
            emp_id,
            employee.name,
            employee.salary,
            employee.department
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {emp_id} not found."
            )
        
        return JSONResponse(
            status_code=200,
            content={"message": f"Employee with ID {emp_id} updated successfully."}
        )
    except Exception as e:
        print(f"Error updating employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating employee in database"
        )


@router.delete("/{emp_id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_id: int):
    """Delete an employee by ID"""
    try:
        success = delete_employee_from_db(emp_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {emp_id} not found."
            )
        
        return JSONResponse(
            status_code=200,
            content={"message": f"Employee with ID {emp_id} deleted successfully."}
        )
    except Exception as e:
        print(f"Error deleting employee: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting employee from database"
        )
    
@router.get("/name/{name}", response_model=list[Employee])
async def get_employee_by_name_route(name: str):
    """Get employees by name"""
    employees = get_employee_by_name(name)
    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No employees found with name '{name}'."
        )
    return JSONResponse(status_code=200, content={"employees": employees})