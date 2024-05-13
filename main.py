from code_1 import Vertice, Graph, Implication
from pyvis.network import Network
import networkx as nx
from collections import defaultdict

COLORS = {1:"red", 2:"blue", 3:"green"}

if __name__ == '__main__':
    vis_graph = defaultdict(list)
    graph = Graph()
    graph.read_file('graph.csv')
    imp = Implication(graph.graph)
    imp.recolor_graph()
    print(graph.graph)

    pairs = [(x.name, y.name) for x in graph.graph for y in graph.graph[x]]
    colors = {x.name: COLORS[x.color] for x in imp.result}

    nt = Network(notebook=True, cdn_resources="remote",
                 bgcolor="#222222",
                 font_color="white",
                 height="1000px",
                 width="100%",)
    for i in graph.graph:
        nt.add_node(i.name, label=f"v_{i.name}", color = colors[i.color], shape='dot')
    for i in pairs:
        nt.add_edge(*i, color="white")

    nt.show('nx.html')

