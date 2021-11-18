#!/usr/bin/env python3
import hashlib
import requests
import base64
import time
import json

base_url = 'http://192.168.1.111/api/v2.0.0'
auth_user = 'Distributor'
auth_pass = 'distributor'
auth_key = auth_user + ':' + hashlib.sha256(auth_pass.encode()).hexdigest()
auth_key_encoded = base64.b64encode(auth_key.encode()).decode('utf-8')
auth_headers = {'accept': 'application/json',
                'Authorization': 'Basic ' + auth_key_encoded, 'Accept-Language': 'de_DE'}

def get_status():
    endpoint = '/status'
    response = requests.get(base_url + endpoint, headers=auth_headers)
    return response.json()


def set_status(body):
    endpoint = '/status'
    response = requests.put(base_url + endpoint,
                            json=body, headers=auth_headers)
    return response.json()

# ++ MISSIONS ++


def get_mission_group_guid(name=''):
    # Get all mission groups
    endpoint = '/mission_groups'
    response = requests.get(base_url + endpoint, headers=auth_headers)
    groups = response.json()

    # Iterate through groups
    for group in groups:
        if group['name'] == name:
            return group['guid']
    return False


def create_mission_group(name, icon, priority=1, feature='default'):
    endpoint = '/mission_groups'
    body = {
        "name": name,
        "feature": feature,
        "icon": icon,
        "priority": priority
    }
    response = requests.post(
        base_url + endpoint, json=body, headers=auth_headers)
    return response.json()["guid"]


def create_mission(name):
    endpoint = '/missions'
    body = {}
    response = requests.post(
        base_url + endpoint, json=body, headers=auth_headers)
    return response.json()["guids"]

# ++ POSITIONS ++


def print_positions():
    endpoint = '/positions'
    response = requests.get(base_url + endpoint, headers=auth_headers)
    return response.json()


def get_position(guid):
    endpoint = '/positions/' + guid
    response = requests.get(base_url + endpoint, headers=auth_headers)
    return response.json()


def set_position(guid, y):
    endpoint = '/positions/' + guid
    body = {
        "pos_y": y,
    }
    response = requests.put(base_url + endpoint,
                            json=body, headers=auth_headers)
    return response.json()

# +++ Custom Scripts +++

# create new mission with custom name and icon
def custom_mission_group():
    mission_group_name = "Python Group"
    mission_group_guid = get_mission_group_guid(mission_group_name)
    if not mission_group_guid:
        with open('base64svg.txt') as f:
            mission_group_guid = create_mission_group(
                mission_group_name, icon=f.read())
    print(mission_group_guid)

# wont work :(, not all endpoints from  rosbridge can be accessed via API
def custom_set_speed():
    endpoint = '/joystick_vel' 
    body = {
        "joystick_token": token,
        "speed_command": {
            "linear": {
                "x": 1,
                "y": 0,
                "z": 0
            },
            "angular": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        }
    }
    response = requests.put(base_url + endpoint, json=body, headers=auth_headers)
    print(json.dumps(response.json()))

# +++ SOME DIRECT CODE SAMPLES +++

# pos_guid = "360933ab-37d4-11ec-9fd2-0001297861a6"
# prev_pos = get_position(pos_guid)
# print(set_position(pos_guid, prev_pos["pos_y"] + 1))
# time.sleep(0.5)
# print(set_position(pos_guid, prev_pos["pos_y"]))

# print(print_positions())

set_status({"clear_error": True})
print(get_status()["mode_key_state"])
print(get_status()["state_id"])
token = set_status(
    {"state_id": 11, "web_session_id": "67l8b1nns52ue9kp5qtt8fivl1"})
print(token)
print(get_status()["state_id"])

print("--> press resume button on robot")
input()

# print(json.dumps(get_status(), indent=2, sort_keys=True))