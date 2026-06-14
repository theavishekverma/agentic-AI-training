'''
file_obj=open("cars.csv","r")

data= file_obj.readlines()
suv=[]
sedan=[]
for line in data:
    car_type=line.split(",")[3].strip()
    if car_type=="suv":
        suv.append(line)
    elif car_type=="sedan":
        sedan.append(line)
file_obj.close()

print("SUV Cars:", suv)
print("Sedan Cars:", sedan)

file=open("suv_cars.csv","a")
file.write("car_name,car_price,car_color,car_type\n")
for car in suv:
    file.write(car)
file.close()

file=open("sedan_cars.csv","a")
file.write("car_name,car_price,car_color,car_type\n")
for car in sedan:
    file.write(car)
file.close()    


# write lines to a file

file=open("suv_cars1.csv","a")
file.writelines(suv)
file.close()


file=open("sedan_cars1.csv","a")
file.writelines(sedan)
file.close()
'''


data1="pranay,techgeekconnect,python,programming"
data2="vishal,techgeekconnect,java,programming"


data=["pranay,techgeekconnect,python,programming\n","vishal,techgeekconnect,java,programming\n"]

file=open("data.csv","a")
file.writelines(data)
file.close()

#write function -> writes a string to a file and returns the number of characters written
#eritelines function -> writes a list of strings to a file and returns the number of characters written