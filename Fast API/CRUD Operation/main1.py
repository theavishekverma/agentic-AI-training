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
    dependencies=[Depends(verify_api_key)]  # Global dependency for API Key validation
)

# ══════════════════════════════════════════════════════════════════════════
# Backend File and Data Management
# ══════════════════════════════════════════════════════════════════════════

JSON_FILE = "laptops_products.json"

# ══════════════════════════════════════════════════════════════════════════
# JSON FILE HELPERS  ← fixes are here
# ══════════════════════════════════════════════════════════════════════════
def write_json(data: dict):
    """Always writes a proper dict to the JSON file."""
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def read_json() -> dict:
    """
    Reads JSON file and returns a dict.
    Auto-heals if file is missing, empty, or corrupted.
    """
    default = {"next_id": 1, "Laptops": {}}

    # ── File doesn't exist → create fresh ─────────────────────────────
    if not os.path.exists(JSON_FILE):
        write_json(default)
        return default

    # ── File exists → try to parse it ─────────────────────────────────
    try:
        with open(JSON_FILE, "r") as f:
            content = f.read().strip()

        # ── Empty file guard ───────────────────────────────────────────
        if not content:
            write_json(default)
            return default

        data = json.loads(content)   # ✅ parse string → dict

        # ── Validate it's a dict with expected keys ────────────────────
        if not isinstance(data, dict):
            raise ValueError("JSON root is not a dict")
        if "next_id" not in data or "Laptops" not in data:
            raise ValueError("Missing required keys")

        return data

    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  Corrupted JSON ({e}), resetting file.")
        write_json(default)
        return default

# ══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ══════════════════════════════════════════════════════════════════════════

class LaptopCreate(BaseModel):
    name:    str
    brand:   str
    price:   float
    processor: str
    ram:     int
    storage: int
#02028999222 - Dr. Parag Sancheti Appointment 

class LaptopUpdate(BaseModel):
    name:    Optional[str] = None
    brand:   Optional[str] = None
    price:   Optional[float] = None
    processor: Optional[str] = None
    ram:     Optional[int] = None
    storage: Optional[int] = None

# ══════════════════════════════════════════════════════════════════════════
# DEPENDENCY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════

def get_db() -> dict:
    db = read_json()
    print(f"DEBUG get_db → type={type(db)}, value={db}")  # remove after testing
    return db

def get_laptop_or_404(laptop_id: int, db: dict = Depends(get_db)) -> dict:
    laptop = db["Laptops"].get(str(laptop_id))
    if not laptop:
        raise HTTPException(status_code=404,
                            detail=f"Laptop {laptop_id} not found")
    return laptop

def get_next_id(db: dict = Depends(get_db)) -> int:
    return db["next_id"]     # ✅ now safe — db is guaranteed a dict

# ══════════════════════════════════════════════════════════════════════════
# ROUTES — CRUD
# ══════════════════════════════════════════════════════════════════════════

# CREATE

app.include_router(create_router, prefix="/api", tags=["Laptops"])
#@app.post("/create",status_code=201, dependencies=[Depends(create_laptop)])


# @app.post("/laptops", status_code=201)
# def create_laptop(
#     laptop: LaptopCreate,
#     db:      dict = Depends(get_db),
#     next_id: int  = Depends(get_next_id),
# ):
#     new_laptop = {"id": next_id, **laptop.model_dump()}
#     db["Laptops"][str(next_id)] = new_laptop
#     db["next_id"] = next_id + 1
#     write_json(db)
#     return {"message": "✅ Laptop created", "laptop": new_laptop}

# READ ALL
@app.get("/laptops")
def get_all_laptops(db: dict = Depends(get_db)):
    laptops = list(db["Laptops"].values())
    return {"total": len(laptops), "laptops": laptops}

# READ ONE
@app.get("/laptops/{laptop_id}")
def get_laptop(laptop: dict = Depends(get_laptop_or_404)):
    return laptop

# UPDATE
@app.put("/laptops/{laptop_id}")
def update_laptop(
    laptop_id: int,
    updates:    LaptopUpdate,
    laptop:    dict = Depends(get_laptop_or_404),
    db:         dict = Depends(get_db),
):
    for field, value in updates.model_dump(exclude_none=True).items():
        laptop[field] = value
    db["Laptops"][str(laptop_id)] = laptop
    write_json(db)
    return {"message": "✅ Laptop updated", "laptop": laptop}

# DELETE
@app.delete("/laptops/{laptop_id}")
def delete_laptop(
    laptop_id: int,
    laptop:    dict = Depends(get_laptop_or_404),
    db:         dict = Depends(get_db),
):
    del db["Laptops"][str(laptop_id)]
    write_json(db)
    return {"message": f"✅ Laptop '{laptop['name']}' deleted"}

# RESET
@app.delete("/laptops")
def reset_all():
    write_json({"next_id": 1, "Laptops": {}})
    return {"message": "🗑️ All laptops deleted"}