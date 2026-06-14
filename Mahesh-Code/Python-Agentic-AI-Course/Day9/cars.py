import csv

cars = [
    ["Toyota", "Camry", 2020, "Sedan"],
    ["Honda", "Civic", 2019, "Sedan"],
    ["Ford", "Mustang", 2021, "Coupe"],
    ["Tesla", "Model 3", 2022, "Sedan"]
]

with open("cars.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(cars)