# run 4 simple functions in different threads

import time
import threading
from functools import wraps

class Future:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        pass

    def __call__(self, *args, **kwargs):
        print("execution for", self.func.__name__)
        return self.func(*args)

class Node:
    def __init__(self):
        pass
    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def outer(*args, **kwargs):
            return Future(func, *args, **kwargs)
        return outer

@Node()
def A(val):
    print("executing A")
    time.sleep(1)
    return val

@Node()
def B(a):
    print("executing B")
    time.sleep(1)
    return a

@Node()
def C(a):
    print("executing C")
    time.sleep(1)
    return a

@Node()
def D(a,b,c):
    print("executing D")
    time.sleep(1)
    return a + b + c


def main():
    results = [None]*4
    # print(type(A))
    # print(type(A()(1)))

    a = A(1)
    b = B(a)
    c = C(a)
    d = D(a, b, c)
    print(d)

    funcs = [a, b, c, d]
    threads = []
    for i, fn in enumerate(funcs):
        x = threading.Thread(target=fn, args=tuple(fn.args))
        if all(not isinstance(arg, Future) for arg in fn.args):
            x.start()
            threads.append(x)
        else:
            print("has unresolved args", fn.func.__name__)
    for x in threads:
        x.join()

start = time.time()
main()
print(time.time() - start)