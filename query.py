import requests

url = "https://dtir-webapp.azurewebsites.net/timeseriesdata?sensortype=tempsensors=AHU01CoolCoilDAT&sensors=AHU01SAT&sensors=AHU01EAT&sensors=AHU01OAT&sensors=AHU01RAT&sensors=AHU01SAT&since=60m&interval=pt5m&yaxis=stacked"
response = requests.get(url)

if response.status_code == 200:
    print("Request successful!")
    print("Response Content:")
    print(response.text)
else:
    print("Request failed with status code: {response.status_code}")
