import itertools
import networkx as nx

# Function to find the k nearest trucks to each taskjob
def find_k_nearest_trucks(trucks, taskjobs, graph, containers):
    nearest_trucks = {}
    for taskjob in taskjobs:
        distances_to_trucks = []
        for truck_id, truck_location in trucks.items():
            if taskjob["TaskJobType"] == "Book_1":
                # Find nearest truck and container pair
                min_distance = float('inf')
                best_container = None
                for container in containers:
                    if container["isAvailable"]:
                        container_location = container["Location"]
                        try:
                            distance = nx.dijkstra_path_length(graph, truck_location, container_location) + \
                                       nx.dijkstra_path_length(graph, container_location, taskjob["Locations"][1])
                            if distance < min_distance:
                                min_distance = distance
                                best_container = container["ContNumber"]
                        except nx.NetworkXNoPath:
                            continue
                distances_to_trucks.append((truck_id, min_distance, best_container))
            else:
                try:
                    distance = nx.dijkstra_path_length(graph, truck_location, taskjob["Locations"][0]) + \
                               nx.dijkstra_path_length(graph, taskjob["Locations"][0], taskjob["Locations"][1])
                except nx.NetworkXNoPath:
                    distance = float('inf')
                distances_to_trucks.append((truck_id, distance, None))

        distances_to_trucks.sort(key=lambda x: x[1])
        nearest_trucks[taskjob["TaskJobID"]] = distances_to_trucks

    return nearest_trucks

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    container_assignments = {}
    for truck_id, taskjob_id in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]

        if taskjob["TaskJobType"] == "Book_1":
            container_locations = [container["Location"] for container in containers if container["isAvailable"]]
            min_distance = float('inf')
            best_container = None
            for container_location in container_locations:
                try:
                    distance = nx.dijkstra_path_length(graph, truck_location, container_location) + \
                               nx.dijkstra_path_length(graph, container_location, taskjob["Locations"][1])
                    if distance < min_distance:
                        min_distance = distance
                        best_container = next(container["ContNumber"] for container in containers if container["Location"] == container_location)
                except nx.NetworkXNoPath:
                    continue
            total_distance += min_distance
            container_assignments[taskjob_id] = best_container
        else:
            try:
                distance = nx.dijkstra_path_length(graph, truck_location, taskjob["Locations"][0]) + \
                           nx.dijkstra_path_length(graph, taskjob["Locations"][0], taskjob["Locations"][1])
            except nx.NetworkXNoPath:
                distance = float('inf')
            total_distance += distance

    return total_distance, container_assignments

# Function to find the best matching plan
def find_best_matching_plan(trucks, taskjobs, graph, containers):
    nearest_trucks = find_k_nearest_trucks(trucks, taskjobs, graph, containers)

    taskjob_ids = list(nearest_trucks.keys())
    truck_ids = list(trucks.keys())

    best_plan = None
    best_container_plan = None
    min_distance = float('inf')

    # Generate all possible matching plans
    for perm in itertools.permutations(truck_ids, len(taskjob_ids)):
        plan = dict(zip(perm, taskjob_ids))
        total_distance, container_assignments = calculate_total_distance(plan, trucks, taskjobs, graph, containers)
        if total_distance < min_distance:
            min_distance = total_distance
            best_plan = plan
            best_container_plan = container_assignments

    return best_plan, best_container_plan, min_distance
