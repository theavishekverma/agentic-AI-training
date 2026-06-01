# Parent Class
class Investment:
    def show_returns(self):
        raise NotImplementedError("Subclass must implement this method")

# Child Class 1: Stocks
class Stock(Investment):
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def show_returns(self):
        # Example: returns = price * quantity
        print("Calculating returns for Mutual Fund...")
        return f"Stock {self.name}: \nCurrent Value = ₹{self.price * self.quantity}"

# Child Class 2: Mutual Fund
class MutualFund(Investment):
    def __init__(self, name, nav, units):
        self.name = name
        self.nav = nav
        self.units = units

    def show_returns(self):
        # Example: returns = NAV * units
        print("Calculating returns for Mutual Fund...")
        return f"Mutual Fund {self.name}: \nCurrentValue = ₹{self.nav * self.units}"


# Demonstration of Polymorphism
portfolio = [
    Stock("TCS", 3500, 10),              # 10 shares of TCS at ₹3500 each
    MutualFund("HDFC Equity Fund", 250, 100)  # 100 units at ₹250 NAV
]

for investment in portfolio:
    # Same method name 'show_returns' behaves differently depending on object type
    print(investment.show_returns())