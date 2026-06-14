
def update_price(new_price):
    print("I'm outside of the calss, trying to update the price to", new_price)


class stock:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_price(self, new_price):
        self.price = new_price

    def __str__(self):
        return f"{self.name} stock is currently priced at ${self.price}"
    
    def get_price(self):
        return self.price

tcs=stock("TCS", 3500, 100)
print(tcs)
tcs.update_price(3600)
print(tcs)

update_price(3700)
print(tcs)


infy=stock("INFY", 1500, 200)
infy.update_price(1550)
print(infy)

rel=stock("RELIANCE", 2000, 150)
rel.update_price(2100)
print(rel)
