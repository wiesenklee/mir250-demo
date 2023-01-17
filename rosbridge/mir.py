import roslibpy

class MirInspect:
    def __init__(self, host="mir.com", port=9090):
        self.host = host
        self.port = port
    
    def __createTopic(self, c, t_name):
        try:
            t_type = c.get_topic_type(t_name, callback=None)
        except:
            print("Error getting informations of topic: " + t_name)
            return None
        return roslibpy.Topic(c,t_name,t_type)

    def connect(self):
        try: self.client = roslibpy.Ros(host=self.host, port=self.port)
        except Exception: 
            print("Could not connect to ROS")
            return False

        self.client.run()
        return True

    def terminate(self):
        self.client.terminate()
        
    def topic_list(self):
        return self.client.get_topics(callback=None)

    def topic_start_echo(self, t_name):
        t = self.__createTopic(self.client, t_name)
        t.subscribe(lambda m: print(m))
        return t

    def topic_stop_echo(self, t):    
        t.unsubscribe()

class MirManual:
    def __init__(self, host="mir.com", port=9090, session_id=None):
        self.host = host
        self.port = port
        self.id = session_id

    def __setupEndpoints(self):
        self.t_vel = roslibpy.Topic(
            self.client, '/joystick_vel', 'mirMsgs/JoystickVel')
        self.t_info = roslibpy.Topic(
            self.client, '/robot_status', 'mirMsgs/RobotStatus')
        self.t_safetyInfo = roslibpy.Topic(
            self.client, '/safety_status', 'mirMsgs/SafetyStatus')
        self.s_setState = roslibpy.Service(
            self.client, '/mirsupervisor/setRobotState', 'mirSupervisor/SetState')
        self.s_errorReset = roslibpy.Service(
            self.client, '/mirsupervisor/requestErrorReset', 'std_srv/Empty')
        self.s_speedMode = roslibpy.Service(
            self.client, '/mirsupervisor/joystick_mode', 'mir_srvs/JoysticksMode')

    def connect(self):
        try: self.client = roslibpy.Ros(host=self.host, port=self.port)
        except Exception: 
            print("Could not connect to ROS")
            return False

        self.__setupEndpoints()
        self.client.run()
        return True

    def terminate(self):
        self.client.terminate()

    def subToInfo(self):
        l = self.t_info

        def set_info(i):
            self.info = i
        l.subscribe(set_info)

    def subToSafetyInfo(self):
        l = self.t_safetyInfo

        def set_info(i):
            self.safetyInfo = i
        l.subscribe(set_info)

    def callManualMode(self):
        s = self.s_setState
        req = roslibpy.ServiceRequest({
            'robotState': 11,
            'web_session_id': self.id
        })
        rep = s.call(req)
        self.token = rep['joystick_token']

    def callPauseMode(self):
        s = self.s_setState
        req = roslibpy.ServiceRequest({'robotState': 4})
        s.call(req)

    def callSpeedLimit(self, b):
        s = self.s_speedMode
        req = roslibpy.ServiceRequest({
            'command': 2 if b else 3
        })
        s.call(req)

    def move(self, x, z):
        if not hasattr(self,'token'): return
        t = self.t_vel
        m = roslibpy.Message({
            'joystick_token': self.token,
            'speed_command': {
                'linear': {
                    'x': x,
                    'y': 0,
                    'z': 0
                },
                'angular': {
                    'x': 0,
                    'y': 0,
                    'z': z
                }
            }
        })
        t.publish(m)
