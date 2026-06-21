from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# MySQL database URL
DATABASE_URL = "mysql+pymysql://root:Avishek%401312@localhost/employee_management"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Print SQL queries
    pool_pre_ping=True,  # Test connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
