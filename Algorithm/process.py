import json
import time
from preprocess import generate_taskjobs_from_orders
from trivial import generate_matching_plans, calculate_total_distance
import build_graph
import networkx as nx
import matplotlib.pyplot as plt
from trivial import trivial_approach
from greedy import assign_tasks_greedy
from genetic import genetic_algorithm
from simulated_annealing import simulated_annealing
from optimized_matching import find_optimal_plan
from brute_force import brute_force
from visualization import visualize_graphs  # Import the visualization functions
from test import brute_force_check

# # Open and parse JSON files
# with open('..\\Data\\trucks.json') as f_Truck, \
#      open('..\\Data\\containers.json') as f_Containers, \
#      open('..\\Data\\orders.json') as f_Orders, \
#      open('..\\Data\\locations.json') as f_Locations, \
#      open('..\\Data\\distances.json') as f_Distances:
    
# Open and parse JSON files
with open('C:\\Users\\thang\\Documents\\GitHub\\CapstoneProject_ADSSystem\\Data\\trucks.json') as f_Truck, \
     open('C:\\Users\\thang\\Documents\\GitHub\\CapstoneProject_ADSSystem\Data\containers.json') as f_Containers, \
     open('C:\\Users\\thang\\Documents\\GitHub\\CapstoneProject_ADSSystem\\Data\\orders.json') as f_Orders, \
     open('C:\\Users\\thang\\Documents\\GitHub\\CapstoneProject_ADSSystem\\Data\\locations.json') as f_Locations, \
     open('C:\\Users\\thang\\Documents\\GitHub\\CapstoneProject_ADSSystem\\Data\\distance.json') as f_Distances:

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


############################### Optimized ####################################
# Apply optimized matching algorithm
opt_start_time = time.perf_counter_ns()
best_opt_plan, best_container_plan, best_opt_distance = find_optimal_plan(AvailableTruckList,containers, AwaitingTaskJob, G )
opt_end_time = time.perf_counter_ns()
opt_runtime = opt_end_time - opt_start_time

print("\nBest Matching Plan (Optimized):", best_opt_plan)
print("Best Container Plan (Optimized):", best_container_plan)
print("Minimum Total Distance (Optimized):", best_opt_distance)
print("Optimized Matching Algorithm Runtime: {} nanoseconds".format(opt_runtime))



  