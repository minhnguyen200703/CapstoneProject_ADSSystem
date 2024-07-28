import json

# Orders to Taskjobs



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



