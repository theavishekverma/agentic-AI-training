fruits=["apple", "banana", "orange"] # This is a list of fruits

'''
for fruit in fruits: # This will iterate through each fruit in the list of fruits
    if fruit == "banana": # This will check if the current fruit is "banana"
        print("Banana is healthy") # This will print a message if the current fruit is "banana"
    


for i in range(5): # This will iterate through the numbers from 0 to 4
    print(i) # This will print the current number in the iteration

'''

students=[{"name":"john","age":25,"city":"New York"},
          {"name":"jane","age":30,"city":"Los Angeles"},
          {"name":"bob","age":35,"city":"Chicago"}]

marks=0
for student in students:
     #marks+=student["age"] # This will print the type of the variable 'student', which is <class 'dict'>
     marks=marks+student["age"] # This will print the type of the variable 'student', which is <class 'dict'>



print(f"Total marks: {marks}") # This will print the total marks, which is the sum of the ages of all students

# while syntax
#while <condition>:
#     <action>


i=0
while i <= 5:
     print(i) # This will print the current value of 'i' in the iteration
     i+=1 # This will increment the value of 'i' by 1 in each iteration
     if i == 3:
          break