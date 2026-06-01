import getpass

# Prompt for password (input is hidden)
password = getpass.getpass("Enter password: ")

# Display asterisks equal to password length
print("Password entered:", '*' * len(password))