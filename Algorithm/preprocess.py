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









# 



