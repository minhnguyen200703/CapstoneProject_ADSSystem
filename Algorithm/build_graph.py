import networkx as nx

# Build the graph using NetworkX
def build_graph(locations, distances):
    G = nx.Graph()
    
    # Add nodes with location details
    for location in locations:
        loc_id = location["LocationID"]
        G.add_node(loc_id, **location)
    
    # Add edges with distances
    for distance in distances:
        loc1, loc2, dist = distance["LocationFromID"], distance["LocationToID"], float(distance["DistanceKm"])
        G.add_edge(loc1, loc2, weight=dist)
    
    return G

def dijkstra(G, start, end):
    return nx.dijkstra_path_length(G, start, end)