import random
import math
import networkx as nx

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    container_assignments = {}
    used_containers = set()
    for truck_id, taskjob_id in plan.items():
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
            total_distance += min_distance
            container_assignments[taskjob_id] = best_container
            used_containers.add(best_container)
        else:
            try:
                distance = nx.dijkstra_path_length(graph, truck_location, taskjob["Locations"][0]) + \
                           nx.dijkstra_path_length(graph, taskjob["Locations"][0], taskjob["Locations"][1])
            except nx.NetworkXNoPath:
                distance = float('inf')
            total_distance += distance

    return total_distance, container_assignments

# Function to generate a neighbor by swapping two assignments
def generate_neighbor(current_plan):
    truck_ids = list(current_plan.keys())
    new_plan = current_plan.copy()
    truck1, truck2 = random.sample(truck_ids, 2)
    new_plan[truck1], new_plan[truck2] = new_plan[truck2], new_plan[truck1]
    return new_plan

# Simulated Annealing algorithm function
def simulated_annealing(trucks, taskjobs, graph, containers, initial_temperature=10000, cooling_rate=0.003, stopping_temperature=1):
    current_plan = dict(zip(trucks.keys(), [taskjob["TaskJobID"] for taskjob in taskjobs]))
    current_distance, current_container_assignments = calculate_total_distance(current_plan, trucks, taskjobs, graph, containers)
    best_plan = current_plan.copy()
    best_distance = current_distance
    best_container_assignments = current_container_assignments.copy()
    temperature = initial_temperature

    while temperature > stopping_temperature:
        neighbor_plan = generate_neighbor(current_plan)
        neighbor_distance, neighbor_container_assignments = calculate_total_distance(neighbor_plan, trucks, taskjobs, graph, containers)
        cost_diff = neighbor_distance - current_distance

        if cost_diff < 0 or math.exp(-cost_diff / temperature) > random.random():
            current_plan = neighbor_plan.copy()
            current_distance = neighbor_distance
            current_container_assignments = neighbor_container_assignments.copy()

        if current_distance < best_distance:
            best_plan = current_plan.copy()
            best_distance = current_distance
            best_container_assignments = current_container_assignments.copy()

        temperature *= 1 - cooling_rate

    return best_plan, best_container_assignments, best_distance
