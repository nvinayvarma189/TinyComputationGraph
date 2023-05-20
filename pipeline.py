import argparse

from node import Node
from future import Future
from graph import graph

@Node()
def _add(a, b):
    return a + b

@Node()
def add(a, b):
    return _add(a, b)

@Node()
def subtract(a, b):
    return a - b

@Node()
def multiply(a, b, c):
    return a * b * c

@Node()
def pipeline(a, b, c, d):
    add_future = add(a, b)
    subtract_future = subtract(c, d)
    multiply_future = multiply(add_future, c, subtract_future)
    return multiply_future


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-gv','--graph-viz', help='Type of grpah visualisation to use. Either "nx" or "pydot"', default="pydot")
    args = vars(parser.parse_args())

    pipeline_future: Future = pipeline(10, 2, 5, 6)
    print("\nResult after executing the computation graph: ", pipeline_future.resolve())


    graph_viz_type = args['graph_viz']
    if graph_viz_type == "pydot":
        graph.visualize_graph_pydot()
    elif graph_viz_type == "nx":
        graph.visualize_graph_nx()
    else:
        raise NotImplemented(f"Graph type {args['graph-viz']} not implemented yet.")
    
    print(f"\nSaved the graph visualisation({graph_viz_type}) of the computation graph to the disk!")