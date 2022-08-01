from node import Node
from future import Future
from graph import graph

@Node(verbose=False)
def add2(a, b):
    return a+b

@Node(verbose=False)
def add(a, b):
    return add2(a,b)

@Node(verbose=False)
def subtract(a, b):
    return a - b

@Node(verbose=False)
def multiply(a, b, c):
    return a * b * c

@Node(verbose=False)
def pipeline(a, b, c, d):
    add_future = add(a, b)
    subtract_future = subtract(c, d)
    multiply_future = multiply(add_future, c, subtract_future)
    return multiply_future

pipeline_future: Future = pipeline(10, 2, 5, 6)
print(graph)
# print(pipeline_future.resolve())
# print(graph)
# graph.visualize()