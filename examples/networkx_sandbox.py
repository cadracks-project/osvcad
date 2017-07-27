# coding: utf-8

r"""Example of direct construction"""

import networkx as nx
import matplotlib.pyplot as plt

n1 = "n1"
n10 = "n10"
n11 = "n11"
n12 = "n12"
n101 = "n101"
n111 = "n111"
n121 = "n121"

A = nx.DiGraph()

# A.add_node(n1)
# A.add_node(n10)
# A.add_node(n11)

A.add_edge(n1, n10, object="n1 -> n10")
A.add_edge(n1, n11, object="n1 -> n11")
A.add_edge(n1, n12, object="n1 -> n12")

A.add_edge(n10, n101, object="n10 -> n101")
A.add_edge(n11, n111, object="n11 -> n111")
A.add_edge(n12, n121, object="n12 -> n121")
print(list(nx.bfs_edges(A, n1)))
print(nx.dfs_tree(A, n1))
print(A.number_of_nodes())
print(A.number_of_edges())

for node in A.nodes():
    out_edges_of_node = A.out_edges(node, data=True)
    # print("s--**--")
    # print(out_edges_of_node)
    # print("e--**--")

# A.show_plot()
# A.write_yaml("sample.yaml")
# A.write_json("sample.json")

val_map = {'A': 1.0,
           'D': 0.5714285714285714,
           'H': 0.0}

values = [val_map.get(node, 0.25) for node in A.nodes()]

pos = nx.spring_layout(A)
nx.draw_networkx_nodes(A, pos, cmap=plt.get_cmap('jet'),
                       node_color=values)
nx.draw_networkx_edges(A, pos, edgelist=A.edges(), edge_color='r',
                       arrows=True)
nx.draw_networkx_labels(A, pos)
nx.draw_networkx_edge_labels(A, pos)
plt.show()
