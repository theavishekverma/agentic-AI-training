import json

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse

app = FastAPI(title="Stock AI API", 
              description="A simple FastAPI application to demonstrate Stock portfolio creation with update, delete and patch operations." , 
              version="1.0.0" , 
              contact={"name": "Avishek Verma", "email": "your.email@example.com"},
              )

class stock(BaseModel):
    stock_name: str = Field(..., min_length=3, max_length=50, description="Name of the stock")
    stock_symbol: str = Field(..., min_length=1, max_length=10, description="Stock symbol")
    stock_buy_price: int = Field(..., gt=0, description="Price at which the stock was bought")
    stock_unit: int = Field(..., gt=0, description="Number of units bought")



Portfolio = []  # Simulated in-memory portfolio storage

@app.get("/stocks")
async def get_stocks():
    return JSONResponse(status_code=200, content={"stocks": Portfolio})

@app.get("/stocks/{stock_symbol}")
async def get_stock(stock_symbol: str):
    for s in Portfolio:
        if json.loads(s)["stock_symbol"] == stock_symbol:
            return JSONResponse(status_code=200, content={"stock": json.loads(s)})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Stock with symbol {stock_symbol} not found in portfolio.")

@app.post("/stocks", status_code=status.HTTP_201_CREATED)
async def add_stocks(stock: stock):
    Portfolio.append(json.dumps(stock.dict()))  # Simulate saving to a database
    return JSONResponse(status_code=201, content={"message": "Stock added to portfolio!", "stock": Portfolio[-1]})

@app.delete("/stocks/{stock_symbol}", status_code=status.HTTP_200_OK)
async def delete_stock(stock_symbol: str):
    global Portfolio
    Portfolio = [s for s in Portfolio if json.loads(s)["stock_symbol"] != stock_symbol]
    return JSONResponse(status_code=200, content={"message": f"Stock with symbol {stock_symbol} deleted from portfolio!"})

@app.put("/stocks/{stock_symbol}", status_code=status.HTTP_200_OK)
async def update_stock(stock_symbol: str, updated_stock: stock):
    global Portfolio
    for i, s in enumerate(Portfolio):
        if json.loads(s)["stock_symbol"] == stock_symbol:
            Portfolio[i] = json.dumps(updated_stock.dict())
            return JSONResponse(status_code=200, content={"message": f"Stock with symbol {stock_symbol} updated!", "stock": Portfolio[i]})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Stock with symbol {stock_symbol} not found in portfolio.")

@app.patch("/stocks/{stock_symbol}", status_code=status.HTTP_200_OK)
async def patch_stock(stock_symbol: str, updated_fields: stock):
    global Portfolio
    for i, s in enumerate(Portfolio):
        stock_data = json.loads(s)
        if stock_data["stock_symbol"] == stock_symbol:
            updated_data = {**stock_data, **updated_fields.dict(exclude_unset=True)}
            Portfolio[i] = json.dumps(updated_data)
            return JSONResponse(status_code=200, content={"message": f"Stock with symbol {stock_symbol} patched!", "stock": Portfolio[i]})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Stock with symbol {stock_symbol} not found in portfolio.")