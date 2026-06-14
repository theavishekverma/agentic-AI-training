class Stock:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_price(self):
        return self.price
    
    def total_value(self):
        return self.price * self.quantity

class MutualFund:
    def __init__(self, mutual_fund_name, notional_value, units):
        self.mutual_fund_name = mutual_fund_name
        self.notional_value = notional_value
        self.units = units

    def get_price(self):
        return self.notional_value
    
    def total_value(self):
        return self.notional_value * self.units    
        
class Portfolio(Stock, MutualFund):
    def __init__(self, name, price, quantity,mutual_fund_name, notional_value, units, gold_price, property_price):
        Stock.__init__(self, name, price, quantity)
        MutualFund.__init__(self, mutual_fund_name, notional_value, units)
        self.gold_price = gold_price
        self.property_price = property_price

    # calculate total value of stock and mutual fund
    def total_portfolio_value(self):
        stock_value = Stock.total_value(self)
        mutual_fund_value = MutualFund.total_value(self)
        return stock_value + mutual_fund_value + self.gold_price + self.property_price
    


pranay=Portfolio("TCS", 3500, 10,"Mutual Fund A", 5000, 10000, 1000000, 5000000)
mansi=Portfolio("Infy", 150, 40,"Mutual Fund B", 500000, 1000000, 100000000, 500000000)
vishal=Portfolio("Reliance", 2050, 40,"Mutual Fund C", 500000000, 1000000, 100000000, 500000000)
print("Total value of Pranay's portfolio:", pranay.total_portfolio_value())
print("Total value of Mansi's portfolio:", mansi.total_portfolio_value())
print("Total value of Vishal's portfolio:", vishal.total_portfolio_value())