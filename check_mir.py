#!/usr/bin/env python3

import requests
import json
import rospy


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
        #print(js)
        return r,parsed,js
     

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
        #print(r.text.encode('utf8'))
        return r.text.encode('utf8')

    def put(self,source,payload):
        r = requests.request("PUT", self.url+source, headers=self.headers, data = payload) 
        #print(r.text.encode('utf8'))
        return r.text.encode('utf8')

    def check(self,source):
        r = requests.request("GET", self.url+source, headers=self.headers, data = {}) 
        return json.loads(r.text)

# create insdtance       
mir = ROSAPI('http://192.168.12.20/api/v2.0.0')
#mir.getinfo('')
#mir.listinfo('/position_types')


goal = mir.check('/positions') # retrieve position GUID
print("**ID to modify during operation\n\t",goal[8]['guid'])


infoY = mir.check('/positions/3b70ea6b-3c95-11ec-be1f-0001297861a6')
print("**get actual goal in y direction\n\t",infoY['pos_y'])


newgoal= 23
print("**change goal with desired y position\n\t", newgoal)
mir.put('/positions/3b70ea6b-3c95-11ec-be1f-0001297861a6','{\"pos_y\":'+str(newgoal)+'}')

while(1):
    _,p,_ = mir.getinfo('/status')
    robotstate= round(p['position']['y'],1)
    print("**get actual position of mir\n\t",robotstate)

    deltaY = abs(robotstate - newgoal)
    print("**delta position of mir to goal \n\t",deltaY)

    if(deltaY <= 0.2):
        mir.put('/positions/3b70ea6b-3c95-11ec-be1f-0001297861a6','{\"pos_y\":'+str(newgoal+0.5)+'}')
    else:
        break


# etc...

#mir.put('/status',"{\"state_id\": 4}") #pause
#mir.put('/status',"{\"state_id\": 3}") #play
#mir.do('/mission_queue',"{\"mission_id\": \"fa6e448b-3002-11ec-97dd-0001297861a6\"}") # sound
#mir.do('/mission_queue',"{\"mission_id\": \"42fff034-2fe4-11ec-858f-0001297861a6\"}") # move fw
#mir.do('/mission_queue',"{\"mission_id\": \"1e1a23d1-2fe5-11ec-858f-0001297861a6\"}") # move bw
#mir.do('/mission_queue',"{\"mission_id\": \"6909221d-300f-11ec-a638-0001297861a6\"}") # move cw
#mir.do('/mission_queue',"{\"mission_id\": \"78440d54-300f-11ec-a638-0001297861a6\"}") # move ccw

#mir.do('/positions')
#mir.put('/positions',"{\"pos_x\": 1}") 
#a= mir.check('/mission_queue') # get mission list
#print(len(a)) # total number if missions

