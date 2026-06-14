from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from services.department_service import DepartmentService
from pydantic import BaseModel

router = APIRouter(prefix="/departments", tags=["Departments"])

class DepartmentModel(BaseModel):
    id: int
    name: str

@router.get("/")
def read_departments():
    service = DepartmentService()
    departments = service.read_departments()
    return JSONResponse(content={"departments": departments}, status_code=200)
    

@router.get("/{department_id}")
def read_department(department_id: int):
    service = DepartmentService()
    departments = service.read_departments()
    department = next((dept for dept in departments if dept["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return JSONResponse(content={"department": department}, status_code=200)

@router.post("/")
def create_department(department: DepartmentModel):
    service = DepartmentService()
    departments = service.read_departments()
    department.id = max(dept["id"] for dept in departments) + 1 if departments else 1
    departments.append(department.model_dump())
    service.write_departments(departments)
    return JSONResponse(content={"message": "Department created successfully", "department": department.model_dump()}, status_code=201)

@router.delete("/{department_id}")
def delete_department(department_id: int):
    service = DepartmentService()
    departments = service.read_departments()
    department = next((dept for dept in departments if dept["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    departments.remove(department)
    service.write_departments(departments)
    return JSONResponse(content={"message": "Department deleted successfully"}, status_code=200)


@router.put("/{department_id}")
def update_department(department_id: int, department: DepartmentModel):
    service = DepartmentService()
    departments = service.read_departments()
    existing_department = next((dept for dept in departments if dept["id"] == department_id), None)
    if not existing_department:
        raise HTTPException(status_code=404, detail="Department not found")
    existing_department.update(department.model_dump())
    service.write_departments(departments)
    return JSONResponse(content={"message": "Department updated successfully", "department": existing_department}, status_code=200)

