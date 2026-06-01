# Parent Class 1: Stocks
class Stocks:
    def __init__(self, stock_name, stock_value):
        self.stock_name = stock_name
        self.stock_value = stock_value

    def stock_info(self):
        print(f"Stock: {self.stock_name}, Value: ₹{self.stock_value}")

# Parent Class 2: Mutual Funds
class MutualFund:
    def __init__(self, fund_name, fund_value):
        self.fund_name = fund_name
        self.fund_value = fund_value

    def fund_info(self):
        print(f"Mutual Fund: {self.fund_name}, Value: ₹{self.fund_value}")

# Child Class inheriting from both Stocks and MutualFund
class Portfolio(Stocks, MutualFund):
    def __init__(self, owner, stock_name, stock_value, fund_name, fund_value):
        Stocks.__init__(self, stock_name, stock_value)       # Initialize Stocks
        MutualFund.__init__(self, fund_name, fund_value)     # Initialize MutualFund
        self.owner = owner

    def portfolio_info(self):
        print(f"Portfolio Owner: {self.owner}")
        self.stock_info()
        self.fund_info()


# Demonstration
portfolio1 = Portfolio("Avishek", "TCS", 120000, "HDFC Equity Fund", 80000)
portfolio2 = Portfolio("Abhilasha", "Infosys", 150000, "ICICI PruFund", 100000)
print("\n-----------------------------------------\n")
portfolio1.portfolio_info()
print("\n-----------------------------------------\n")
portfolio2.portfolio_info()
print("\n-----------------------------------------\n")
