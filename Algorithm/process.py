import json
from preprocess import generate_taskjobs_from_orders

# Open and parse JSON files
with open('../Data/trucks.json') as f_Truck, \
     open('../Data/containers.json') as f_Containers, \
     open('../Data/orders.json') as f_Orders, \
     open('../Data/locations.json') as f_locations, \
     open('../Data/distances.json') as f_distances:

    trucks = json.load(f_Truck)
    containers = json.load(f_Containers)
    orders = json.load(f_Orders)
    locations = json.load(f_locations)
    distances = json.load(f_distances)

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