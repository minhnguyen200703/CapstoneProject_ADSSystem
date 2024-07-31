import json
import time
from preprocess import generate_taskjobs_from_orders
from trivial import generate_matching_plans, calculate_total_distance
import build_graph
import networkx as nx
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

############################### Brute Force ####################################

# Apply brute force algorithm
brute_start_time = time.perf_counter_ns()
best_brute_plan, best_brute_distance = brute_force(AvailableTruckList, AwaitingTaskJob, G, containers)
brute_end_time = time.perf_counter_ns()
brute_runtime = brute_end_time - brute_start_time

print("\nBest Matching Plan (Brute Force):", best_brute_plan)
print("Minimum Total Distance (Brute Force):", best_brute_distance)
print("Brute Force Algorithm Runtime: {} nanoseconds".format(brute_runtime))

############################### Trivial Approach ####################################

# Start the timer
start_time_trivial = time.perf_counter_ns()

# Generate all possible matching plans
all_matching_plans = generate_matching_plans(AvailableTruckList, AwaitingTaskJob)

# Print all possible matching plans with their costs
best_plan = None
min_distance = float('inf')

# print("All Possible Matching Plans and Their Costs:")
print("\n")
for plan in all_matching_plans:
    matching_plan = dict(zip(plan, [taskjob["TaskJobID"] for taskjob in AwaitingTaskJob]))
    total_distance = calculate_total_distance(matching_plan, AvailableTruckList, AwaitingTaskJob, G, containers)
    # print("Matching Plan:", matching_plan, "Total Distance:", total_distance)
    if total_distance < min_distance:
        min_distance = total_distance
        best_plan = matching_plan

# Print the best plan and its total distance
print("\nBest Matching Plan:", best_plan)
print("Minimum Total Distance:", min_distance)

# End the timer
end_time_trivial = time.perf_counter_ns()

# Calculate total runtime
total_runtime = end_time_trivial - start_time_trivial
print("\nTotal Runtime Trivial: {} seconds".format(total_runtime))


############################### Greedy ####################################

# Apply greedy algorithm
greedy_start_time = time.perf_counter_ns()
best_greedy_plan = assign_tasks_greedy(AvailableTruckList, AwaitingTaskJob, G, containers)
greedy_end_time = time.perf_counter_ns()
greedy_total_distance = calculate_total_distance(best_greedy_plan, AvailableTruckList, AwaitingTaskJob, G, containers)
greedy_runtime = greedy_end_time - greedy_start_time

print("\nBest Matching Plan (Greedy):", best_greedy_plan)
print("Minimum Total Distance (Greedy):", greedy_total_distance)
print("Greedy Algorithm Runtime: {} nanoseconds".format(greedy_runtime))


############################### Genetic ####################################

# Apply genetic algorithm
genetic_start_time = time.perf_counter_ns()
best_genetic_plan, best_genetic_distance = genetic_algorithm(AvailableTruckList, AwaitingTaskJob, G, containers)
genetic_end_time = time.perf_counter_ns()
genetic_runtime = genetic_end_time - genetic_start_time

print("\nBest Matching Plan (Genetic):", best_genetic_plan)
print("Minimum Total Distance (Genetic):", best_genetic_distance)
print("Genetic Algorithm Runtime: {} nanoseconds".format(genetic_runtime))


############################### Simulated Annealing ####################################
# Apply simulated annealing algorithm
sa_start_time = time.perf_counter_ns()
best_sa_plan, best_sa_distance = simulated_annealing(AvailableTruckList, AwaitingTaskJob, G, containers)
sa_end_time = time.perf_counter_ns()
sa_runtime = sa_end_time - sa_start_time

print("\nBest Matching Plan (Simulated Annealing):", best_sa_plan)
print("Minimum Total Distance (Simulated Annealing):", best_sa_distance)
print("Simulated Annealing Algorithm Runtime: {} nanoseconds".format(sa_runtime))



############################### Optimized ####################################
# Apply optimized matching algorithm
opt_start_time = time.perf_counter_ns()
best_opt_plan, best_opt_distance = find_best_matching_plan(AvailableTruckList, AwaitingTaskJob, G, containers)
opt_end_time = time.perf_counter_ns()
opt_runtime = opt_end_time - opt_start_time

print("\nBest Matching Plan (Optimized):", best_opt_plan)
print("Minimum Total Distance (Optimized):", best_opt_distance)
print("Optimized Matching Algorithm Runtime: {} nanoseconds".format(opt_runtime))