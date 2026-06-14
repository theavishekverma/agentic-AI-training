number=10
divisor=0
try:
    division_result = number / divisor
except Exception as e:
    print("An error occurred:", e)
except ZeroDivisionError as e:
    print("Cannot divide by zero:", e)
finally:
    print("Cleanup operations.")

  # Exit the program after handling the exception
print("Program continues after handling the exception.")
