import sematic
from sematic.future import Future
import time

@sematic.func
def add(a: int, b: int) -> int:
    time.sleep(1)
    return a + b

@sematic.func
def sub(a: int, b: int) -> int:
    time.sleep(1)
    return a - b

@sematic.func
def mul(a: int, b: int) -> int:
    return a * b

@sematic.func
def pipeline(a: int, b: int) -> int:
    add_f = add(a, b)
    sub_f = sub(a, b)
    mul_f = mul(add_f, sub_f)
    return mul_f

start = time.time()
pipeline_f: Future = pipeline(1, 2)
print(pipeline_f.resolve(tracking=False))
end = time.time()
print(f"pipeline: {end - start}")