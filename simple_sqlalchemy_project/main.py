from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

app = FastAPI(title="Database Manager API")

# Connection string to your local MySQL server (without specifying a DB name)
# Format: mysql+pymysql://user:password@host:port
BASE_DATABASE_URL = "mysql+pymysql://root:Avishek%401312@localhost/:3306"
#mysql+pymysql://root:Avishek%401312@localhost/employee_management

# The name of the database we want to create/drop
TARGET_DB = "my_dynamic_db"

# Create a database engine that connects to the root server
engine = create_engine(BASE_DATABASE_URL, isolation_level="AUTOCOMMIT")

@app.post("/create-database")
def create_database():
    """Creates the target database if it does not exist."""
    try:
        with engine.connect() as conn:
            # text() ensures the raw SQL is safely executed by SQLAlchemy
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {TARGET_DB}"))
        return {"status": "success", "message": f"Database '{TARGET_DB}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/drop-database")
def drop_database():
    """Drops the target database if it exists."""
    try:
        with engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS {TARGET_DB}"))
        return {"status": "success", "message": f"Database '{TARGET_DB}' dropped successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))