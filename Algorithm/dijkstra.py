import networkx as nx

def dijkstra(G, start, end):
    try:
        # Ensure nodes exist in the graph
        if start not in G or end not in G:
            raise ValueError(f"Nodes {start} or {end} do not exist in the graph.")
        
        # Calculate the shortest path length using Dijkstra's algorithm
        shortest_distance = nx.dijkstra_path_length(G, source=start, target=end)
        return shortest_distance
    except nx.NetworkXNoPath:
        print(f"No path exists between {start} and {end}.")
        return float('inf')
    except nx.NodeNotFound:
        print(f"One or both of the nodes {start}, {end} do not exist in the graph.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None