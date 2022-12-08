from graph import findShortestRouteBetween, graphAll, shortestPathVisitingAll
import json
import time

with open('map.json') as f:
    stations = json.load(f)


# stations["Unknown"] = []

def getValidStation(prompt: str) -> str:
    valid = False
    while not valid:
        station = input(prompt)
        valid = station.lower() in [c.lower() for c in stations.keys()]
        if not valid:
            print('Invalid station')
    return station

s = time.time()
graphAll(stations)
print(f"Calculated all routes in {time.time() - s} seconds")
s = time.time()
cost, path = shortestPathVisitingAll(start="A", graph=stations)
print(f"Calculated shortest path visiting all stations in {time.time() - s} seconds")
print(f"Cost: {cost}, {' -> '.join(path)}")

while True:
    start, end = getValidStation('Start: '), getValidStation('End: ')
    distance, route, failed = findShortestRouteBetween(start, end, stations)
    if failed:
        print(f"There is no route between {start} and {end}")
        continue
    print(f'The shortest route between {start} and {end} is {distance} stops long')
    for i, stop in enumerate(route):
        print(f'[{i + 1}] {stop}')
