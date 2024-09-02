import itertools
import heapq  # For efficient selection of the top x nearest trucks
import networkx as nx
from dijkstra import dijkstra  # Importing the custom Dijkstra function

# Function to find the k nearest trucks to each taskjob
def find_k_nearest_trucks(trucks, taskjobs, graph, containers):
    nearest_trucks = {}
    x = min(len(trucks), len(taskjobs))

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
                            # Using custom dijkstra function
                            distance = dijkstra(graph, truck_location, container_location) + \
                                       dijkstra(graph, container_location, taskjob["Locations"][1])
                            if distance < min_distance:
                                min_distance = distance
                                best_container = container["ContNumber"]
                        except KeyError:  # Assuming dijkstra raises KeyError on no path
                            continue
                distances_to_trucks.append((truck_id, min_distance, best_container))
            else:
                try:
                    # Using custom dijkstra function
                    distance = dijkstra(graph, truck_location, taskjob["Locations"][0]) + \
                               dijkstra(graph, taskjob["Locations"][0], taskjob["Locations"][1])
                except KeyError:
                    distance = float('inf')
                distances_to_trucks.append((truck_id, distance, None))

        # Use a heap to find the top x nearest trucks
        top_x_trucks = heapq.nsmallest(x, distances_to_trucks, key=lambda item: item[1])
        nearest_trucks[taskjob["TaskJobID"]] = top_x_trucks

    return nearest_trucks

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    container_assignments = {}
    used_containers = set()  # Track used containers to ensure no duplication

    for truck_id, taskjob_id in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]

        if taskjob["TaskJobType"] == "Book_1":
            container_locations = [container for container in containers if container["isAvailable"] and container["ContNumber"] not in used_containers]
            min_distance = float('inf')
            best_container = None
            for container in container_locations:
                container_location = container["Location"]
                try:
                    # Using custom dijkstra function
                    distance = dijkstra(graph, truck_location, container_location) + \
                               dijkstra(graph, container_location, taskjob["Locations"][1])
                    if distance < min_distance:
                        min_distance = distance
                        best_container = container["ContNumber"]
                except KeyError:
                    continue
            if best_container:  # If a valid container is found
                total_distance += min_distance
                container_assignments[taskjob_id] = [truck_id, best_container]
                used_containers.add(best_container)  # Mark container as used
            else:
                total_distance = float('inf')  # If no valid container found, make this plan invalid
        else:
            try:
                # Using custom dijkstra function
                distance = dijkstra(graph, truck_location, taskjob["Locations"][0]) + \
                           dijkstra(graph, taskjob["Locations"][0], taskjob["Locations"][1])
            except KeyError:
                distance = float('inf')
            total_distance += distance
            container_assignments[taskjob_id] = truck_id  # Direct assignment if no container needed

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
