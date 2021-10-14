import requests

base_url = 'http://192.168.1.111/api/v2.0.0'
auth_key = 'RGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=='
auth_headers = {'accept': 'application/json', 'Authorization': 'Basic ' + auth_key, 'Accept-Language': 'de_DE'}

endpoint = '/missions'
response = requests.get(base_url + endpoint, headers=auth_headers)
print(response.json()[-1])
mission_id = response.json()[-1]["guid"]

endpoint = '/mission_queue'
response = requests.post(base_url + endpoint, json={'mission_id': mission_id}, headers=auth_headers)
print(response.json())

endpoint = '/status'
response = requests.put(base_url + endpoint, json={'state_id': 3}, headers=auth_headers)
print(response.json())
