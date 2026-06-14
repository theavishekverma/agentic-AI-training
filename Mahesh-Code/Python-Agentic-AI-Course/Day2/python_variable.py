'''
number=10   # This is an integer variable
name="John" # This is a string variable
marks=95.523432442432 # This is a float variable
is_passed=True # This is a boolean variable


print("Number:", number) # This will print the value of the variable 'number'
print(name) # This will print the value of the variable 'name'
print("Marks : %.2f" % marks) # This will print the value of the variable 'marks' formatted to 2 decimal places
print(f"Is Passed: {is_passed}") # This will print the value of the variable 'is_passed' using an f-string for formatting


mobile_number=1234567890 # This is a variable to store a mobile number
print("Mobile Number:", mobile_number) # This will print the value of the variable 'mobile_number'

mobile_number=1234567890
flat_number="B10"

print(type(mobile_number)) # This will print the type of the variable 'mobile_number'
print(type(flat_number)) # This will print the type of the variable 'flat_number'

print(type(int(str(mobile_number)))) # This will convert the integer 'mobile_number' to a string and print it


a="Hello" # This is a string variable
a=10
print(a) # This will print the value of the variable 'a'
#print(A) # This will print the value of the variable 'A'

#best practice to declare variable is to use small letters and underscores to separate words
first_name="John" # This is a variable to store the first name
last_name="Doe" # This is a variable to store the last name
full_name=first_name + " " + last_name # This will concatenate the first name and

first_name="python"
print(first_name)
firstName="python"


name,age,city="John",25,"New York" # This is a multiple assignment where we assign values to multiple variables in a single line
print(f"type(name): {type(name)}")
print(f"type(age): {type(age)}")
print(f"type(city): {type(city)}")

mark1=mark2=mark3=95

print(f"mark1: {mark1}, mark2: {mark2}, mark3: {mark3}")
'''

name=None
print(f"type(name): {type(name)}") # This will print the value of the variable 'name', which is None

fruits=[] # empty fruit list
fruits={} # empty fruit dictionary
fruits=() # empty fruit tuple

fruits=["apple", "banana", "orange"] # This is a list of fruits
print(fruits) # This will print the list of fruits
print(fruits[1]) # This will print the second fruit in the list, which is "banana"

print(type(fruits)) # This will print the type of the variable 'fruits', which is <class 'list'>

student_info={"name":"john",
              "age":25,
              "city":"New York"} # This is a dictionary to store student information

print(student_info["age"]) # This will print the dictionary containing student information

print(type(student_info)) # This will print the type of the variable 'student_info', which is <class 'dict'>



students=[{"name":"john","age":25,"city":"New York"},
          {"name":"jane","age":30,"city":"Los Angeles"},
          {"name":"bob","age":35,"city":"Chicago"}]
print(students[2]) # This will print the list of dictionaries containing student information
print(students[2]["name"]) # This will raise an error because we cannot access a list using a string index
print(type(students)) # This will print the type of the variable 'students', which is <class 'list'>

cities=("New York", "USA") # This is a tuple to store city information
print(cities) # This will print the tuple containing city information
print(type(cities)) # This will print the type of the variable 'cities', which is <class 'tuple'>