import threading


def <function_name>():
    <function_body>


t1 = threading.Thread(target=<function_name>)
t2 = threading.Thread(target=<function_name>)

t1.start()
t2.start()

t1.join()
t2.join()

