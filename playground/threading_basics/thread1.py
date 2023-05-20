# run 4 simple functions in different threads

import time
import threading

def A():
    time.sleep(1)

def B():
    time.sleep(1)

def C():
    time.sleep(1)

def D():
    time.sleep(1)

def main():
    funcs = [A, B, C, D]
    threads = []
    for fn in funcs:
        x = threading.Thread(target=fn)
        x.start()
        threads.append(x)

    for x in threads:
        x.join()

    # A()
    # B()
    # C()
    # D()

start = time.time()
main()
print(time.time() - start)