from node import node, all_nodes, edges
import time
from tasks import add, multiply, subtract


@node
def pipeline(a, b, c, d):
    start = time.time()
    add_result = add(a, b)
    multiply_result = multiply(c, d)
    subtract_result = subtract(multiply_result, add_result)
    end = time.time()
    print(f"Pipeline took {end - start} seconds")
    return subtract_result

print(all_nodes)
print(edges)
print(pipeline(1, 2, 3, 4))