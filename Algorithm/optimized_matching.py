import itertools

# Function to calculate the distance between two locations
def calculate_distance(loc1, loc2, distances):
    for distance in distances:
        if distance["LocationFromID"] == loc1 and distance["LocationToID"] == loc2:
            return float(distance["DistanceKm"])
    return float('inf')  # return a large number if distance is not found

# Function to find the k nearest trucks to each taskjob
def find_k_nearest_trucks(trucks, taskjobs, distances, k, containers):
    nearest_trucks = {}
    for taskjob in taskjobs:
        distances_to_trucks = []
        for truck_id, truck_location in trucks.items():
            if taskjob["TaskJobType"] == "Book_1":
                # Find nearest truck and container pair
                min_distance = float('inf')
                for container in containers:
                    if container["isAvailable"]:
                        container_location = container["Location"]
                        distance = calculate_distance(str(truck_location), str(container_location), distances) + \
                                   calculate_distance(str(container_location), str(taskjob["Locations"][1]), distances)
                        if distance < min_distance:
                            min_distance = distance
                distances_to_trucks.append((truck_id, min_distance))
            else:
                distance = calculate_distance(str(truck_location), str(taskjob["Locations"][0]), distances) + \
                           calculate_distance(str(taskjob["Locations"][0]), str(taskjob["Locations"][1]), distances)
                distances_to_trucks.append((truck_id, distance))

        distances_to_trucks.sort(key=lambda x: x[1])
        nearest_trucks[taskjob["TaskJobID"]] = distances_to_trucks[:k]

    return nearest_trucks

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, distances, containers):
    total_distance = 0
    for truck_id, taskjob_id in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]

        if taskjob["TaskJobType"] == "Book_1":
            container_locations = [container["Location"] for container in containers if container["isAvailable"]]
            min_distance = float('inf')
            for container_location in container_locations:
                distance = calculate_distance(str(truck_location), str(container_location), distances) + \
                           calculate_distance(str(container_location), str(taskjob["Locations"][1]), distances)
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance
        else:
            distance = calculate_distance(str(truck_location), str(taskjob["Locations"][0]), distances) + \
                       calculate_distance(str(taskjob["Locations"][0]), str(taskjob["Locations"][1]), distances)
            total_distance += distance

    return total_distance

# Function to find the best matching plan
def find_best_matching_plan(trucks, taskjobs, distances, containers):
    k = min(len(trucks), len(taskjobs))
    nearest_trucks = find_k_nearest_trucks(trucks, taskjobs, distances, k, containers)

    # Generate all potential matching plans
    taskjob_ids = list(nearest_trucks.keys())
    potential_plans = []
    for perm in itertools.permutations(range(k), len(taskjob_ids)):
        plan = {}
        for i, taskjob_id in enumerate(taskjob_ids):
            plan[nearest_trucks[taskjob_id][perm[i]][0]] = taskjob_id
        potential_plans.append(plan)

    # Calculate the total distance for each potential plan
    min_distance = float('inf')
    best_plan = None
    for plan in potential_plans:
        total_distance = calculate_total_distance(plan, trucks, taskjobs, distances, containers)
        if total_distance < min_distance:
            min_distance = total_distance
            best_plan = plan

    return best_plan, min_distance

