from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas import EmployeeCreate, Employee
from app.database import (
    get_db,
    get_all_employees,
    get_employee_by_id,
    add_employee_to_db,
    update_employee_in_db,
    delete_employee_from_db,
    get_employees_by_department,
    get_employee_by_name,
)

router = APIRouter(
    prefix="/employee",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[Employee])
async def get_employees(db: Session = Depends(get_db)):
    employees = get_all_employees(db)
    return JSONResponse(
        status_code=200,
        content={"employees": [Employee.model_validate(e).model_dump() for e in employees]},
    )


@router.get("/department/{department}")
async def get_employees_by_dept(department: str, db: Session = Depends(get_db)):
    employees = get_employees_by_department(department, db)
    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No employees found in department '{department}'.",
        )
    return JSONResponse(
        status_code=200,
        content={"employees": [Employee.model_validate(e).model_dump() for e in employees]},
    )


@router.get("/name/{name}", response_model=list[Employee])
async def get_employee_by_name_route(name: str, db: Session = Depends(get_db)):
    employees = get_employee_by_name(name, db)
    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No employees found with name '{name}'.",
        )
    return JSONResponse(
        status_code=200,
        content={"employees": [Employee.model_validate(e).model_dump() for e in employees]},
    )


@router.get("/{emp_id}", response_model=Employee)
async def get_employee(emp_id: int, db: Session = Depends(get_db)):
    employee = get_employee_by_id(emp_id, db)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found.",
        )
    return JSONResponse(
        status_code=200,
        content={"employee": Employee.model_validate(employee).model_dump()},
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    employee_data = add_employee_to_db(employee.name, employee.salary, employee.department, db)
    return JSONResponse(
        status_code=201,
        content={
            "message": "Employee added to portfolio!",
            "employee": Employee.model_validate(employee_data).model_dump(),
        },
    )


@router.put("/{emp_id}", status_code=status.HTTP_200_OK)
async def update_employee(emp_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    success = update_employee_in_db(emp_id, employee.name, employee.salary, employee.department, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found.",
        )
    return JSONResponse(
        status_code=200,
        content={"message": f"Employee with ID {emp_id} updated successfully."},
    )


@router.delete("/{emp_id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    success = delete_employee_from_db(emp_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found.",
        )
    return JSONResponse(
        status_code=200,
        content={"message": f"Employee with ID {emp_id} deleted successfully."},
    )
