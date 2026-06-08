from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from fastapi.security import APIKeyHeader
import json
from fastapi.responses import JSONResponse
import os

app = FastAPI(
    title="Laptop Bazar API with API Key Validation",
    description="CRUD API for laptop data with API Key authentication",
    version="1.0.0",
    contact={"name": "Avishek Verma", "email": "avishek.verma@example.com"}
)

# ============================================================================
# Data Model
# ============================================================================

class Laptop(BaseModel):
    laptop_id: int = Field(..., gt=0, description="Unique identifier for the laptop")
    laptop_name: str = Field(..., min_length=2, max_length=100, description="Name of the laptop")
    laptop_brand: str = Field(..., min_length=2, max_length=50, description="Brand of the laptop")
    laptop_price: float = Field(..., gt=0, description="Price of the laptop")


# ============================================================================
# Configuration
# ============================================================================

FILE_NAME = "laptopsDetails.json"

# Valid API Keys (in production, store in database with encryption)
VALID_API_KEYS = ["your-secure-api-key-123", "test-key-456", "production-key-789"]

# Ensure the JSON file exists and is initialized with an empty list
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w') as f:
        json.dump([], f)

# ============================================================================
# API Key Security
# ============================================================================

api_key_header = APIKeyHeader(name="X-API-Key", description="API Key required for authentication")

async def verify_api_key(x_api_key: str = Depends(api_key_header)):
    """Verify API Key from request headers"""
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return x_api_key

# ============================================================================
# File Operations
# ============================================================================

def read_laptops():
    """Read laptops from JSON file"""
    with open(FILE_NAME, 'r') as f:
        return json.load(f)

def write_laptops(laptops):
    """Write laptops to JSON file"""
    with open(FILE_NAME, 'w') as f:
        json.dump(laptops, f, indent=4)

# ============================================================================
# Endpoints - Public (No API Key Required)
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """API Documentation and Health Check"""
    return {
        "title": "Laptop Bazar API with API Key Validation",
        "version": "1.0.0",
        "message": "Welcome! All endpoints require API Key authentication",
        "api_key_location": "Header (X-API-Key)",
        "valid_api_keys_for_testing": VALID_API_KEYS,
        "endpoints": {
            "GET /laptops": "Get all laptops",
            "GET /laptops/{laptop_id}": "Get specific laptop",
            "GET /laptops_brand/{brand_name}": "Get laptops by brand",
            "POST /laptops": "Create new laptop",
            "DELETE /laptops/{laptop_id}": "Delete a laptop",
        },
        "usage_example": "curl -H 'X-API-Key: your-secure-api-key-123' http://localhost:8000/laptops",
        "docs": "Visit http://localhost:8000/docs for interactive Swagger UI"
    }

# ============================================================================
# Endpoints - Protected (API Key Required)
# ============================================================================

@app.get("/laptops", tags=["Laptops"])
async def get_laptops(api_key: str = Depends(verify_api_key)):
    """Get all laptops - Requires API Key in header (X-API-Key)"""
    laptops = read_laptops()
    return JSONResponse(status_code=200, content={"message": "Laptops retrieved successfully", "count": len(laptops), "laptops": laptops})

@app.get("/laptops/{laptop_id}", tags=["Laptops"])
async def get_laptop(laptop_id: int, api_key: str = Depends(verify_api_key)):
    """Get a specific laptop by ID - Requires API Key in header (X-API-Key)"""
    laptops = read_laptops()
    for laptop in laptops:
        if laptop["laptop_id"] == laptop_id:
            return JSONResponse(status_code=200, content={"message": "Laptop found", "laptop": laptop})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Laptop with ID {laptop_id} not found.")

@app.post("/laptops", status_code=status.HTTP_201_CREATED, tags=["Laptops"])
async def create_laptop(laptop: Laptop, api_key: str = Depends(verify_api_key)):
    """Create a new laptop - Requires API Key in header (X-API-Key)"""
    laptops = read_laptops()
    
    # Check for duplicate laptop_id
    if any(l["laptop_id"] == laptop.laptop_id for l in laptops):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Laptop with this ID already exists.")
    
    laptops.append(laptop.dict())
    write_laptops(laptops)
    
    return JSONResponse(status_code=201, content={"message": "Laptop created successfully!", "laptop": laptop.dict()})

@app.get("/laptops_brand/{brand_name}", tags=["Laptops"])
async def get_laptop_by_brand(brand_name: str, api_key: str = Depends(verify_api_key)):
    """Get all laptops by brand name - Requires API Key in header (X-API-Key)"""
    laptops = read_laptops()
    brand_laptops = [l for l in laptops if l["laptop_brand"].lower() == brand_name.lower()]
    if not brand_laptops:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No laptops found for brand {brand_name}.")
    return JSONResponse(status_code=200, content={"message": f"Laptops found for brand '{brand_name}'", "count": len(brand_laptops), "laptops": brand_laptops})

@app.delete("/laptops/{laptop_id}", status_code=status.HTTP_200_OK, tags=["Laptops"])
async def delete_laptop(laptop_id: int, api_key: str = Depends(verify_api_key)):
    """Delete a laptop by ID - Requires API Key in header (X-API-Key)"""
    laptops = read_laptops()
    updated_laptops = [l for l in laptops if l["laptop_id"] != laptop_id]
    
    if len(updated_laptops) == len(laptops):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Laptop with ID {laptop_id} not found.")
    
    write_laptops(updated_laptops)
    
    return JSONResponse(status_code=200, content={"message": f"Laptop with ID {laptop_id} deleted successfully!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

