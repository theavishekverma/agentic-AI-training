# Class and Constructor Demonstration

class Car:
    # Constructor (__init__) is called when a new object is created
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
    
    # Method to display car details
    print("Car class created with a constructor to initialize attributes.")
    def display_info(self):
        print(f"Car: {self.year} {self.brand} {self.model}")

# Creating objects of the Car class
car1 = Car("Toyota", "Corolla", 2020)
car2 = Car("Tesla", "Model S", 2023)
print("********* Car objects created successfully.********** ")
print("********* Displaying car information: **********")
car1.display_info()
car2.display_info()


# Calling methods