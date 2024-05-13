"""
2-SAT problem
Coloring graph in 3 colors
"""
import csv
from collections import defaultdict
import enum
COLORS = {1:'blue', 2:'green', 3:'red'}



class Vertice:
    """
    Class for vertices of the graph
    """
    def __init__(self, name, color, start_color = None):
        """
        Constructor of the class
        :param name: name of the vertice
        :param color: color of the vertice
        """
        self.name = name
        self.color = color+1
        self.visited = False
        self._start_color = start_color or self.color

    def to_tuple(self):
        return (self.name, self.color)

    def __repr__(self):
        """
        Method for representation of the object
        :return: string representation of the object
        """
        #return f"(v_{self.name}: color: {COLORS[self.color]}; start_color: {COLORS[self._start_color]})\n"
        return  f"(v_{self.name} color: {self.color}; start_color: {self._start_color})"

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
        self.result = defaultdict(list)
    
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
        self.scc = []
        self.result = []


    def generate_cnf(self):
        for node in self.graph:
            possible_col = [1, 2, 3]
            possible_col.remove(node.color)
            self.cnf.add(tuple([Vertice(node.name, new_col-1, node._start_color) for new_col in possible_col]))
            self.cnf.add(tuple([Vertice(node.name, -new_col-1, node._start_color) for new_col in possible_col]))
            for neighbour in self.graph[node]:
                for new_col in possible_col:
                    if neighbour.color != new_col and tuple([Vertice(neighbour.name, -new_col-1, node._start_color), Vertice(node.name, -new_col-1, node._start_color)]) not in self.cnf:
                        self.cnf.add(tuple([Vertice(node.name, -new_col-1, node._start_color), Vertice(neighbour.name, -new_col-1, node._start_color)]))

        self.cnf = sorted(self.cnf)

    def generate_implication_graph(self):
        for tup in self.cnf:
            first_node = tup[0]
            second_node = tup[1]
            new_first = (Vertice(first_node.name, -first_node.color-1, first_node._start_color))
            new_second = (Vertice(second_node.name, -second_node.color-1, second_node._start_color))
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

    def tarjan(self):
        result = []
        order = []

        for vertex in sorted(self.imp_graph.keys(), reverse=True):
            order.extend(self.dfs(vertex, self.imp_graph))

        new_visited = []
        for vertex in reversed(order):
            if vertex not in new_visited:
                component = self.dfs(vertex, self.reverse_graph)
                result.append(component)
                new_visited.extend(component)

        return result

    def recolor_graph(self):

        self.generate_cnf()
        self.generate_implication_graph()
        self.create_reverse_graph()
        self.scc = self.tarjan()
        for connections in reversed(self.scc):
            if all([False for x in connections if Vertice(x.name, -x.color) not in connections]):
                return "No solution"
            for vertice in reversed(connections):
                if len(self.result) == len(self.graph):
                    break
                if vertice.color > 0 and vertice not in self.result:
                    if not any(v.name == vertice.name for v in self.result):
                        self.result.append(vertice)
                elif vertice.color < 0:
                    new_vertice = Vertice(vertice.name, int(({1 , 2, 3} - {abs(vertice.color), vertice._start_color}).pop())-1, vertice._start_color)
                    if not any(v.name == new_vertice.name for v in self.result):
                        self.result.append(new_vertice)
        return
