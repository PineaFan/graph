from graph import findWeightedShortestPathsFrom, graphAll, shortestPathVisitingAll
import json
import time

with open('houses.json') as f:
    houses = json.load(f)

s = time.time()
graphAll(houses)
print(f"Calculated all routes in {time.time() - s} seconds")
s = time.time()
cost, path = shortestPathVisitingAll(start="A", graph=houses)
print(f"Calculated shortest path visiting all houses in {time.time() - s} seconds")
print(f"Cost: {cost}, {' -> '.join(path)}")


while True:
    start, end = input('Start: '), input('End: ')
    distance, route, failed = findWeightedShortestPathsFrom(start, end, graph=houses)
    if failed:
        print(f"There is no route between {start} and {end}")
        continue
    print(f'The shortest route between {start} and {end} is {distance} stops long')
    for i, node in enumerate(route[end]["path"]):
        print(f'[{i + 1}] {node}')

