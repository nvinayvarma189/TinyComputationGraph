# run 4 simple functions in different threads

import time
import inspect
import threading
from functools import wraps

executed = {}

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

        new_args = []
        for arg in self.args:
            if isinstance(arg, Future):
                new_args.append(executed[arg.name])
            else:
                new_args.append(arg)
        result = self.func(*new_args)
        executed[self.name] = result
        return result

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
    return a - 2

@Node()
def D(a):
    print("executing D")
    time.sleep(1)
    return a - 2

@Node()
def E(c, d):
    print("executing E")
    time.sleep(1)
    return c - d

@Node()
def F(b):
    print("executing F")
    time.sleep(1)
    return b * 10

@Node()
def G(f, c, e):
    print("executing G")
    time.sleep(1)
    return f + c - e


def pf(stack):
    for s in stack:
        print(s.func.__name__, end=" ")
    print()

def main():
    aa = A(10)
    b = B(aa)
    c = C(aa)
    d = D(aa)
    e = E(c, d)
    f = F(b)
    g = G(f, c, e)

    stack = [g]
    threads = []
    while stack:
        last_fn = stack[-1]
        if all((not isinstance(arg, Future) or (arg.name in executed) for arg in last_fn.args)):
            popped_fn = stack.pop()
            print("popped1", popped_fn.name)
            if not popped_fn.name in executed:
                x = threading.Thread(target=popped_fn)
                x.start()
                threads.append(x)
        else:
            unresolved_args = [arg for arg in last_fn.args if arg not in last_fn.resolved_args]
            for ua in unresolved_args:
                stack.append(ua)

        pf(stack)
    
    for thread in threads:
        thread.join()

    print(executed[g.name])
start = time.time()
main()
print(time.time() - start)