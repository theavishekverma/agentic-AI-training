# Empty list
'''
fruits=[]


# List of cities
cities=["Pune","Mumbai","Delhi","Bangalore"]
print(cities)

# Access list members
print(cities[1])

# Check Noida is in cities list or not
print("Noida" in cities)
print("Pune" in cities)

if "Noida" in cities:
    print("Noida is in cities list")
else:
    print("Noida is not in cities list")    

cities[2]="Noida"
print(cities)

cities[1]="Noida"
print(cities)

#Allows duplicate values

cities.append("Delhi")
print(cities)

print(len(cities))

print("Count of Noida in cities list:", cities.count("Noida"))

#cities.clear()
#print(cities)

#print(len(cities))

cities.remove("Noida")
print(cities)
cities.remove("Noida")
print(cities)

cities.pop()
print(cities)



fruits=["Apple","Mango","Banana","Grapes"]

# List slicing
print(fruits[0:2])


stocks=["TCS","INFY","RELIANCE","HDFCBANK"]
for stock in stocks:
    if stock=="RELIANCE":
        print("Call X client System to sell this stocks")
    elif stock=="HDFCBANK":
        print("Call Y client System to buy this stocks")            
    elif stock=="TCS":
        print("Call Z client System to sell this stocks")    

'''        

stocks=["TCS","INFY","RELIANCE","HDFCBANK"]

stocks.sort()
print("sorted stocks:", stocks)
stocks.reverse()
print("Reversed stocks:", stocks)