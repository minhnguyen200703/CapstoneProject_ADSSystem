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
        loc1 = distance["LocationFromID"]
        loc2 = distance["LocationToID"]
        dist = float(distance["DistanceKm"])  # Ensure distance is a float
        
        # Ensure both locations are in the graph before adding the edge
        if loc1 in G and loc2 in G:
            G.add_edge(loc1, loc2, weight=dist)
        else:
            print(f"Warning: Locations {loc1} or {loc2} not found in the graph nodes.")
    
    return G

