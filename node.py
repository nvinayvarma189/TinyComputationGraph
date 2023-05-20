from future import Future
from graph import graph

class Node:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __call__(self, func, *args, **kwargs):
        def outer(*args, **kwargs):
            if self.verbose:
                print('outer()')
            graph.add_node(func.__name__)
            return Future(func, *args, **kwargs)

        return outer