# greedy.py

# Function to calculate the distance between two locations
def calculate_distance(loc1, loc2, distances):
    for distance in distances:
        if distance["LocationFromID"] == loc1 and distance["LocationToID"] == loc2:
            return float(distance["DistanceKm"])
    return float('inf')  # return a large number if distance is not found

# Function to assign taskjobs to trucks using a greedy algorithm
def assign_tasks_greedy(trucks, taskjobs, distances, containers):
    matching_plan = {}
    available_trucks = set(trucks.keys())
    available_taskjobs = set(taskjob["TaskJobID"] for taskjob in taskjobs)

    while available_taskjobs:
        best_assignment = None
        min_cost = float('inf')
        
        for truck_id in available_trucks:
            for taskjob_id in available_taskjobs:
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
                    cost = min_distance
                else:
                    cost = calculate_distance(str(truck_location), str(taskjob["Locations"][0]), distances) + \
                           calculate_distance(str(taskjob["Locations"][0]), str(taskjob["Locations"][1]), distances)
                
                if cost < min_cost:
                    min_cost = cost
                    best_assignment = (truck_id, taskjob_id)
        
        if best_assignment:
            truck_id, taskjob_id = best_assignment
            matching_plan[truck_id] = taskjob_id
            available_trucks.remove(truck_id)
            available_taskjobs.remove(taskjob_id)
    
    return matching_plan
