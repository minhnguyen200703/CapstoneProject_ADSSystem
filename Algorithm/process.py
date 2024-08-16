import json
import time
from preprocess import generate_taskjobs_from_orders
from trivial import generate_matching_plans, calculate_total_distance
import build_graph
import networkx as nx
from trivial import trivial_approach
from greedy import assign_tasks_greedy
from genetic import genetic_algorithm
from simulated_annealing import simulated_annealing
from optimized_matching import find_best_matching_plan
from brute_force import brute_force



# # Open and parse JSON files
# with open('..\\Data\\trucks.json') as f_Truck, \
#      open('..\\Data\\containers.json') as f_Containers, \
#      open('..\\Data\\orders.json') as f_Orders, \
#      open('..\\Data\\locations.json') as f_Locations, \
#      open('..\\Data\\distances.json') as f_Distances:
    
# Open and parse JSON files
with open('C:\\Users\\Minh\\Documents\\New folder\\CapstoneProject_ADSSystem\\Data\\trucks.json') as f_Truck, \
     open('C:\\Users\\Minh\\Documents\\New folder\\CapstoneProject_ADSSystem\\Data\\containers.json') as f_Containers, \
     open('C:\\Users\\Minh\\Documents\\New folder\\CapstoneProject_ADSSystem\\Data\\orders.json') as f_Orders, \
     open('C:\\Users\\Minh\\Documents\\New folder\\CapstoneProject_ADSSystem\\Data\\locations.json') as f_Locations, \
     open('C:\\Users\\Minh\\Documents\\New folder\\CapstoneProject_ADSSystem\\Data\\distance.json') as f_Distances:

    trucks = json.load(f_Truck)
    containers = json.load(f_Containers)
    orders = json.load(f_Orders)
    locations = json.load(f_Locations)
    distances = json.load(f_Distances)

# Initialize dictionaries and list
LocationList = [location for location in locations]
Distances = [distance for distance in distances]
AvailableTruckList = {truck["CarID"]: truck["current_location"] for truck in trucks if truck["isAvailable"]}
AvailableContainerList = {container["ContNumber"]: container["Location"] for container in containers if container["isAvailable"]}
AwaitingOrders = [order for order in orders if order["CurrentStatus"] == "Pending"]

# Generate TaskJobs from AwaitingOrders
AwaitingTaskJob = generate_taskjobs_from_orders(AwaitingOrders)
# Print the results
print("AvailableTruckList:", AvailableTruckList)
print("AvailableContainerList:", AvailableContainerList)
print("AwaitingOrders:", AwaitingOrders)
print("AwaitingTaskJob:", AwaitingTaskJob)

# Build graph
G = build_graph.build_graph(LocationList, Distances)

############################### Trivial Approach ####################################

# Apply Trivial algorithm

start_time = time.perf_counter_ns()
best_trivial_plan, best_trivial_container_plan, best_trivial_distance = trivial_approach(AvailableTruckList, AwaitingTaskJob, Distances, containers)
end_time = time.perf_counter_ns()
trivial_runtime = end_time - start_time
print("\nBest Matching Plan (Trivial Approach):", best_trivial_plan)
print("Best Container Plan (Trivial Approach):", best_trivial_container_plan)
print("Minimum Total Distance (Trivial Approach):", best_trivial_distance)
print("Trivial Approach Algorithm Runtime: {} nanoseconds".format(trivial_runtime))

############################### Brute Force ####################################

# Apply brute force algorithm
brute_start_time = time.perf_counter_ns()
best_brute_plan, best_brute_container_plan, best_brute_distance = brute_force(AvailableTruckList, AwaitingTaskJob, G, containers)
brute_end_time = time.perf_counter_ns()
brute_runtime = brute_end_time - brute_start_time

print("\nBest Matching Plan (Brute Force):", best_brute_plan)
print("Best Container Plan (Brute Force):", best_brute_container_plan)
print("Minimum Total Distance (Brute Force):", best_brute_distance)
print("Brute Force Algorithm Runtime: {} nanoseconds".format(brute_runtime))

############################### Greedy ####################################

# Apply greedy algorithm
greedy_start_time = time.perf_counter_ns()
best_greedy_plan, best_greedy_container_plan, best_greedy_distance = assign_tasks_greedy(AvailableTruckList, AwaitingTaskJob, G, containers)
greedy_end_time = time.perf_counter_ns()
greedy_runtime = greedy_end_time - greedy_start_time

print("\nBest Matching Plan (Greedy):", best_greedy_plan)
print("Best Container Plan (Greedy):", best_greedy_container_plan)
print("Minimum Total Distance (Greedy):", best_greedy_distance)
print("Greedy Algorithm Runtime: {} nanoseconds".format(greedy_runtime))


# ############################### Genetic ####################################

# # Apply genetic algorithm
# genetic_start_time = time.perf_counter_ns()
# best_genetic_plan, best_genetic_distance = genetic_algorithm(AvailableTruckList, AwaitingTaskJob, G, containers)
# genetic_end_time = time.perf_counter_ns()
# genetic_runtime = genetic_end_time - genetic_start_time

# print("\nBest Matching Plan (Genetic):", best_genetic_plan)
# print("Minimum Total Distance (Genetic):", best_genetic_distance)
# print("Genetic Algorithm Runtime: {} nanoseconds".format(genetic_runtime))


############################### Simulated Annealing ####################################

# Apply simulated annealing algorithm
sa_start_time = time.perf_counter_ns()
best_sa_plan, best_sa_container_plan, best_sa_distance = simulated_annealing(AvailableTruckList, AwaitingTaskJob, G, containers)
sa_end_time = time.perf_counter_ns()
sa_runtime = sa_end_time - sa_start_time

print("\nBest Matching Plan (Simulated Annealing):", best_sa_plan)
print("Best Container Plan (Simulated Annealing):", best_sa_container_plan)
print("Minimum Total Distance (Simulated Annealing):", best_sa_distance)
print("Simulated Annealing Algorithm Runtime: {} nanoseconds".format(sa_runtime))



############################### Optimized ####################################
# Apply optimized matching algorithm
opt_start_time = time.perf_counter_ns()
best_opt_plan, best_container_plan, best_opt_distance = find_best_matching_plan(AvailableTruckList, AwaitingTaskJob, G, containers)
opt_end_time = time.perf_counter_ns()
opt_runtime = opt_end_time - opt_start_time

print("\nBest Matching Plan (Optimized):", best_opt_plan)
print("Best Container Plan (Optimized):", best_container_plan)
print("Minimum Total Distance (Optimized):", best_opt_distance)
print("Optimized Matching Algorithm Runtime: {} nanoseconds".format(opt_runtime))