class StockError(Exception):
    """Base class for exceptions in this module."""
    pass

class InsufficientStockError(StockError):
    """Exception raised for errors in the stock quantity."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidStockOperationError(StockError):
    """Exception raised for invalid stock operations."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

        
stock = {"TCS": 100, "INFY": 200,"WIPRO": 150} 

def sell_stock(stock_name,quantity):
    if stock_name not in stock:
        raise InvalidStockOperationError(f"Stock '{stock_name}' does not exist.")
    if stock[stock_name] < quantity:
        raise InsufficientStockError(f"Insufficient stock for '{stock_name}'. Available: {stock[stock_name]}, Requested: {quantity}")
    print(f"Selling {quantity} shares of {stock_name}.")

if __name__ == "__main__":
    try:
        sell_stock("TCS", 150)  # Valid operation
    except (InsufficientStockError, InvalidStockOperationError) as e:
        print(f"Error: {e.message}")

    sell_stock("GOOG", 50)  # Invalid stock
  