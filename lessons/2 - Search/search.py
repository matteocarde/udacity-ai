from Graph import Graph, GraphNode

nodeG = GraphNode('G')
nodeR = GraphNode('R')
nodeA = GraphNode('A')
nodeP = GraphNode('P')
nodeH = GraphNode('H')
nodeS = GraphNode('S')

graph = Graph([nodeG, nodeR, nodeA, nodeP, nodeH, nodeS])
graph.add_edge(nodeG, nodeR)
graph.add_edge(nodeA, nodeR)
graph.add_edge(nodeA, nodeG)
graph.add_edge(nodeR, nodeP)
graph.add_edge(nodeH, nodeG)
graph.add_edge(nodeH, nodeP)
graph.add_edge(nodeS, nodeR)


def bfs(root_node: GraphNode, search_value: str):
    seen = set()
    frontier = [root_node]

    while len(frontier) > 0:
        node: GraphNode = frontier.pop()
        seen.add(node)

        if node.get_label() == search_value:
            return node

        for neighbour in node.get_neighbors():
            if neighbour not in seen:
                frontier.append(neighbour)

    return False


def dfs_deep(node: GraphNode, search_value: str, seen: set):

    seen.add(node)
    if node.get_label() == search_value:
        return node

    for neighbour in node.get_neighbors():
        if neighbour not in seen:
            found = dfs_deep(neighbour, search_value, seen)
            if found:
                return found

    return False


def dfs(root_node: GraphNode, search_value: str):
    seen = set()
    return dfs_deep(root_node, search_value, seen)


''' TO DO: Find the shortest path from the source node to every other node in the given graph '''


def dijkstra(graph: Graph, source: GraphNode):
    # Declare and initialize result, unvisited, and path
    result = dict()
    result[source.get_label()] = 0

    unvisited = set(graph.node_list)

    # As long as unvisited is non-empty
    while unvisited:
        # 1. Find the unvisited node having smallest known distance from the source node.

        # 2. For the current node, find all the unvisited neighbours. For this, you have calculate the distance of each unvisited neighbour.

        # 3. If the calculated distance of the unvisited neighbour is less than the already known distance in result dictionary, update the shortest distance in the result dictionary.

        # 4. If there is an update in the result dictionary, you need to update the path dictionary as well for the same key.

        # 5. Remove the current node from the unvisited set.

    return result

assert nodeA == bfs(nodeS, 'A')
assert nodeS == bfs(nodeP, 'S')
assert nodeR == bfs(nodeH, 'R')

assert nodeA == dfs(nodeS, 'A')
assert nodeS == dfs(nodeP, 'S')
assert nodeR == dfs(nodeH, 'R')

