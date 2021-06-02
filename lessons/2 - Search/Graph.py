class GraphNode(object):
    def __init__(self, label):
        self.__label = label
        self.__neighbours = []

    def add_neighbour(self, neighbour):
        self.__neighbours.append(neighbour)

    def delete_neighbour(self, neighbour):
        if neighbour in self.__neighbours:
            self.__neighbours.remove(neighbour)

    def get_neighbors(self):
        return self.__neighbours

    def get_label(self):
        return self.__label


class Graph(object):
    def __init__(self, node_list: list):
        self.node_list = node_list

    def add_edge(self, node_a: GraphNode, node_b: GraphNode):
        if node_a in self.node_list and node_b in self.node_list:
            node_a.add_neighbour(node_b)
            node_b.add_neighbour(node_a)

    def remove_edge(self, node_a: GraphNode, node_b: GraphNode):
        if node_a in self.node_list and node_b in self.node_list:
            node_a.delete_neighbour(node_b)
            node_b.delete_neighbour(node_a)


