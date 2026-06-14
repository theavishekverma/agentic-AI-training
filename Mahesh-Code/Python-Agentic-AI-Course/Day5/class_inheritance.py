class Vehicle:
    def __init__(self, make, model, fuel_type, price):
        self.make = make
        self.model = model        
        self.fuel_type = fuel_type
        self.price = price

    def display_info(self):
        return f"Vehicle Make: {self.make}, Model: {self.model}, Fuel Type: {self.fuel_type}, Price: ${self.price}"


class Car(Vehicle):
    def __init__(self, make, model, fuel_type, price, num_doors):
        super().__init__(make, model, fuel_type, price)
        self.num_doors = num_doors

    def display_info(self):
        base_info = super().display_info()
        return f"{base_info}, Number of Doors: {self.num_doors}"
    
class Bike(Vehicle):
    def __init__(self, make, model, fuel_type, price, has_pedals):
        super().__init__(make, model, fuel_type, price)
        self.has_pedals = has_pedals

    def display_info(self):
        base_info = super().display_info()
        pedals_info = self.has_pedals
        return f"{base_info}, Has Pedals: {pedals_info}"
    

toyota=Car("Toyota", "Camry", "Gasoline", 24000, 4)
print(toyota.display_info())