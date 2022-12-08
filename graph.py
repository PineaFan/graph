import itertools
import math


class Path:
    def __init__(self, cost: int, route: list[str], start: str, end: str) -> None:
        self.cost = cost
        self.route = route
        self.start = start
        self.end = end


class Graph:
    def __init__(
        self,
        data: dict[str, dict[str, int] | list[str]]
    ) -> None:
        self.data = data
        self.weighted = self.isDataWeighted()
        self._shortestPaths = None

    def __getattribute__(self, name) -> any:
        if name == "shortestPaths":
            if self._shortestPaths is None:
                self._shortestPaths = self.findAllRoutes()
            return self._shortestPaths
        return super().__getattribute__(name)

    def isDataWeighted(self) -> bool:
        """Check if the data is weighted"""
        for entry in self.data:
            if isinstance(self.data[entry], dict):
                return True
        return False

    def findAllRoutesFrom(self, start: str, end: str | None = None) -> tuple[dict[str, int], dict[str, list[str]]]:
        """Find the shortest path from a node to all others"""
        # Check if it has already been calculated
        if self.shortestPaths is not None:
            if end is None:
                return self.shortestPaths[start]["cost"], self.shortestPaths[start]["route"]
            else:
                return self.shortestPaths[start]["cost"][end], self.shortestPaths[start]["route"][end]
        # Check if the graph is weighted
        if self.weighted:
            return self._findWeightedShortestPathsFrom(start, end)
        else:
            return self._findAllShortestRoutesFrom(start, end)

    def _findWeightedShortestPathsFrom(self, start: str, end: str | None = None) -> tuple[dict[str, int], dict[str, list[str]]]:
        """Find the shortest path from a node to all others"""
        # Set up the data
        currentLowestCost = {start: 0}
        routes = {start: [start]}
        checked = set()
        unchecked = {start: 0}

        # Loop until all nodes have been checked
        while unchecked:
            # Find the node with the lowest cost
            currentNode = min(unchecked, key=unchecked.get)
            currentCost = unchecked[currentNode]

            # Remove the node from the unchecked list
            del unchecked[currentNode]

            # Check all the nodes connected to the current node
            for node in self.data[currentNode]:
                # Calculate the cost of the new route
                newCost = currentCost + self.data[currentNode][node]

                # If the route is shorter than the current shortest route, update the shortest route
                if node not in currentLowestCost or newCost < currentLowestCost[node]:
                    currentLowestCost[node] = newCost
                    routes[node] = routes[currentNode] + [node]
                    unchecked[node] = newCost

            # Add the current node to the checked list
            checked.add(currentNode)

            # If the target has been found, return
            if end is not None and end in checked:
                return currentLowestCost, routes
        return currentLowestCost, routes

    def _findShortestPathsFrom(start: str, end: str | None = None) -> tuple[dict[str, int], dict[str, list[str]]]:
        """Find the shortest path from a node to all others"""
        # Set up the data
        currentLowestCost = {start: 0}
        routes = {start: [start]}
        checked = set()
        unchecked = {start: 0}

        # Loop until all nodes have been checked
        while unchecked:
            # Find the node with the lowest cost
            currentNode = min(unchecked, key=unchecked.get)
            currentCost = unchecked[currentNode]

            # Remove the node from the unchecked list
            del unchecked[currentNode]

            # Check all the nodes connected to the current node
            for node in self.data[currentNode]:
                # Calculate the cost of the new route
                newCost = currentCost + 1

                # If the route is shorter than the current shortest route, update the shortest route
                if node not in currentLowestCost or newCost < currentLowestCost[node]:
                    currentLowestCost[node] = newCost
                    routes[node] = routes[currentNode] + [node]
                    unchecked[node] = newCost

            # Add the current node to the checked list
            checked.add(currentNode)

            # If the target has been found, return
            if end is not None and end in checked:
                return currentLowestCost, routes
        return currentLowestCost, routes

    def findAllRoutes(self) -> dict[str, dict]:
        """Find all the shortest routes between all nodes"""
        out = {}
        for entry in self.data:
            if self.weighted:
                cost, route = self._findWeightedShortestPathsFrom(entry)
            else:
                cost, route = self._findShortestPathsFrom(entry)
            out[entry] = {"cost": cost, "route": route}
        self.shortestPaths = out
        return out

