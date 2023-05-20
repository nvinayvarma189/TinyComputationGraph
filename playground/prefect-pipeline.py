from prefect import Flow, Parameter, task

@task()
def add2(a, b):
    return a+b

@task()
def add(a, b):
    return add2(a,b)

@task()
def subtract(a, b):
    return a - b

@task()
def multiply(a, b, c):
    return a * b * c

with Flow("Add One") as flow:
    a = b = c = d = 1
    add_future = add(a, b)
    subtract_future = subtract(c, d)
    multiply_future = multiply(add_future, c, subtract_future)


flow.visualize()
