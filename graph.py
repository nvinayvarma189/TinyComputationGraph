import networkx as nx
import matplotlib.pyplot as plt
import pydot

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

    def visualize_graph_nx(self):
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

        plt.savefig('images/nx_graph.png', format="PNG")

    def visualize_graph_pydot(self):
        graph = pydot.Dot(graph_type='digraph',fontsize = 20  )
        cluster_mapping = {}

        for cluster_name in self.dict:
            cluster_mapping = self.create_cluster(cluster_mapping, cluster_name)

            nested_futures = self.dict[cluster_name]["nested_futures"]
            if nested_futures:
                for nf in nested_futures:
                    cluster_mapping = self.create_cluster(cluster_mapping, nf)
                    cluster_mapping[cluster_name].add_subgraph(cluster_mapping[nf])


            parent_futures = self.dict[cluster_name]["parent_futures"]
            inputs = self.dict[cluster_name]["inputs"]
            if inputs and parent_futures:
                parent_future = parent_futures[0]
                for inp in inputs:
                    cluster_mapping = self.create_cluster(cluster_mapping, inp)
                    edge = pydot.Edge(cluster_mapping[inp], cluster_mapping[cluster_name], len=1.5)
                    cluster_mapping[parent_future].add_edge(edge)
                    cluster_mapping[parent_future].add_subgraph(cluster_mapping[inp])

        
        graph.add_subgraph(list(cluster_mapping.values())[0])
        graph.set_label("Static Graph View")
        graph.write("images/pydot_graph.png", prog = 'fdp',format = 'png')

    @staticmethod
    def create_cluster(cluster_mapping, cluster_name):
        if not cluster_name in cluster_mapping:
            cluster_mapping[cluster_name] = pydot.Cluster(cluster_name, compound=True, rankdir='TB')
            cluster_mapping[cluster_name].add_node(pydot.Node(cluster_name, style="invis"))
            cluster_mapping[cluster_name].set_label(cluster_name)
        return cluster_mapping

graph = Graph()
