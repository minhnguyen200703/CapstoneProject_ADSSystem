import itertools

# Function to calculate the distance between two locations
def calculate_distance(loc1, loc2, distances):
    for distance in distances:
        if distance["LocationFromID"] == loc1 and distance["LocationToID"] == loc2:
            return float(distance["DistanceKm"])
    return float('inf')  # return a large number if distance is not found

# Function to generate all possible matching plans
def generate_matching_plans(trucks, taskjobs):
    truck_ids = list(trucks.keys())
    taskjob_ids = [taskjob["TaskJobID"] for taskjob in taskjobs]
    return list(itertools.permutations(truck_ids, len(taskjob_ids)))

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