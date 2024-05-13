from code_1 import Vertice, Graph, Implication
from pyvis.network import Network

COLORS = {1: "red", 2: "blue", 3: "green"}

def create_graph(path:str):

    graph = Graph()
    graph.read_file(path)
    imp = Implication(graph.graph)
    imp.recolor_graph()

    print(imp.result)
    return graph, imp.result


def visualize(graph: Graph, result: list[Vertice]):

    pairs = [(x.name, y.name) for x in graph.graph for y in graph.graph[x]]

    nt = Network(notebook=True, cdn_resources="remote",
                 bgcolor="#222222",
                 font_color="white",
                 height="1000px",
                 width="100%", )


    for node in result:
        nt.add_node(node.name, label=f"v_{node.name}", color=COLORS[node.color], shape='dot')

    for edge in pairs:
        nt.add_edge(*edge, color="white")

    nt.show('nx.html')


if __name__ == '__main__':
    visualize(*create_graph('graph.csv'))
