from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

# Initialize the FastAPI application
app = FastAPI(title="My FastAPI Application", description="A simple FastAPI application to demonstrate API creation.")


@app.get("/GetStockDetails/{stock_id}")
def get_stock_details(stock_id: int):
    if stock_id == 1:
        stock_name = "Apple Inc."
        response = Response(content="stock_name", media_type="application/json")
        return JSONResponse(status_code=200, content={"stock_name": stock_name})
    elif stock_id == 2:
        stock_name = "Microsoft Corporation"
        response = Response(content="stock_name", media_type="application/json")
        return JSONResponse(status_code=200, content={"stock_name": stock_name})

    elif stock_id == 3:
        stock_name = "Amazon.com, Inc."
        response = Response(content="stock_name", media_type="application/json")
        return JSONResponse(status_code=200, content={"stock_name": stock_name})
    else:
         return JSONResponse(status_code=404, content={"message": "Stock not found"})


@app.get("/Welcome")
def get_welcome_message_API():
    response = Response(content="Welcome to my FastAPI application!", media_type="application/json")
    return JSONResponse(status_code=200, content={"message": "Welcome to my FastAPI application!"})

# Define a GET endpoint at the root URL ("/")
@app.get("/hello")
async def Hello_World_API():
    return {"message": "Hello World"}