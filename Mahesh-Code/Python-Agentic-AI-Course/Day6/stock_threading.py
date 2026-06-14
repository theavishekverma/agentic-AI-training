#stock count 10 and thread is 15 execute the code 

import time
import threading


stock = 10
lock=threading.Lock()
def sell_stock():
    global stock
   
    if stock > 0:
        print(f"Thread {threading.current_thread().name} is selling stock. Remaining stock: {stock}")
        time.sleep(0.1)  # Simulate some delay
        stock -= 1
    else:
        print(f"Thread {threading.current_thread().name} cannot sell stock. No stock left.")


threads = []
for i in range(100):
    t = threading.Thread(target=sell_stock, name=f"Seller-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Stock count after selling: ", stock)
print("All threads have finished executing.")    
