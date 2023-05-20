from node import node
import time

@node
def add(a, b):
    # time.sleep(2)
    return a + b

@node
def multiply(a, b):
    # time.sleep(2)
    return a * b

@node
def subtract(a, b):
    return a - b