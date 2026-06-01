class Stock:
    def __init__(self, name, price, quantity):
        self.name = name              # Public attribute
        self.__price = price          # Private attribute
        self.__quantity = quantity    # Private attribute

    # Public method to access private attributes safely
    def get_value(self):
        return self.__price * self.__quantity

    # Public method to update private attributes
    def buy(self, qty, price):
        self.__quantity += qty
        self.__price = price

    def sell(self, qty):
        if qty <= self.__quantity:
            self.__quantity -= qty
        else:
            print("Not enough shares to sell!")

    def stock_info(self):
        print("****************")
        print(f"Stock: {self.name}, Quantity: {self.__quantity}, Price: ₹{self.__price}")
        print("****************")


# Demonstration
stock1 = Stock("Infosys", 1500, 20)

# ✅ Accessible (public attribute)
print("****************")
print("Accessible Attribute:", stock1.name)   # Works fine

# ❌ Inaccessible (private attributes)
# Direct access will raise an AttributeError
try:
    print("****************")
    print(stock1.__price)
except AttributeError:
    print("Cannot access __price directly (Encapsulation in action)")

# ✅ Access private attributes via public methods
stock1.stock_info()
print("Portfolio Value:", stock1.get_value())

# ✅ Update values safely
stock1.buy(10, 1600)
stock1.stock_info()
print("Portfolio Value:", stock1.get_value())
print("****************")