def build_graph(distances):
    graph = {}
    for distance in distances:
        loc1, loc2, dist = distance["LocationFromID"], distance["LocationToID"], float(distance["DistanceKm"])
        if loc1 not in graph:
            graph[loc1] = {}
        if loc2 not in graph:
            graph[loc2] = {}
        graph[loc1][loc2] = dist
        graph[loc2][loc1] = dist
    return graph
