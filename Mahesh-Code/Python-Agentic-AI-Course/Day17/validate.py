from fastapi import HTTPException
from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    product_name: str
    product_brand: str
    product_price: float
    product_qty: int

def verify_product_data(product: Product):
    print(f"Verifying product data: {product}")
    if product.product_price < 0:
        raise HTTPException(status_code=400, detail="Product price cannot be negative")
    if product.product_qty < 0:
        raise HTTPException(status_code=400, detail="Product quantity cannot be negative")
    return True
