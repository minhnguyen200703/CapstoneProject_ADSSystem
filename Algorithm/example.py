import networkx as nx

# Build the graph using NetworkX with additional conditions
def build_graph_with_conditions(locations, distances):
    G = nx.Graph()
    
    # Add nodes with location details
    for location in locations:
        loc_id = location["LocationID"]
        G.add_node(loc_id, **location)
    
    # Add edges with distances and other factors
    for distance in distances:
        loc1 = distance["LocationFromID"]
        loc2 = distance["LocationToID"]
        dist = float(distance["DistanceKm"])  # Original distance
        
        urgency_weight = distance.get("UrgencyWeight", 1) 
        driver_weight = distance.get("DriverWeight", 1)  

        w_distance = 0.5
        w_urgency = 0.3
        w_driver = 0.2
        
        # Calculate the total weight considering all factors
        total_weight = w_distance * dist + w_urgency * urgency_weight + w_driver * driver_weight
        
        if loc1 in G and loc2 in G:
            G.add_edge(loc1, loc2, weight=total_weight, distance=dist, urgency_weight=urgency_weight, driver_weight=driver_weight)
        else:
            print(f"Warning: Locations {loc1} or {loc2} not found in the graph nodes.")
    
    return G
