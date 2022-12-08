import itertools
import math

def findAllShortestRoutesFrom(start: str, target: str = None, graph: dict[str, list[str]] = None) -> tuple[dict[str, int], dict[str, list[str]], bool]:
    """Find the shortest route from a given node to all other nodes"""
    graphKeys = list(graph.keys())
    if start not in graphKeys or (target is not None and target not in graphKeys):
        return None, None, False
    out = {start: 0}
    routes = {start: [start]}
    visited = [start]
    checked = []
    while len(checked) < len(graphKeys):  # Go through all nodes
        recognised = 0
        for node in set(visited) - set(checked):  # Go through all visited nodes that haven't been checked (length of the neighbors is not known)
            for neighbour in graph[node]:  # For each neighbour of a node
                if neighbour not in visited:  # If the neighbour hasn't been visited yet
                    out[neighbour] = out[node] + 1  # Add one to the distance to the neighbour (it can be reached in one stop)
                    visited.append(neighbour)  # Add to the list of visited, but unchecked nodes
                    routes[neighbour] = routes[node] + [neighbour]  # Add to the route to get there
                    recognised += 1  # Add to the number of nodes added this loop. If this is 0, then no new nodes were added
            checked.append(node)  # Then mark the node as checked
            if target is not None and target in checked:  # If the target has been found, return
                return out, routes, False
        if recognised == 0:  # No nodes have been added, so there is no route to the node
            return out, routes, True
        recognised = 0  # Reset the number of nodes added
    return out, routes, False


def findWeightedShortestPathsFrom(start: str, target: str = None, graph: dict[str, dict[str, int]] = None) -> tuple[dict[str, int], dict[str, list[str]], bool]:
    """Find the shortest route from a given node to all other nodes, with each node having a cost associated with it"""
    graphKeys = list(graph.keys())
    if start not in graphKeys or (target is not None and target not in graphKeys):
        return None, None, False
    out = {start: 0}
    routes = {start: {"path": [start], "cost": 0}}
    currentLowestCost = {k: 10**100 for k in graphKeys}  # Set all costs to a very high number, so that the first node will always be chosen
    currentLowestCost[start] = 0
    checked = []
    while len(checked) < len(graphKeys):  # Go through all nodes
        # Find the node with the current lowest cost that is not in the checked list
        currentNode = min(set(graphKeys) - set(checked), key=lambda x: currentLowestCost[x])
        for neighbour in graph[currentNode]:  # For each neighbour of the current best node
            # Check if the cost of the current node + the cost of the neighbour is less than the current lowest cost of the neighbour
            if currentLowestCost[currentNode] + graph[currentNode][neighbour] < currentLowestCost[neighbour]:
                # Update the cost of the neighbour
                currentLowestCost[neighbour] = currentLowestCost[currentNode] + graph[currentNode][neighbour]
                # Update the route to the neighbour
                routes[neighbour] = {"path": routes[currentNode]["path"] + [neighbour], "cost": currentLowestCost[neighbour]}
        checked.append(currentNode)  # Then mark the node as checked
        if target is not None and target in checked:  # If the target has been found, return
            return currentLowestCost, routes, False
    return currentLowestCost, routes, False


def findShortestRouteBetween(start: str, end: str, data) -> tuple[int, list[str], bool]:
    """Returns shortest route (int), route (list[str]), and whether it failed (bool)"""
    if isDataWeighted(data):
        shortestPaths, routes, failed = findWeightedShortestPathsFrom(start, end, data)
    else:
        shortestPaths, routes, failed = findAllShortestRoutesFrom(start, end, data)
    if failed:
        return None, None, True
    return shortestPaths[end], routes[end], False


def isDataWeighted(data) -> bool:
    """Check if the data is weighted"""
    for entry in data:
        if isinstance(data[entry], dict):
            return True
    return False


def graphAll(data) -> dict[str, dict[str, int]]:
    # Check if the graph is weighted
    weighted = isDataWeighted(data)
    out = {}
    for entry in data:
        if weighted:
            out[entry] = findWeightedShortestPathsFrom(entry, graph=data)[0]
        else:
            out[entry] = findAllShortestRoutesFrom(entry, graph=data)[0]
    return out


def shortestPathVisitingAll(start: str | None, graph) -> tuple[int, list[str]]:
    """Find the shortest path visiting all nodes"""
    # Find the shortest path between every node and every other node
    shortestPaths = graphAll(graph)

    # Find the shortest path visiting all nodes
    shortestPath = 10**100
    shortestPathRoute = []
    if len(shortestPaths) >= 50:
        if input(f"This will take a long time ({math.factorial(len(shortestPaths))}). Continue? (y/n): ").lower() != "y":
            return None, None
    allPermutations = itertools.permutations(list(shortestPaths.keys()))
    # If a start node is given, only check permutations that start with that node
    for route in allPermutations:
        if start is not None and route[0] != start:
            continue
        path = 0
        for i in range(len(route) - 1):
            path += shortestPaths[route[i]][route[i + 1]]
        if path < shortestPath:
            shortestPath = path
            shortestPathRoute = route

    return shortestPath, shortestPathRoute
