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

def filterDistanceFileAttributes(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    filtered_data = []
    for record in data['RECORDS']:
        filtered_record = { # Eliminate other attributes
            "DistanceKm": record["DistanceKm"],
            "LocationFromName": record["LocationFromName"],
            "LocationToName": record["LocationToName"]
        }
        filtered_data.append(filtered_record)
    
    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=4)
    print("Processed Distance Data Successfully, File Name:", output_file)

# Run the func
input_file = 'Data/Data_23042024/Distance.json'
output_file = 'Data/distance.json'
filterDistanceFileAttributes(input_file, output_file)









# 



