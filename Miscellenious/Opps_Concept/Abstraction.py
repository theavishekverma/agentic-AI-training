from abc import ABC, abstractmethod

# Abstract Base Class
class Investment(ABC):
    @abstractmethod
    def calculate_value(self):
        pass   # Must be implemented by child classes

    @abstractmethod
    def investment_info(self):
        pass   # Must be implemented by child classes


# Child Class 1: Stock
class Stock(Investment):
    def __init__(self, name, price, quantity):
        self.name = name
        self.__price = price       # private (inaccessible directly)
        self.__quantity = quantity # private (inaccessible directly)

    def calculate_value(self):
        return self.__price * self.__quantity

    def investment_info(self):
        print(f"Stock: {self.name}, Value: ₹{self.calculate_value()}")


# Child Class 2: Mutual Fund
class MutualFund(Investment):
    def __init__(self, name, nav, units):
        self.name = name
        self.__nav = nav           # private (inaccessible directly)
        self.__units = units       # private (inaccessible directly)

    def calculate_value(self):
        return self.__nav * self.__units

    def investment_info(self):
        print(f"Mutual Fund: {self.name}, Value: ₹{self.calculate_value()}")


# Demonstration
portfolio = [
    Stock("TCS", 3500, 10),              # 10 shares at ₹3500
    MutualFund("HDFC Equity Fund", 250, 100)  # 100 units at ₹250 NAV
]

for investment in portfolio:
    investment.investment_info()