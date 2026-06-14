from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from services.payroll_service import PayrollService
from pydantic import BaseModel

router = APIRouter(prefix="/payroll", tags=["Payroll"])

class PayrollModel(BaseModel):
    id: int
    employee_id: int
    amount: float
    date: str

@router.get("/")
def read_payroll():
    service = PayrollService()
    payroll = service.read_payroll()
    return JSONResponse(content={"payroll": payroll}, status_code=200)
    

@router.get("/{employee_id}")
def read_employee_payroll(employee_id: int):
    service = PayrollService()
    payroll = service.read_payroll()
    employee_payroll = [record for record in payroll if record["employee_id"] == employee_id]
    if not employee_payroll:
        raise HTTPException(status_code=404, detail="Employee payroll not found")
    return JSONResponse(content={"payroll": employee_payroll}, status_code=200)

@router.post("/")
def create_payroll(payroll: PayrollModel):
    service = PayrollService()
    payroll_records = service.read_payroll()
    payroll.id = max(record["id"] for record in payroll_records) + 1 if payroll_records else 1
    payroll_records.append(payroll.model_dump())
    service.write_payroll(payroll_records)
    return JSONResponse(content={"message": "Payroll record created successfully", "payroll": payroll.model_dump()}, status_code=201)

@router.delete("/{employee_id}")
def delete_employee_payroll(employee_id: int):
    service = PayrollService()
    payroll_records = service.read_payroll()
    employee_payroll = [record for record in payroll_records if record["employee_id"] == employee_id]
    if not employee_payroll:
        raise HTTPException(status_code=404, detail="Employee payroll not found")
    for record in employee_payroll:
        payroll_records.remove(record)
    service.write_payroll(payroll_records)
    return JSONResponse(content={"message": "Employee payroll deleted successfully"}, status_code=200)


@router.put("/{employee_id}")
def update_employee_payroll(employee_id: int, payroll: PayrollModel):
    service = PayrollService()
    payroll_records = service.read_payroll()
    existing_record = next((record for record in payroll_records if record["id"] == payroll.id), None)
    if not existing_record:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    existing_record.update(payroll.model_dump())
    service.write_payroll(payroll_records)
    return JSONResponse(content={"message": "Payroll record updated successfully", "payroll": existing_record}, status_code=200)

