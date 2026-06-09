import json
import os
from fastapi import FastAPI, HTTPException, Depends, Header
from auth import verify_api_key
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Laptop Product CRUD API with API Key Validation",
    description="Complete CRUD operations for Laptop products using Depends for API Key validation",
    version="2.0.0",
    dependenies=[Depends(verify_api_key)]  # Global dependency for API Key validation
)

JSON_FILE = "laptops_products.json"

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════

VALID_API_KEYS = ["laptop-key-123", "admin-key-456", "test-key-789"]

# ══════════════════════════════════════════════════════════════════════════
# JSON FILE HELPERS
# ══════════════════════════════════════════════════════════════════════════

def read_json() -> dict:
    """Read JSON file or initialize with empty structure"""
    if not os.path.exists(JSON_FILE):
        write_json({"next_id": 1, "laptops": {}})
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def write_json(data: dict):
    """Write data to JSON file"""
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ══════════════════════════════════════════════════════════════════════════

class LaptopCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Laptop name")
    brand: str = Field(..., min_length=2, max_length=50, description="Brand name")
    price: float = Field(..., gt=0, description="Price in USD")
    processor: str = Field(..., min_length=2, description="Processor type")
    ram: int = Field(..., gt=0, description="RAM in GB")
    storage: int = Field(..., gt=0, description="Storage in GB")

    class Config:
        example = {
            "name": "Dell XPS 13",
            "brand": "Dell",
            "price": 999.99,
            "processor": "Intel i7",
            "ram": 16,
            "storage": 512
        }

class LaptopUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    processor: Optional[str] = None
    ram: Optional[int] = None
    storage: Optional[int] = None

class LaptopResponse(BaseModel):
    id: int
    name: str
    brand: str
    price: float
    processor: str
    ram: int
    storage: int

# ══════════════════════════════════════════════════════════════════════════
# DEPENDENCY FUNCTIONS - Using "Depends" Pattern
# ══════════════════════════════════════════════════════════════════════════

# Dep 1 - API Key Validation
# def verify_api_key(x_api_key: str = Header(..., description="API Key required")) -> str:
#     """
#     Validate API Key from request header.
    
#     Raises:
#         HTTPException: 401 if API key is invalid
#     """
#     if x_api_key not in VALID_API_KEYS:
#         raise HTTPException(
#             status_code=401,
#             detail="❌ Invalid API Key. Access Denied!",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     return x_api_key

# Dep 2 - Load JSON Database
def get_db(api_key: str = Depends(verify_api_key)) -> dict:
    """Load JSON file as database after verifying API key"""
    return read_json()

# Dep 3 - Get Next Available ID
def get_next_id(db: dict = Depends(verify_api_key)) -> int:
    """Get auto-incremented next ID"""
    return db["next_id"]

# Dep 4 - Validate Laptop Exists (for GET/PUT/DELETE)
def get_laptop_or_404(
    laptop_id: int,
    db: dict = Depends(get_db)
) -> dict:
    """
    Fetch laptop by ID or raise 404 error.
    Reusable dependency for GET, PUT, DELETE operations.
    """
    laptop = db["laptops"].get(str(laptop_id))
    if not laptop:
        raise HTTPException(
            status_code=404,
            detail=f"❌ Laptop with ID {laptop_id} not found"
        )
    return laptop

# ══════════════════════════════════════════════════════════════════════════
# ROUTES - CRUD OPERATIONS
# ══════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Info"])
async def root():
    """API Documentation and Health Check"""
    return {
        "title": "Laptop Product CRUD API",
        "version": "2.0.0",
        "message": "All endpoints require API Key validation",
        "api_key_header": "X-API-Key",
        "valid_api_keys_for_testing": VALID_API_KEYS,
        "endpoints": {
            "POST /laptops": "Create new laptop",
            "GET /laptops": "Get all laptops",
            "GET /laptops/{laptop_id}": "Get specific laptop",
            "PUT /laptops/{laptop_id}": "Update laptop",
            "DELETE /laptops/{laptop_id}": "Delete laptop"
        },
        "usage_example": "curl -H 'X-API-Key: laptop-key-123' http://localhost:8000/laptops",
        "docs": "Visit http://localhost:8000/docs for Swagger UI"
    }

# ── CREATE ─────────────────────────────────────────────────────────────────
@app.post("/laptops", status_code=201, tags=["Laptops"], summary="Create new laptop")
def create_laptop(
    laptop: LaptopCreate,
    db: dict = Depends(get_db),
    next_id: int = Depends(get_next_id),
    api_key: str = Depends(verify_api_key)
):
    """
    Create a new laptop product.
    
    **Security:** Requires API Key in header (X-API-Key)
    """
    new_laptop = {"id": next_id, **laptop.model_dump()}
    
    db["laptops"][str(next_id)] = new_laptop
    db["next_id"] = next_id + 1
    write_json(db)
    
    return {
        "message": "✅ Laptop created successfully",
        "laptop": new_laptop
    }


