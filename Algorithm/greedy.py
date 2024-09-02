import networkx as nx
from dijkstra import dijkstra  # Importing the custom Dijkstra function
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
                                # Using custom dijkstra function
                                distance_to_container = dijkstra(graph, truck_location, container_location)
                                distance_container_to_taskjob = dijkstra(graph, container_location, taskjob["Locations"][1])
                                distance = distance_to_container + distance_container_to_taskjob
                                
                                if distance < min_distance:
                                    min_distance = distance
                                    best_container = container["ContNumber"]
                            except ValueError as e:
                                print(e)
                                continue
                    cost = min_distance
                else:
                    try:
                        # Using custom dijkstra function
                        distance_to_task_start = dijkstra(graph, truck_location, taskjob["Locations"][0])
                        distance_task_start_to_end = dijkstra(graph, taskjob["Locations"][0], taskjob["Locations"][1])
                        cost = distance_to_task_start + distance_task_start_to_end
                    except ValueError as e:
                        print(e)
                        cost = float('inf')

                if cost < min_cost:
                    min_cost = cost
                    best_assignment = (truck_id, taskjob_id, best_container if taskjob["TaskJobType"] == "Book_1" else None)

        if best_assignment:
            truck_id, taskjob_id, container_id = best_assignment
            matching_plan[taskjob_id] = [truck_id, container_id] if container_id else truck_id
            total_distance += min_cost
            if container_id is not None:
                container_assignments[taskjob_id] = container_id
                used_containers.add(container_id)
            available_trucks.remove(truck_id)
            available_taskjobs.remove(taskjob_id)

    return matching_plan, container_assignments, total_distance