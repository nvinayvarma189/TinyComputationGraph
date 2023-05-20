import sematic
from sematic.future import Future
import time

@sematic.func
def A(val: int) -> int:
    print("executing A")
    time.sleep(1)
    return val

@sematic.func
def B(a: int) -> int:
    print("executing B")
    time.sleep(1)
    return a

@sematic.func
def C(a: int) -> int:
    print("executing C")
    time.sleep(1)
    return a

@sematic.func
def D(a: int) -> int:
    print("executing D")
    time.sleep(1)
    return a

@sematic.func
def E(c: int, d: int) -> int:
    print("executing E")
    time.sleep(1)
    return c - d

@sematic.func
def F(b: int) -> int:
    print("executing F")
    time.sleep(1)
    return b * 10

@sematic.func
def G(f: int, c: int, e: int) -> int:
    print("executing G")
    time.sleep(1)
    return f + c - e

@sematic.func
def pipeline(a: int) -> int:
    aa = A(a)
    b = B(aa)
    c = C(aa)
    d = D(aa)
    e = E(c, d)
    f = F(b)
    g = G(f, c, e)
    return g

pipeline_future: Future = pipeline(10)
print(pipeline_future.resolve())