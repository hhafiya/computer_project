"""
2-SAT problem
Coloring graph in 3 colors
"""
import csv
from collections import defaultdict
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
        self.visited = False

    def __repr__(self):
        """
        Method for representation of the object
        :return: string representation of the object
        """
        return f"v_{self.name} {self.color}"

    def __eq__(self, other):
        """
        Method for comparing two objects
        :param other: object for comparing
        :return: boolean value of comparing
        """
        return self.name == other.name and self.color == other.color

    def __gt__(self, other):
        return self.name > other.name

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
        self.graph = defaultdict(list)
    
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
                self.graph[u_node].append(v_node)
                self.graph[v_node].append(u_node)


class Implication:
    def __init__(self, graph):
        self.graph = graph
        self.cnf = set()
        self.imp_graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)

    def old_cnf(self):
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

    def generate_cnf(self):
        for node in self.graph:
            possible_col = [1, 2, 3]
            possible_col.remove(node.color)
            self.cnf.add(tuple([Vertice(node.name, new_col-1) for new_col in possible_col]))
            self.cnf.add(tuple([Vertice(node.name, -new_col-1) for new_col in possible_col]))
            for neighbour in self.graph[node]:
                for new_col in possible_col:
                    if neighbour.color != new_col and tuple([Vertice(neighbour.name, -new_col-1), Vertice(node.name, -new_col-1)]) not in self.cnf:
                        self.cnf.add(tuple([Vertice(node.name, -new_col-1), Vertice(neighbour.name, -new_col-1)]))

        self.cnf = sorted(self.cnf)

    def generate_implication_graph(self):
        for tup in self.cnf:
            first_node = tup[0]
            second_node = tup[1]
            new_first = (Vertice(first_node.name, -first_node.color-1))
            new_second = (Vertice(second_node.name, -second_node.color-1))
            self.imp_graph[new_first].append(second_node)
            self.imp_graph[new_second].append(first_node)

    def create_reverse_graph(self):
        for vert in self.imp_graph:
            for node in self.imp_graph[vert]:
                self.reverse_graph[node] += [vert]

    def dfs(self, start_vertex, graph):
        visited = []
        stack = [start_vertex]
        visited_path = []

        while stack:
            current_vertex = stack[-1]
            clear_stack = True

            if current_vertex not in visited:
                visited.append(current_vertex)
                visited_path.append(current_vertex)

            remaining_adjacents = [adj for adj in sorted(graph[current_vertex]) if adj not in visited]

            if remaining_adjacents:
                stack.append(remaining_adjacents[0])
                clear_stack = False

            if clear_stack:
                stack.pop()

        return visited_path

    def scc(self):
        result = []
        visited = []
        order = []

        for vertex in sorted(self.imp_graph.keys(), reverse=True):
            if vertex not in visited:
                order.extend(self.dfs(vertex, self.imp_graph))

        new_visited = []
        for vertex in reversed(order):
            if vertex not in new_visited:
                component = self.dfs(vertex, self.reverse_graph)
                result.append(component)
                new_visited.extend(component)

        return result



graph = Graph()
graph.read_file('graph.csv')
imp = Implication(graph.graph)
imp.generate_cnf()
print(len(imp.cnf))
print(imp.cnf)
imp.generate_implication_graph()
print((imp.imp_graph))
imp.create_reverse_graph()
print(imp.reverse_graph)
print(imp.scc())
