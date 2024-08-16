import networkx as nx

# Function to assign taskjobs to trucks using a greedy algorithm
def assign_tasks_greedy(trucks, taskjobs, graph, containers):
    matching_plan = {}
    container_assignments = {}
    total_distance = 0
    available_trucks = set(trucks.keys())
    available_taskjobs = set(taskjob["TaskJobID"] for taskjob in taskjobs)
    used_containers = set()

    while available_taskjobs:
        best_assignment = None
        min_cost = float('inf')

        for truck_id in available_trucks:
            for taskjob_id in available_taskjobs:
                taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
                truck_location = trucks[truck_id]

                if taskjob["TaskJobType"] == "Book_1":
                    min_distance = float('inf')
                    best_container = None
                    for container in containers:
                        if container["isAvailable"] and container["ContNumber"] not in used_containers:
                            container_location = container["Location"]
                            try:
                                distance = nx.dijkstra_path_length(graph, truck_location, container_location) + \
                                           nx.dijkstra_path_length(graph, container_location, taskjob["Locations"][1])
                                if distance < min_distance:
                                    min_distance = distance
                                    best_container = container["ContNumber"]
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
                    best_assignment = (truck_id, taskjob_id, best_container if taskjob["TaskJobType"] == "Book_1" else None)

        if best_assignment:
            truck_id, taskjob_id, container_id = best_assignment
            matching_plan[truck_id] = taskjob_id
            total_distance += min_cost
            if container_id is not None:
                container_assignments[taskjob_id] = container_id
                used_containers.add(container_id)
            available_trucks.remove(truck_id)
            available_taskjobs.remove(taskjob_id)

    return matching_plan, container_assignments, total_distance
