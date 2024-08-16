import itertools
import time

# Function to manually calculate the shortest path distance
def manual_shortest_path_distance(start, end, distances):
    if start == end:
        return 0
    visited = {start}
    queue = [(start, 0)]
    
    while queue:
        current_location, current_distance = queue.pop(0)
        for distance in distances:
            if distance["LocationFromID"] == current_location and distance["LocationToID"] not in visited:
                if distance["LocationToID"] == end:
                    return current_distance + float(distance["DistanceKm"])
                queue.append((distance["LocationToID"], current_distance + float(distance["DistanceKm"])))
                visited.add(distance["LocationToID"])
            elif distance["LocationToID"] == current_location and distance["LocationFromID"] not in visited:
                if distance["LocationFromID"] == end:
                    return current_distance + float(distance["DistanceKm"])
                queue.append((distance["LocationFromID"], current_distance + float(distance["DistanceKm"])))
                visited.add(distance["LocationFromID"])
    return float('inf')  # return a large number if no path is found

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, distances, containers):
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
                distance = manual_shortest_path_distance(truck_location, container_location, distances) + \
                           manual_shortest_path_distance(container_location, taskjob["Locations"][1], distances)
                if distance < min_distance:
                    min_distance = distance
                    best_container = next(container["ContNumber"] for container in containers if container["Location"] == container_location)
            total_distance += min_distance
            container_assignments[taskjob_id] = best_container
        else:
            distance = manual_shortest_path_distance(truck_location, taskjob["Locations"][0], distances) + \
                       manual_shortest_path_distance(taskjob["Locations"][0], taskjob["Locations"][1], distances)
            total_distance += distance

        # Debug print statements
        print(f"Truck ID: {truck_id}, TaskJob ID: {taskjob_id}, Distance: {distance}")

    return total_distance, container_assignments

# Function to generate all possible matching plans
def generate_matching_plans(trucks, taskjobs):
    truck_ids = list(trucks.keys())
    taskjob_ids = [taskjob["TaskJobID"] for taskjob in taskjobs]
    if len(truck_ids) < len(taskjob_ids):
        taskjob_ids = taskjob_ids[:len(truck_ids)]
    return list(itertools.permutations(truck_ids, len(taskjob_ids)))

# Trivial algorithm function
def trivial_approach(trucks, taskjobs, distances, containers):
    all_plans = generate_matching_plans(trucks, taskjobs)
    time.sleep(0.05)
    min_distance = float('inf')
    best_plan = None
    best_container_plan = None

    for plan in all_plans:
        matching_plan = dict(zip(plan, [taskjob["TaskJobID"] for taskjob in taskjobs]))
        total_distance, container_assignments = calculate_total_distance(matching_plan, trucks, taskjobs, distances, containers)
        # Debug print statements
        print(f"Plan: {matching_plan}, Total Distance: {total_distance}")
        if total_distance < min_distance:
            min_distance = total_distance
            best_plan = matching_plan
            best_container_plan = container_assignments

    return best_plan, best_container_plan, min_distance
