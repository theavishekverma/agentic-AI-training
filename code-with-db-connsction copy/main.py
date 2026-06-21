from fastapi import FastAPI

from app.routers import employees
from app.database import initialize_database

app = FastAPI(
    title="Stock AI API",
    description="A simple FastAPI application to demonstrate Router with MySQL database connection for Employee management.",
    version="1.0.0",
    contact={"name": "Avishek Verma", "email": "avishek@example.com"},
)

# Initialize database on startup
initialize_database()

# Include the employees router
app.include_router(employees.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Employee Management API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)