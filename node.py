from future import Future
from graph import graph
from functools import wraps


class Node:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def outer(*args, **kwargs):
            if self.verbose:
                print("Wrapping the function to create a node: ", func.__name__)
            graph.add_node(func.__name__)
            return Future(func, *args, **kwargs)

        return outer