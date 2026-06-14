# function definition
#def <function_name>(<paramter>):
#    <function_body>
#     return <value>

# call function
#result = <function_name>(<argument>)
'''

def greet(name):
    print(f"Hello, {name}!")


greet("Vishal")
greet("Pranay")
greet("Mansi")


def welcome_message(name):
    return f"Welcome, {name}!"


message = welcome_message("Vishal")
print(message)
message = welcome_message("Pranay")
print(message)
message = welcome_message("Mansi")
print(message)
print(welcome_message("Avishek"))
'''

def stock_price_change(open_price, close_price):
    change_price = close_price - open_price
    change_percentage = (change_price / open_price) * 100
    return change_price, change_percentage


change_price, change_percentage = stock_price_change(3343, 3300)
print("TCS stock price change: %.2f (%.2f%%)" % (change_price, change_percentage))

change_price, change_percentage = stock_price_change(1400, 1450)
print("Infosys stock price change: %.2f (%.2f%%)" % (change_price, change_percentage))

change_price, change_percentage = stock_price_change(243, 241)
print("Wipro stock price change: %.2f (%.2f%%)" % (change_price, change_percentage))
