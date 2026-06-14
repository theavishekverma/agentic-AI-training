from fastapi import FastAPI,Response,HTTPException
from fastapi.responses import JSONResponse


app = FastAPI(title="Stock AI API",summary="This API developed for stock price prediction using AI",version="1.0")

@app.get("/")
def get_stock_info():
    response = Response(content="Hello Vishal", media_type="application/json")
    return response


@app.get("/hello")
def get_info():
    return {"message": "Hello Vishal"}


@app.get("/stock/{stock_name}")
def get_stock_price(stock_name: str):
    # Here you can implement your logic to fetch stock price based on the stock_name
    # For demonstration, we will return a dummy stock price
    if stock_name.lower() == "tcs":
        return JSONResponse(status_code=200, content={"stock_name": stock_name, "price": 3000})
    elif stock_name.lower() == "reliance":
        return JSONResponse(status_code=200, content={"stock_name": stock_name, "price": 2500})
    else:
        raise HTTPException(status_code=404, detail="Stock not found")
        