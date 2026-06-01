import os

# 1. Create a new directory
new_dir = "new_directory"
os.makedirs(new_dir, exist_ok=True)
print(f"Directory '{new_dir}' created successfully.")

# 2. Create and open a text file in that directory
file_path = os.path.join(new_dir, "sample.txt")
file = open(file_path, "w")

# 3. Write a line "this is first line in this file"
file.write("this is first line in this file")

# 4. Close the text file
file.close()
print("File closed after writing.")

# 5. Print the content of the text file
file = open(file_path, "r")
content = file.read()
print(f"Content of the file: {content}")

# 6. Close the text file
file.close()
print("File closed after reading.")