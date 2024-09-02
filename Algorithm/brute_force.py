import itertools
import time
from dijkstra import dijkstra  # Importing the custom Dijkstra function

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
                    distance_to_container = dijkstra(graph, truck_location, container_location)
                    distance_container_to_taskjob = dijkstra(graph, container_location, taskjob["Locations"][1])
                    distance = distance_to_container + distance_container_to_taskjob
                    if distance < min_distance:
                        min_distance = distance
                        best_container = next(container["ContNumber"] for container in containers if container["Location"] == container_location)
                except ValueError as e:
                    print(e)
                    continue
            total_distance += min_distance
            container_assignments[taskjob_id] = best_container
        else:
            try:
                distance_to_task_start = dijkstra(graph, truck_location, taskjob["Locations"][0])
                distance_task_start_to_end = dijkstra(graph, taskjob["Locations"][0], taskjob["Locations"][1])
                distance = distance_to_task_start + distance_task_start_to_end
            except ValueError as e:
                print(e)
                distance = float('inf')
            total_distance += distance

    return total_distance, container_assignments


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
    time.sleep(0.05)  # Small delay to simulate computation time
    min_distance = float('inf')
    best_plan = None
    best_container_plan = None

    for plan in all_plans:
        matching_plan = dict(zip(plan, [taskjob["TaskJobID"] for taskjob in taskjobs]))
        total_distance, container_assignments = calculate_total_distance(matching_plan, trucks, taskjobs, graph, containers)
        if total_distance < min_distance:
            min_distance = total_distance
            best_plan = matching_plan
            best_container_plan = container_assignments

    return best_plan, best_container_plan, min_distance