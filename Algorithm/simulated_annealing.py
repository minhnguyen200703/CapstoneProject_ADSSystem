
# simulated_annealing.py
import random
import math

# Function to calculate the distance between two locations
def calculate_distance(loc1, loc2, distances):
    for distance in distances:
        if distance["LocationFromID"] == loc1 and distance["LocationToID"] == loc2:
            return float(distance["DistanceKm"])
    return float('inf')  # return a large number if distance is not found

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

# Function to generate a neighbor by swapping two assignments
def generate_neighbor(current_plan, taskjob_ids):
    truck_ids = list(current_plan.keys())
    new_plan = current_plan.copy()
    truck1, truck2 = random.sample(truck_ids, 2)
    new_plan[truck1], new_plan[truck2] = new_plan[truck2], new_plan[truck1]
    return new_plan

# Simulated Annealing algorithm function
def simulated_annealing(trucks, taskjobs, distances, containers, initial_temperature=10000, cooling_rate=0.003, stopping_temperature=1):
    current_plan = dict(zip(trucks.keys(), [taskjob["TaskJobID"] for taskjob in taskjobs]))
    current_distance = calculate_total_distance(current_plan, trucks, taskjobs, distances, containers)
    best_plan = current_plan.copy()
    best_distance = current_distance
    temperature = initial_temperature

    while temperature > stopping_temperature:
        neighbor_plan = generate_neighbor(current_plan, taskjobs)
        neighbor_distance = calculate_total_distance(neighbor_plan, trucks, taskjobs, distances, containers)
        cost_diff = neighbor_distance - current_distance

        if cost_diff < 0 or math.exp(-cost_diff / temperature) > random.random():
            current_plan = neighbor_plan.copy()
            current_distance = neighbor_distance

        if current_distance < best_distance:
            best_plan = current_plan.copy()
            best_distance = current_distance

        temperature *= 1 - cooling_rate

    return best_plan, best_distance
