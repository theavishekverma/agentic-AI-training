# Parent Class
class Car:
    def __init__(self, maker, model, year):
        self.maker = maker
        self.model = model
        self.year = year

    def car_info(self):
        print(f"{self.year} {self.maker} {self.model}")

# Child Class inheriting from Car
class ElectricCar(Car):
    def __init__(self, maker, model, year, battery_capacity):
        # Call parent constructor using super()
        super().__init__(maker, model, year)
        self.battery_capacity = battery_capacity

    def car_info(self):
        # Override parent method (Polymorphism)
        print(f"{self.year} {self.maker} {self.model} - Battery: {self.battery_capacity} kWh")

# Another Child Class
class SportsCar(Car):
    def __init__(self, maker, model, year, horsepower):
        super().__init__(maker, model, year)
        self.horsepower = horsepower

    def car_info(self):
        print(f"{self.year} {self.maker} {self.model} - Horsepower: {self.horsepower} HP")


# Demonstration
car1 = Car("Toyota", "Corolla", 2020)
car2 = ElectricCar("Tesla", "Model S", 2023, 100)
car3 = SportsCar("Ferrari", "488 GTB", 2021, 660)

car1.car_info()   # 2020 Toyota Corolla
car2.car_info()   # 2023 Tesla Model S - Battery: 100 kWh
car3.car_info()   # 2021 Ferrari 488 GTB - Horsepower: 660 HP