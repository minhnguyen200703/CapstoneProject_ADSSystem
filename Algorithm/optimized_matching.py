import heapq
from dijkstra import dijkstra_with_intermediate
from dijkstra import dijkstra

# Function to find the k nearest trucks or truck-container pairs for each taskjob
def find_k_nearest_trucks_containers(trucks, containers, taskjobs, graph):
    nearest_trucks_containers = {}
    k = min(len(trucks), len(taskjobs))

    for taskjob in taskjobs:
        distances_to_vehicles = []
        task_start = taskjob["Locations"][0]
        
        if taskjob["TaskJobType"] == "Book_1":
            # Task requires both truck and container, and container location should replace None in Locations[0]
            for truck_id, truck_location in trucks.items():
                for container in containers:
                    if container["isAvailable"]:
                        container_location = container["Location"]

                        # Ensure the truck, container, and task start location are valid nodes
                        if truck_location not in graph.nodes or container_location not in graph.nodes or taskjob["Locations"][1] not in graph.nodes:
                            print(f"Skipping truck {truck_id} or container {container['ContNumber']} due to invalid node in the graph")
                            continue

                        try:
                            # Calculate the distance: truck -> container -> task start (Locations[1])
                            distance = dijkstra_with_intermediate(graph, truck_location, container_location, taskjob["Locations"][1])
                            if distance is None:
                                distance = float('inf')  # Handle missing distances
                            distances_to_vehicles.append((truck_id, distance, container["ContNumber"]))
                        except KeyError:
                            print(f"KeyError in finding distance for truck {truck_id} and container {container['ContNumber']}")
                            continue
        else:
            # Task only requires a truck
            for truck_id, truck_location in trucks.items():
                if truck_location not in graph.nodes or task_start not in graph.nodes or taskjob["Locations"][1] not in graph.nodes:
                    print(f"Skipping truck {truck_id} due to invalid node in the graph")
                    continue
                
                try:
                    # Calculate the distance: truck -> task start -> task end
                    distance = dijkstra_with_intermediate(graph, truck_location, task_start, taskjob["Locations"][1])
                    if distance is None:
                        distance = float('inf')  # Handle missing distances
                    distances_to_vehicles.append((truck_id, distance, None))
                except KeyError:
                    print(f"KeyError in finding distance for truck {truck_id}")
                    continue

        if distances_to_vehicles:
            # Use a heap to find the top k nearest trucks or truck-container pairs
            top_k_vehicles = heapq.nsmallest(k, distances_to_vehicles, key=lambda item: item[1])
            nearest_trucks_containers[taskjob["TaskJobID"]] = top_k_vehicles
        else:
            print(f"No valid trucks/containers found for task job {taskjob['TaskJobID']}")

    return nearest_trucks_containers

# Function to calculate the total distance for a given plan
def calculate_total_plan_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    container_assignments = {}

    for taskjob_id, (truck_id, container_id) in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]
        
        if taskjob["TaskJobType"] == "Book_1" and container_id:
            container_location = containers[container_id]["Location"]
            # Calculate distance: truck -> container -> task start (Locations[1]) -> task end (Locations[1])
            distance = dijkstra_with_intermediate(graph, truck_location, container_location, taskjob["Locations"][1])
            total_distance += distance
            container_assignments[taskjob_id] = container_id  # Track container assignment
            print(f"TaskJobID {taskjob_id} assigned ContainerID {container_id} with total distance {distance}")
        else:
            # Calculate distance: truck -> task start -> task end
            distance = dijkstra_with_intermediate(graph, truck_location, taskjob["Locations"][0], taskjob["Locations"][1])
            total_distance += distance

    return total_distance, container_assignments

# Main function to find the optimal matching plan
def find_optimal_plan(trucks, containers, taskjobs, graph):
    valid_taskjobs = []
    for taskjob in taskjobs:
        # Only skip if it's not Book_1, because None in Book_1 means we need the container location
        if taskjob["TaskJobType"] != "Book_1" and taskjob["Locations"][0] is None:
            print(f"Skipping task job {taskjob['TaskJobID']} due to missing start location")
            continue
        valid_taskjobs.append(taskjob)

    if not valid_taskjobs:
        print("No valid task jobs found.")
        return None, None, float('inf')

    nearest_trucks_containers = find_k_nearest_trucks_containers(trucks, containers, valid_taskjobs, graph)

    all_potential_plans = find_all_potential_plans(nearest_trucks_containers, valid_taskjobs, trucks, containers, graph)

    if not all_potential_plans:
        print("No potential plans found.")
        return None, None, float('inf')

    min_distance = float('inf')
    best_plan = None
    best_container_plan = None

    for plan in all_potential_plans:
        total_distance, container_plan = calculate_total_plan_distance(plan, trucks, valid_taskjobs, graph, containers)
        if total_distance < min_distance:
            min_distance = total_distance
            best_plan = plan
            best_container_plan = container_plan

    return best_plan, best_container_plan, min_distance

# Function to check and resolve any assignment conflicts using a binary tree approach
def find_all_potential_plans(nearest_trucks_containers, taskjobs, trucks, containers, graph):
    # Recursive function to explore all combinations of task job assignments
    def branch(node, taskjob_ids, current_assignments):
        # If all task jobs are assigned, return the current valid assignments
        if len(node) == len(taskjob_ids):
            return [current_assignments]

        # Get the next task job to process
        current_taskjob = taskjob_ids[len(node)]
        # Get the best available options for that task job
        best_options = nearest_trucks_containers[current_taskjob]

        result = []
        # Try each option (truck and container) for the current task job
        for idx, (truck_id, _, container_id) in enumerate(best_options):
            # Check if the truck or container is already assigned
            if truck_id in [v[0] for v in current_assignments.values()] or \
               (container_id and container_id in [v[1] for v in current_assignments.values()]):
                # Skip if the truck or container is already used
                continue
            # Make a copy of current assignments and add the new assignment
            new_assignments = current_assignments.copy()
            new_assignments[current_taskjob] = (truck_id, container_id)
            # Branch to the next task job
            result.extend(branch(node + [idx], taskjob_ids, new_assignments))

        return result

    # Get the list of task job IDs to process
    taskjob_ids = list(nearest_trucks_containers.keys())
    # Start branching to resolve conflicts and find valid assignment plans
    all_potential_plans = branch([], taskjob_ids, {})
    return all_potential_plans


