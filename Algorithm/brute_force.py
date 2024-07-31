import itertools
import networkx as nx
import time

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    for truck_id, taskjob_id in plan.items():
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
            total_distance += min_distance
        else:
            try:
                distance = nx.dijkstra_path_length(graph, truck_location, taskjob["Locations"][0]) + \
                           nx.dijkstra_path_length(graph, taskjob["Locations"][0], taskjob["Locations"][1])
            except nx.NetworkXNoPath:
                distance = float('inf')
            total_distance += distance

    return total_distance

# Function to generate all possible matching plans
def generate_matching_plans(trucks, taskjobs):
    truck_ids = list(trucks.keys())
    taskjob_ids = [taskjob["TaskJobID"] for taskjob in taskjobs]
    if len(truck_ids) < len(taskjob_ids):
        taskjob_ids = taskjob_ids[:len(truck_ids)]
    return list(itertools.permutations(truck_ids, len(taskjob_ids)))

# Brute force algorithm function
def brute_force(trucks, taskjobs, graph, containers):
    all_plans = generate_matching_plans(trucks, taskjobs)
    time.sleep(0.05)
    min_distance = float('inf')
    best_plan = None

    for plan in all_plans:
        matching_plan = dict(zip(plan, [taskjob["TaskJobID"] for taskjob in taskjobs]))
        total_distance = calculate_total_distance(matching_plan, trucks, taskjobs, graph, containers)
        if total_distance < min_distance:
            min_distance = total_distance
            best_plan = matching_plan

    return best_plan, min_distance
