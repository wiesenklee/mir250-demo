#!/usr/bin/env python3

import requests
import json
import rospy

# ROS
from sensor_msgs.msg import Joy
rospy.init_node("rosmir_node")
throttle, steering, button = 0.0, 0.0,0.0
def cb(data):
    global throttle, steering, button
    throttle = data.axes[1]
    steering = data.axes[2]
    button = data.buttons[0]

sub = rospy.Subscriber("joy",Joy,cb)
rate = rospy.Rate(2)

class ROSAPI:
    def __init__(self, uri):
        self.url = uri if len(uri) > 0 else 'http://192.168.12.20/api/v2.0.0'
        self.payload  = {}
        self.headers = {
            'Authorization': 'Basic RGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA==',
            'Content-Type': 'application/json'
                    }

    # get information about source (url, type, id, ...)
    def getinfo(self,source):
        # /missions, /mission_queue, ...
        r = requests.request("GET", self.url+source, headers=self.headers, data = self.payload)
        # parsing requests -> python dictionary
        parsed = json.loads(r.text)
        # python dictionary -> json
        js = json.dumps(parsed,indent=2)
        print(js)

    # get information about PUT GET DELETE POST for source
    def listinfo(self,data):
        try:
            # read requests
            r = requests.request("GET", self.url, headers=self.headers, data = self.payload)
            # parsing requests -> python dictionary
            parsed = json.loads(r.text)
            # python dictionary -> json
            js = json.dumps(parsed,indent=2)
            print(js) if data == '' else print(parsed[data])
        except:
            print("typo error, try: '/missions' ")

    def do(self,source,payload):
        r = requests.request("POST", self.url+source, headers=self.headers, data = payload) 
        print(r.text.encode('utf8'))

    def put(self,source,payload):
        r = requests.request("PUT", self.url+source, headers=self.headers, data = payload) 
        print(r.text.encode('utf8'))

    def check(self,source):
        r = requests.request("GET", self.url+source, headers=self.headers, data = {}) 
        return json.loads(r.text)

i = ROSAPI('http://192.168.12.20/api/v2.0.0')
#i.getinfo('/status')
#i.listinfo('/mission_queue')
#i.put('/status',"{\"state_id\": 4}") #pause
i.put('/status',"{\"state_id\": 3}") #play
#i.do('/mission_queue',"{\"mission_id\": \"fa6e448b-3002-11ec-97dd-0001297861a6\"}") # sound
#i.do('/mission_queue',"{\"mission_id\": \"42fff034-2fe4-11ec-858f-0001297861a6\"}") # move fw
#i.do('/mission_queue',"{\"mission_id\": \"1e1a23d1-2fe5-11ec-858f-0001297861a6\"}") # move bw
#i.do('/mission_queue',"{\"mission_id\": \"6909221d-300f-11ec-a638-0001297861a6\"}") # move cw
#i.do('/mission_queue',"{\"mission_id\": \"78440d54-300f-11ec-a638-0001297861a6\"}") # move ccw

a= i.check('/mission_queue') # get mission list
print(len(a)) # total number if missions

def main():
    while not rospy.is_shutdown():
        if steering == 1.0: i.do('/mission_queue',"{\"mission_id\": \"6909221d-300f-11ec-a638-0001297861a6\"}") 
        if steering == -1.0 : i.do('/mission_queue',"{\"mission_id\": \"78440d54-300f-11ec-a638-0001297861a6\"}")

        if throttle == 1.0 : i.do('/mission_queue',"{\"mission_id\": \"42fff034-2fe4-11ec-858f-0001297861a6\"}")
        if throttle == -1.0 : i.do('/mission_queue',"{\"mission_id\": \"1e1a23d1-2fe5-11ec-858f-0001297861a6\"}")

        if button == 1: i.do('/mission_queue',"{\"mission_id\": \"fa6e448b-3002-11ec-97dd-0001297861a6\"}") # sound
        print(steering, throttle, button)
        rate.sleep()

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass