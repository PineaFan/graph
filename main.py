from graph import Graph
import json

with open('old/houses.json') as f:
    houses = json.load(f)

graph = Graph(houses)

print(graph.findAllRoutesFrom("A", "F"))