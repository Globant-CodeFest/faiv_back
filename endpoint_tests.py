import requests
import json

# # 645069496 Junio 1990
# # 679197496 Julio 1991

# -33.42880235568389, -70.6053026540827


body = {
    'location': {
        'lat': -33.42880235568389, # Number
        'lng': -70.6053026540827, # Number
        'elevation': 0 # Number
    },
    'dateRange': {
        'startDate': 645069496, # timestamp,
        'endDate': 679197496 # timestamp,
    },
}
URL = 'https://vvac2nztgxuwsbs6qq7hgk3za40adukc.lambda-url.us-east-1.on.aws/'

headers = {
    'Content-Type': 'application/json',
    'api-key': 'hola'
}

res = requests.post(URL, headers=headers, json=body)
print(res)
print(res.json())