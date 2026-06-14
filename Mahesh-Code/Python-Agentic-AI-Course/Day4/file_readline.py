# readline function for reading file

file_obj = open("stock.csv", "r")
lines= file_obj.readlines()
for line in lines:
    print(line)

# read() -> reads the entire file content and returns as a string
# readline() -> reads a single line from the file and returns as a string
# readlines() -> reads the entire file content and returns as a list of lines
