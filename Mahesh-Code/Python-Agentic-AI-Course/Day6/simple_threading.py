# print 1 to 100 numbers using threading

import threading
import time

def print_numbers(start, end):
    print(f"Thread {threading.current_thread().name} starting to print numbers from {start} to {end}")
    for i in range(start, end + 1):
        time.sleep(0.1)  # Simulate some delay        
        print(i)
    print(f"Thread {threading.current_thread().name} finished printing numbers from {start} to {end}")    

# Create threads for printing numbers
start_time = time.time()

thread1 = threading.Thread(target=print_numbers, args=(1, 100))
# Start the threads
thread1.start()
print("Finished printing numbers from 1 to 100.")
print("Time taken: ", time.time() - start_time, "seconds")