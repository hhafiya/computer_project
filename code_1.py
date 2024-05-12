"""
2-SAT problem
Coloring graph in 3 colors
"""
import csv
class Vertice:
    """
    Class for vertices of the graph
    """
    def __init__(self, name, color):
        """
        Constructor of the class
        :param name: name of the vertice
        :param color: color of the vertice
        """
        self.name = name
        self.color = color+1

    def __repr__(self):
        """
        Method for representation of the object
        :return: string representation of the object
        """
        return f"v_{self.name}"

    def __eq__(self, other):
        """
        Method for comparing two objects
        :param other: object for comparing
        :return: boolean value of comparing
        """
        return self.name == other.name and self.color == other.color

    def __hash__(self):
        """
        Method for hashing object
        :return: hash value of the object
        """
        return hash((self.name, self.color))
    
class Graph:
    """
    Class for graph
    """
    def __init__(self):
        """
        Constructor of the class
        """
        self.vertices = {}
    
    def read_file(self, filename):
        """
        Method for reading data from file
        """
        with open(filename, 'r', encoding = 'utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                u, v, color_u, color_v = row
                u_node = Vertice(int(u), int(color_u))
                v_node = Vertice(int(v), int(color_v))
                if u_node not in self.vertices:
                    self.vertices[u_node] = []
                if v_node not in self.vertices:
                    self.vertices[v_node] = []
                self.vertices[u_node].append(v_node)
                self.vertices[v_node].append(u_node)
        
class Implication:
    def __init__(self, graph):
        self.graph = graph
        self.cnf = []
        self.imp_graph = {}

    def generate_cnf(self):
        for node in self.graph:
            possible_col = [1, 2, 3]
            possible_col.remove(node.color)
            self.cnf.append(tuple([(node, new_col) for new_col in possible_col]))
            self.cnf.append(tuple([(node, -new_col) for new_col in possible_col]))
            for neighbour in self.graph[node]:
                for new_col in possible_col:
                    if neighbour.color != new_col and \
                        tuple([(neighbour, -new_col), (node, -new_col)]) not in self.cnf:
                        self.cnf.append(tuple([(node, -new_col), (neighbour, -new_col)]))

    def generate_implication_graph(self):
        for tupl in self.cnf:
            first_node = tupl[0]
            second_node = tupl[1]
            new_first = (first_node[0], -first_node[1])
            new_second = (second_node[0], -second_node[1])
            if new_first not in self.imp_graph:
                self.imp_graph[new_first] = []
            if new_second not in self.imp_graph:
                self.imp_graph[new_second] = []
            self.imp_graph[new_first].append(second_node)
            self.imp_graph[new_second].append(first_node)

graph = Graph()
graph.read_file('graph.csv')
imp = Implication(graph.vertices)
imp.generate_cnf()
print(imp.cnf)
imp.generate_implication_graph()
print(len(imp.imp_graph))

# print(graph.vertices)