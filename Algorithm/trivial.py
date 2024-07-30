import itertools
from dijkstra import dijkstra

# Function to calculate the total distance for a given matching plan
def calculate_total_distance(plan, trucks, taskjobs, graph, containers):
    total_distance = 0
    for truck_id, taskjob_id in plan.items():
        taskjob = next(tj for tj in taskjobs if tj["TaskJobID"] == taskjob_id)
        truck_location = trucks[truck_id]

        if taskjob["TaskJobType"] == "Book_1":
            container_locations = [container["Location"] for container in containers if container["isAvailable"]]
            min_distance = float('inf')
            for container_location in container_locations:
                distance = dijkstra(graph, str(truck_location), str(container_location)) + \
                           dijkstra(graph, str(container_location), str(taskjob["Locations"][1]))
                if distance < min_distance:
                    min_distance = distance
            total_distance += min_distance
        else:
            distance = dijkstra(graph, str(truck_location), str(taskjob["Locations"][0])) + \
                       dijkstra(graph, str(taskjob["Locations"][0]), str(taskjob["Locations"][1]))
            total_distance += distance

    return total_distance

# Function to generate all possible matching plans
def generate_matching_plans(trucks, taskjobs):
    truck_ids = list(trucks.keys())
    taskjob_ids = [taskjob["TaskJobID"] for taskjob in taskjobs]
    return list(itertools.permutations(truck_ids, len(taskjob_ids)))
