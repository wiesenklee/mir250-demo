from hashlib import sha256
import requests
import base64

base_url = 'http://192.168.1.111/api/v2.0.0'
auth_user = 'Distributor'
auth_pass = 'distributor'
auth_key = auth_user + ':' + sha256(auth_pass.encode()).hexdigest()
auth_key_encoded = base64.b64encode(auth_key.encode()).decode('utf-8')
auth_headers = {'accept': 'application/json', 'Authorization': 'Basic ' + auth_key_encoded, 'Accept-Language': 'de_DE'}

# Get Latested added mission

# endpoint = '/missions'
# response = requests.get(base_url + endpoint, headers=auth_headers)
# print(response.json()[-1])
# mission_id = response.json()[-1]["guid"]

# Add new mission

# endpoint = '/mission_queue'
# response = requests.post(base_url + endpoint, json={'mission_id': mission_id}, headers=auth_headers)
# print(response.json())

# endpoint = '/status'
# response = requests.put(base_url + endpoint, json={'state_id': 3}, headers=auth_headers)
# print(response.json())

def get_mission_group_guid(name=''):
    # Get all mission groups
    endpoint = '/mission_groups'
    response = requests.get(base_url + endpoint, headers=auth_headers)
    groups = response.json()

    # Iterate through groups
    for group in groups: 
        if group['name'] == name: return group['guid']
    return False

def create_mission_group(name, icon, priority=1, feature='default'):
    endpoint = '/mission_groups'
    body = {
        "name": name,
        "feature": feature,
        "icon": icon,
        "priority": priority
    }
    response = requests.post(base_url + endpoint, json=body, headers=auth_headers)
    return response.json()["guid"]

def create_mission(name):
    endpoint = '/missions'
    body = {
        "name": name,
        "feature": feature,
        "icon": icon,
        "priority": priority
    }
    response = requests.post(base_url + endpoint, json=body, headers=auth_headers)
    return response.json()["guids"]

mission_group_name = "Python Group"
mission_group_guid = get_mission_group_guid(mission_group_name)
if not mission_group_guid:
    with open('base64svg.txt') as f: 
        mission_group_guid = create_mission_group(mission_group_name, icon=f.read())

print(mission_group_guid)