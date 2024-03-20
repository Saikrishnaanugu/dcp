import json
from datetime import datetime

# The JSON data as a string
json_string = '''
[
    {
        "timestamps": ["2023-09-07T17:20:00Z", "2023-09-07T17:25:00Z", "2023-09-07T17:30:00Z"],
        "properties": [
            {
                "values": [null, null, null],
                "name": "temperature",
                "type": "Double"
            }
        ],
        "progress": 100.0,
        "continuationToken": null
    },
    {
        "timestamps": ["2023-09-07T17:35:00Z", "2023-09-07T17:40:00Z", "2023-09-07T17:45:00Z"],
        "properties": [
            {
                "values": [null, null, null],
                "name": "temperature",
                "type": "Double"
            }
        ],
        "progress": 100.0,
        "continuationToken": null
    }
]
'''

# Parse the JSON data
data = json.loads(json_string)

# Extract and organize the data points
data_points = []

for entry in data:
    timestamps = entry['timestamps']
    values = entry['properties'][0]['values']  # Assuming there's only one property named "temperature"

    for timestamp, value in zip(timestamps, values):
        # Convert the timestamp to a Python datetime object
        timestamp_dt = datetime.fromisoformat(timestamp[:-1])  # Remove the 'Z' at the end

        # Create a data point dictionary with timestamp and temperature
        data_point = {
            'timestamp': timestamp_dt,
            'temperature': value
        }

        # Add the data point to the list
        data_points.append(data_point)

# Now 'data_points' list contains the extracted data points
print(data_points)