# @app.post("/laptops", status_code=201)
# def create_laptop(
#     laptop: LaptopCreate,
#     db:      dict = Depends(get_db),
#     next_id: int  = Depends(get_next_id),
# ):
#     new_laptop = {"id": next_id, **laptop.model_dump()}
#     db["laptops"][str(next_id)] = new_laptop
#     db["next_id"] = next_id + 1
#     write_json(db)
#     return {"message": "✅ Laptop created", "laptop": new_laptop}

# ── READ ALL ───────────────────────────────────────────────────────────────
@app.get("/laptops", tags=["Laptops"], summary="Get all laptops")
def get_all_laptops(
    db: dict = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Retrieve all laptops from the database.
    
    **Security:** Requires API Key in header (X-API-Key)
    """
    laptops = list(db["laptops"].values())
    return {
        "message": "✅ All laptops retrieved",
        "count": len(laptops),
        "laptops": laptops
    }

# ── READ ONE ───────────────────────────────────────────────────────────────
@app.get("/laptops/{laptop_id}", tags=["Laptops"], summary="Get specific laptop")
def get_laptop(
    laptop_id: int,
    laptop: dict = Depends(get_laptop_or_404),
    api_key: str = Depends(verify_api_key)
):
    """
    Retrieve a specific laptop by ID.
    
    **Security:** Requires API Key in header (X-API-Key)
    """
    return {
        "message": "✅ Laptop retrieved",
        "laptop": laptop
    }

# ── UPDATE ─────────────────────────────────────────────────────────────────
@app.put("/laptops/{laptop_id}", tags=["Laptops"], summary="Update laptop")
def update_laptop(
    laptop_id: int,
    updates: LaptopUpdate,
    laptop: dict = Depends(get_laptop_or_404),
    db: dict = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Update an existing laptop (partial or full update).
    
    **Security:** Requires API Key in header (X-API-Key)
    """
    updated_data = updates.model_dump(exclude_unset=True)
    laptop.update(updated_data)
    
    db["laptops"][str(laptop_id)] = laptop
    write_json(db)
    
    return {
        "message": "✅ Laptop updated successfully",
        "laptop": laptop
    }

# ── DELETE ─────────────────────────────────────────────────────────────────
@app.delete("/laptops/{laptop_id}", tags=["Laptops"], summary="Delete laptop")
def delete_laptop(
    laptop_id: int,
    laptop: dict = Depends(get_laptop_or_404),
    db: dict = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Delete a laptop product from the database.
    
    **Security:** Requires API Key in header (X-API-Key)
    """
    del db["laptops"][str(laptop_id)]
    write_json(db)
    
    return {
        "message": f"✅ Laptop {laptop_id} deleted successfully",
        "deleted_laptop_id": laptop_id
    }

# ── ADVANCED: Search by Brand ──────────────────────────────────────────────
@app.get("/laptops/brand/{brand_name}", tags=["Laptops"], summary="Search by brand")
def search_by_brand(
    brand_name: str,
    db: dict = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Search for laptops by brand name.
    
    **Security:** Requires API Key in header (X-API-Key)
    """
    brand_laptops = [
        laptop for laptop in db["laptops"].values()
        if laptop["brand"].lower() == brand_name.lower()
    ]
    
    if not brand_laptops:
        raise HTTPException(
            status_code=404,
            detail=f"❌ No laptops found for brand '{brand_name}'"
        )
    
    return {
        "message": f"✅ Laptops found for brand '{brand_name}'",
        "count": len(brand_laptops),
        "laptops": brand_laptops
    }

# ── ADVANCED: Get by Price Range ───────────────────────────────────────────
@app.get("/laptops/price-range/{min_price}/{max_price}", tags=["Laptops"], summary="Filter by price")
def filter_by_price(
    min_price: float,
    max_price: float,
    db: dict = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Filter laptops by price range.
    
    **Security:** Requires API Key in header (X-API-Key)
    """
    if min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="❌ min_price cannot be greater than max_price"
        )
    
    price_filtered = [
        laptop for laptop in db["laptops"].values()
        if min_price <= laptop["price"] <= max_price
    ]
    
    if not price_filtered:
        raise HTTPException(
            status_code=404,
            detail=f"❌ No laptops found in price range ${min_price} - ${max_price}"
        )
    
    return {
        "message": f"✅ Laptops found in price range ${min_price} - ${max_price}",
        "count": len(price_filtered),
        "laptops": price_filtered
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)