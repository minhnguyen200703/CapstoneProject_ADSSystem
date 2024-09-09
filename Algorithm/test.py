import itertools
import heapq
from dijkstra import dijkstra_with_intermediate
from dijkstra import dijkstra

# Function to calculate the total distance for a given plan
def calculate_total_plan_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    container_assignments = {}

    for taskjob_id, (truck_id, container_id) in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]
        
        if taskjob["TaskJobType"] == "Book_1" and container_id:
            # Directly get the container location using container_id
            container_location = containers[container_id]  # containers[container_id] gives the location
            # Calculate distance: truck -> container -> task start (Locations[1]) -> task end
            distance = dijkstra_with_intermediate(graph, truck_location, container_location, taskjob["Locations"][1])
            total_distance += distance
            container_assignments[taskjob_id] = container_id  # Track container assignment
            print(f"TaskJobID {taskjob_id} assigned ContainerID {container_id} with total distance {distance}")
        else:
            # Calculate distance: truck -> task start -> task end
            distance = dijkstra_with_intermediate(graph, truck_location, taskjob["Locations"][0], taskjob["Locations"][1])
            total_distance += distance

    return total_distance, container_assignments


# Brute-force function to check all possible plans
def brute_force_plan(trucks, containers, taskjobs, graph):
    all_possible_plans = []

    # Generate all possible combinations of trucks for taskjobs
    truck_ids = list(trucks.keys())
    taskjob_ids = [tj["TaskJobID"] for tj in taskjobs]

    # Generate all permutations of truck assignments
    truck_permutations = list(itertools.permutations(truck_ids, len(taskjob_ids)))

    # Prepare container-related data for Book_1 tasks
    book_1_taskjob_ids = [tj["TaskJobID"] for tj in taskjobs if tj["TaskJobType"] == "Book_1"]
    container_ids = list(containers.keys())
    container_permutations = list(itertools.permutations(container_ids, len(book_1_taskjob_ids))) if book_1_taskjob_ids else [[]]

    # Iterate over all possible truck permutations
    for truck_perm in truck_permutations:
        # Iterate over all possible container permutations
        for container_perm in container_permutations:
            current_plan = {}
            container_assignment = {book_1_taskjob_ids[i]: container_perm[i] for i in range(len(book_1_taskjob_ids))}
            
            # Assign trucks to all task jobs
            for i, taskjob_id in enumerate(taskjob_ids):
                current_plan[taskjob_id] = (truck_perm[i], container_assignment.get(taskjob_id, None))  # Assign trucks and containers

            # Calculate total distance for this plan
            total_distance, _ = calculate_total_plan_distance(current_plan, trucks, taskjobs, graph, containers)
            all_possible_plans.append((current_plan, total_distance))

    # Find the plan with the minimum total distance
    best_plan = min(all_possible_plans, key=lambda x: x[1])
    
    return best_plan

# Function to run brute-force check
def brute_force_check(trucks, containers, taskjobs, graph):
    best_brute_plan, best_brute_distance = brute_force_plan(trucks, containers, taskjobs, graph)

    print("Best Brute-Force Plan:", best_brute_plan)
    print("Best Brute-Force Total Distance:", best_brute_distance)
