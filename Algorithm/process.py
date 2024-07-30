import json
from preprocess import generate_taskjobs_from_orders
from trivial import calculate_distance, generate_matching_plans, calculate_total_distance

# # Open and parse JSON files
# with open('..\\Data\\trucks.json') as f_Truck, \
#      open('..\\Data\\containers.json') as f_Containers, \
#      open('..\\Data\\orders.json') as f_Orders, \
#      open('..\\Data\\locations.json') as f_Locations, \
#      open('..\\Data\\distances.json') as f_Distances:
    
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
LocationList = []
Distances = []
AvailableTruckList = {}
AvailableContainerList = {}
AwaitingOrders = []
AwaitingTaskJob = []

# Loop through locations.json
for location in locations:
    LocationList.append(location)

# Loop through distances.json
for distance in distances:
    Distances.append(distance)

# Loop through trucks.json
for truck in trucks:
    if truck["isAvailable"]:
        AvailableTruckList[truck["CarID"]] = truck["current_location"]

# Loop through containers.json
for container in containers:
    if container["isAvailable"]:
        AvailableContainerList[container["ContNumber"]] = container["Location"]

# Loop through orders.json
for order in orders:
    if order["CurrentStatus"] == "Pending":
        AwaitingOrders.append(order)

# Generate TaskJobs from AwaitingOrders
AwaitingTaskJob = generate_taskjobs_from_orders(AwaitingOrders)

# Print the results
print("AvailableTruckList:", AvailableTruckList)
print("AvailableContainerList:", AvailableContainerList)
print("AwaitingOrders:", AwaitingOrders)
print("AwaitingTaskJob:", AwaitingTaskJob)

# Generate all possible matching plans
all_matching_plans = generate_matching_plans(AvailableTruckList, AwaitingTaskJob)

# Print all possible matching plans with their costs
print("All Possible Matching Plans and Their Costs:")
for plan in all_matching_plans:
    matching_plan = dict(zip(plan, [taskjob["TaskJobID"] for taskjob in AwaitingTaskJob]))
    total_distance = calculate_total_distance(matching_plan, AvailableTruckList, AwaitingTaskJob, Distances, containers)
    print("Matching Plan:", matching_plan, "Total Distance:", total_distance)

# Find the plan with the minimum total distance
min_distance = float('inf')
best_plan = None
for plan in all_matching_plans:
    matching_plan = dict(zip(plan, [taskjob["TaskJobID"] for taskjob in AwaitingTaskJob]))
    total_distance = calculate_total_distance(matching_plan, AvailableTruckList, AwaitingTaskJob, Distances, containers)
    if total_distance < min_distance:
        min_distance = total_distance
        best_plan = matching_plan

# Print the best plan and its total distance
print("\nBest Matching Plan:", best_plan)
print("Minimum Total Distance:", min_distance)













