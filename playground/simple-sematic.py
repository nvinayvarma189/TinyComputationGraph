import sematic
from sematic.future import Future

@sematic.func
def damn(a: int, b: int) -> int:
    return a + b

@sematic.func
def add(ab: int, b: int) -> int:
    d = damn(ab, b)
    return d

@sematic.func
def subtract(a: int, b: int) -> int:
    return a - b

@sematic.func
def multiply(a: int, b: int, c: int) -> int:
    return a * b * c

@sematic.func
def pipeline(a: int, bb:int , c: int, d: int) -> int:
    aa = a + 10
    add_future = add(aa, bb)
    subtract_future = subtract(c, d)
    multiply_future = multiply(add_future, c, subtract_future)
    return multiply_future

pipeline_future: Future = pipeline(10, 2, 5, 6)
pipeline_future.resolve()