import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.dict = {}
        self.root_node = None

    def add_edge(self, from_future, to_future, key):
        from_future = from_future.func.__name__
        to_future = to_future.func.__name__
        self.dict[from_future][key].append(to_future)
    
    def add_node(self, node):
        self.dict[node] = {"parent_futures": [], "nested_futures": [], "inputs": [], "outputs": []}

    def get_nodes(self):
        return list(self.dict.keys())

    def set_root_node(self, node):
        self.root_node = node.func.__name__

    def list_edges(self):
        return [(from_future, to_future) for from_future, to_futures in self.dict.items() for to_future in to_futures]

    def __repr__(self) -> str:
        return str(self.dict)

    def visualize(self):
        G = nx.DiGraph()

        parent_nested_edges = []
        input_output_edges = []
        for from_future, to_futures in self.dict.items():
            G.add_node(from_future)
            for to_future in to_futures["parent_futures"]:
                parent_nested_edges.append((to_future, from_future))
            for inputs in to_futures["inputs"]:
                input_output_edges.append((inputs, from_future))

        labels = {}
        for node in G.nodes():
            labels[node] = node

        nx.draw_networkx_edges(G, pos=nx.circular_layout(G), edgelist=parent_nested_edges, edge_color="tab:red")
        nx.draw_networkx_edges(G, pos=nx.circular_layout(G), edgelist=input_output_edges, edge_color="tab:gray")
        nx.draw_networkx_nodes(G, pos=nx.circular_layout(G), nodelist=self.get_nodes(), node_color="tab:blue")
        nx.draw_networkx_nodes(G, pos=nx.circular_layout(G), nodelist=[self.root_node], node_color="tab:green")
        nx.draw_networkx_labels(G, pos=nx.circular_layout(G), labels=labels)

        plt.show()
    
graph = Graph()
