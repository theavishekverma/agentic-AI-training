from fastapi import FastAPI,HTTPException, Header, Depends
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse
from auth import authenticate_user
import os
from action import read_products, write_products
from validate import verify_product_data, Product



app = FastAPI(title="Laptab Bazar API", 
              summary="This API developed for laptop management system", 
              version="1.0",
              dependencies=[Depends(authenticate_user)])


@app.get("/products")
def get_products():
    inventory = read_products()
    return JSONResponse(status_code=200, content={"products": inventory})

@app.get("/products/{product_id}")
def get_product(product_id: int):
    inventory = read_products()
    for product in inventory:
        if product["product_id"] == product_id:
            return JSONResponse(status_code=200, content={"product": product})
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
def add_product(product: Product,
                verify_product_data = Depends(verify_product_data)):

    inventory = read_products()
    inventory.append(product.dict())
    write_products(inventory)
    # Send data to header for verification
    return JSONResponse(status_code=201, content={"message": "Product added successfully", "product": product.dict()})


@app.put("/products/{product_id}")
def update_product(product_id: int, 
                   updated_product: Product,
                   verify_product_data = Depends(verify_product_data)):
    inventory = read_products()
    for product in inventory:
        if product["product_id"] == product_id:
            product.update(updated_product.dict())
            write_products(inventory)
            return JSONResponse(status_code=200, content={"message": "Product updated successfully"})
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    inventory = read_products()
    for product in inventory:
        if product["product_id"] == product_id:
            inventory.remove(product)
            write_products(inventory)
            return JSONResponse(status_code=200, content={"message": "Product deleted successfully"})
    raise HTTPException(status_code=404, detail="Product not found")