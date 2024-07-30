import heapq

def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances[end]
