import networkx as nx

# Function to assign taskjobs to trucks using a greedy algorithm
def assign_tasks_greedy(trucks, taskjobs, graph, containers):
    matching_plan = {}
    available_trucks = set(trucks.keys())
    available_taskjobs = set(taskjob["TaskJobID"] for taskjob in taskjobs)

    while available_taskjobs:
        best_assignment = None
        min_cost = float('inf')
        
        for truck_id in available_trucks:
            for taskjob_id in available_taskjobs:
                taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
                truck_location = trucks[truck_id]
                
                if taskjob["TaskJobType"] == "Book_1":
                    container_locations = [container["Location"] for container in containers if container["isAvailable"]]
                    min_distance = float('inf')
                    for container_location in container_locations:
                        try:
                            distance = nx.dijkstra_path_length(graph, truck_location, container_location) + \
                                       nx.dijkstra_path_length(graph, container_location, taskjob["Locations"][1])
                            if distance < min_distance:
                                min_distance = distance
                        except nx.NetworkXNoPath:
                            continue
                    cost = min_distance
                else:
                    try:
                        cost = nx.dijkstra_path_length(graph, truck_location, taskjob["Locations"][0]) + \
                               nx.dijkstra_path_length(graph, taskjob["Locations"][0], taskjob["Locations"][1])
                    except nx.NetworkXNoPath:
                        cost = float('inf')
                
                if cost < min_cost:
                    min_cost = cost
                    best_assignment = (truck_id, taskjob_id)
        
        if best_assignment:
            truck_id, taskjob_id = best_assignment
            matching_plan[truck_id] = taskjob_id
            available_trucks.remove(truck_id)
            available_taskjobs.remove(taskjob_id)
    
    return matching_plan
