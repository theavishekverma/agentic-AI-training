import csv

data = [
    {
        "name":"Vishal",
        "age": 25,
        "city": "Delhi"
     },
     {
        "name":"Priya",
        "age": 30,
        "city": "Mumbai"
     }
]

with open("data.csv","w",newline="") as file:
    keys = data[0].keys()
    writer = csv.DictWriter(file,fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)
