import json

# Orders to Taskjobs
import uuid

def generate_taskjobs_from_orders(orders):
    taskjobs = []
    for order in orders:
        if order["OrderType"] == "Booking":
            taskjobs.append({
                "TaskJobID": str(uuid.uuid4()),
                "OrderID": order["OrderID"],
                "TaskJobType": "Book_1",
                "Deadline": order["Book_LiftingEmpty"],
                "Locations": [None, order["Locations"][0]],
                "CurrentStatus": "Pending"
            })

            taskjobs.append({
                "TaskJobID": str(uuid.uuid4()),
                "OrderID": order["OrderID"],
                "TaskJobType": "Book_2",
                "Deadline": order["Book_CutOffDate"],
                "Locations": order["Locations"],
                "CurrentStatus": "Pending"
            })

        elif order["OrderType"] == "Bill":
            taskjobs.append({
                "TaskJobID": str(uuid.uuid4()),
                "OrderID": order["OrderID"],
                "TaskJobType": "Bill_1",
                "Deadline": order["Bill_LastFreeDayDEM"],
                "Locations": order["Locations"],
                "CurrentStatus": "Pending"
            })

            taskjobs.append({
                "TaskJobID": str(uuid.uuid4()),
                "OrderID": order["OrderID"],
                "TaskJobType": "Bill_2",
                "Deadline": order["Bill_LastFreeDayDET"],
                "Locations": order["Locations"][::-1],
                "CurrentStatus": "Pending"
            })
            
    return taskjobs


#  Extracting distances for our simulated locations.json

# def filterDistanceFileAttributes(input_file, output_file):
#     with open(input_file, 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
#     filtered_data = []
#     for record in data['RECORDS']:
#         filtered_record = { # Eliminate other attributes
#             "DistanceKm": record["DistanceKm"],
#             "LocationFromName": record["LocationFromName"],
#             "LocationToName": record["LocationToName"]
#         }
#         filtered_data.append(filtered_record)
    
#     with open(output_file, 'w') as f:
#         json.dump(filtered_data, f, indent=4)
#     print("Processed Distance Data Successfully, File Name:", output_file)

# # Run the func
# input_file = 'Data/Data_23042024/Distance.json'
# output_file = 'Data/distance.json'
# filterDistanceFileAttributes(input_file, output_file)


# Load locations and distances JSON data
with open('C:\\Users\\Minh\\Documents\\New folder\\CapstoneProject_ADSSystem\\Data\\locations.json', 'r', encoding='utf-8') as f:
    locations = json.load(f)

with open('C:\\Users\\Minh\\Documents\\New folder\\CapstoneProject_ADSSystem\\Data\\Data_23042024\\Distance.json', 'r', encoding='utf-8') as f:
    old_distances = json.load(f)

# Create a mapping from location names to location IDs
location_name_to_id = {loc['Name']: loc['LocationID'] for loc in locations}

# Prepare the new distances list
new_distances = []

# Loop through old distances to find corresponding distances and map to IDs
for record in old_distances['RECORDS']:
    location_from_name = record['LocationFromName'].strip()
    location_to_name = record['LocationToName'].strip()

    if location_from_name in location_name_to_id and location_to_name in location_name_to_id:
        location_from_id = location_name_to_id[location_from_name]
        location_to_id = location_name_to_id[location_to_name]
        distance_km = record['DistanceKm']

        new_distances.append({
            'LocationFromID': location_from_id,
            'LocationToID': location_to_id,
            'DistanceKm': distance_km
        })

# Save the new distances to a new JSON file
new_distance_data = {'RECORDS': new_distances}

with open('new_distance.json', 'w', encoding='utf-8') as f:
    json.dump(new_distance_data, f, ensure_ascii=False, indent=4)

print("New distance.json file created successfully.")






# 



