from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

app = FastAPI(title="Stock AI API",summary="This API developed for stock price prediction using AI",version="1.0")

class Stock(BaseModel):
    stock_name: str
    stock_symbol: str
    stock_buy_price: float
    quality: int

portfolio = []

@app.get("/stocks")
def get_stocks():
    print(portfolio)
    return JSONResponse(status_code=200, content={"stocks": portfolio})

@app.get("/stocks/{stock_symbol}")
def get_stock(stock_symbol: str):
    for stock in portfolio:
        stock_data = json.loads(stock)
        if stock_data["stock_symbol"].lower() == stock_symbol.lower():
            return JSONResponse(status_code=200, content={"stock": stock_data})
    raise HTTPException(status_code=404, detail="Stock not found")


@app.post("/stocks")
def add_stock(stock: Stock):
    portfolio.append(json.dumps(stock.dict()))
    return JSONResponse(status_code=201, content={"message": "Stock added successfully"})



@app.put("/stocks/{stock_symbol}")
def update_stock(stock_symbol: str, updated_stock: Stock):
    for stock in portfolio:
        stock_data = json.loads(stock)
        if stock_data["stock_symbol"].lower() == stock_symbol.lower():
            stock_data.update(updated_stock.dict())
            portfolio[portfolio.index(stock)] = json.dumps(stock_data)
            return JSONResponse(status_code=200, content={"message": "Stock updated successfully"})
    raise HTTPException(status_code=404, detail="Stock not found")


@app.delete("/stocks/{stock_symbol}")
def delete_stock(stock_symbol: str):
    for stock in portfolio:
        stock_data = json.loads(stock)
        if stock_data["stock_symbol"].lower() == stock_symbol.lower():
            portfolio.remove(stock)
            return JSONResponse(status_code=200, content={"message": "Stock deleted successfully"})
    raise HTTPException(status_code=404, detail="Stock not found")