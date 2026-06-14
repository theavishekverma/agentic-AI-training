#read text file

#open file syntax
#file = open("file_name.txt", "r")


file = open("dummy.txt", "r")

#print(type(file))

#read file content
content= file.read()
print(content)

#closing file
file.close()
print(content)

