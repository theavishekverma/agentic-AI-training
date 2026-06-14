from fastapi import FastAPI
from app import employee,department,payroll
from fastapi.middleware.cors import CORSMiddleware
from config.logger import get_logger
import time
from fastapi.requests import Request

# Initialize logger
logger = get_logger('main')

app = FastAPI(title="Employee Management API", summary="This API is developed for employee information management system", version="1.0")

logger.info("FastAPI application initialized")

origins = [    
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logger.info(f"CORS enabled for origins: {origins}")

# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"-> {request.method} {request.url.path} from {request.client.host}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"<- {request.method} {request.url.path} | Status: {response.status_code} | Duration: {process_time:.3f}s")
    
    return response

app.include_router(employee.router)
app.include_router(department.router)
app.include_router(payroll.router)

logger.info("All routers included")

@app.get("/")
def read_root():
    logger.debug("Root endpoint accessed")
    return {"message": "Welcome to the Employee Management System!"}