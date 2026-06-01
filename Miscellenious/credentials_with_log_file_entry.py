import datetime
import getpass

username = input("Enter your username: ")
#password = input("Enter your password: ")
password = getpass.getpass("Enter password: ")

print(f"Username: {username}")
print(f"Password entered:", '*' * len(password))

# Get current date and time
current_time = datetime.datetime.now()

# Write to a log file
with open('C:\\Users\\Avishek\\agentic-AI-training\\Credentials.log', 'a') as f:
    f.write(f"======================== {current_time} ========================:\n")
    f.write(f"Username: {username}\n")
    f.write(f"Password: {password}\n")
    #f.write("Password entered:", '*' * len(password))
    f.write("\n") # Add a newline for better readability between entries

print(f"Credentials and timestamp saved to credentials.log on {current_time}")
