'''
#empty dictionary
stock_dict = {}

stock_dict={"stock_name":"TCS","stock_price":3000,"stock_volume":1000}

print(stock_dict)

#access the key
print(stock_dict.keys())

#access the value
print(stock_dict.values())

stock_dict["stock_name"]="INFOSYS"
print(stock_dict)


#stock_dict.clear()
#print(stock_dict)

print(stock_dict.get("stock_name")) #it will return none because we cleared the dictionary
print(stock_dict["stock_name"])

'''

cars=[{"brand":"BMW","model":"X5","year":2020},
      {"brand":"Audi","model":"Q7","year":2021},
      {"brand":"Mercedes","model":"GLS","year":2022},
      {"brand":"Toyota","model":"Land Cruiser","year":2023},
        {"brand":"Honda","model":"CR-V","year":2024},
         {"brand":"Ford","model":"Explorer","year":2025}
]
#print("Type of cars:",type(cars))

#print(cars[3]) #it will print the 4th dictionary in the list

#print(cars[3]["model"]) #it will print the model of the 4th dictionary in the list

for car in cars:
    if car["year"] > 2022:
        print(car["brand"],car["model"],car["year"])