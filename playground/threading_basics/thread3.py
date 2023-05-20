# run 4 simple functions in different threads

import time
import inspect
import threading
from functools import wraps
from collections import defaultdict

class Future:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.name = func.__name__
        self.args = args
        self.dict_args = self.get_args_as_dict()
        self.resolved_args = self.get_resolved_args()
        self.parent_futures = []
        self.child_futures = []

    def get_resolved_args(self):
        return [arg for arg in self.args if not isinstance(arg, Future)]

    def get_args_as_dict(self):
        arg_names = inspect.getfullargspec(self.func).args
        return dict(zip(arg_names, self.args))


    def __call__(self):

        self.resolved_args = self.resolved_args[::-1]
        return self.func(*self.resolved_args)

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
    return 10

@Node()
def C(a):
    print("executing C")
    time.sleep(1)
    return 3

@Node()
def D(b,c):
    print("executing D")
    time.sleep(1)
    return b - c

def pf(stack):
    for s in stack:
        print(s.func.__name__, end=" ")
    print()

def main():
    a = A(1)
    b = B(a)
    c = C(a)
    d = D(b, c)

    stack = [d]
    executed = {}

    while stack:
        fn = stack[-1]
        if (len(fn.args) == len(fn.resolved_args)):
            fn2 = stack.pop()
            if not fn2.name in executed:
                value = fn2()
                executed[fn2.name] = value
            for pf_ in fn2.parent_futures:
                pf_.resolved_args.append(executed[fn2.name])
        else:
            unresolved_args = [arg for arg in fn.args if arg not in fn.resolved_args]
            for ua in unresolved_args:
                # if ua not in stack:
                stack.append(ua)
                ua.parent_futures.append(fn)
    print(value)

start = time.time()
main()
print(time.time() - start)