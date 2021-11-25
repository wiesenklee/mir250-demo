import roslibpy

class MirManual:
    def __init__(self, host, port, session_id):
        self.host = host if len(host) > 0 else "misr.com"
        self.port = port if port else 9090
        self.id = session_id

    def __setupEndpoints(self):
        self.t_vel = roslibpy.Topic(
            self.client, '/joystick_vel', 'mirMsgs/JoystickVel')
        self.t_info = roslibpy.Topic(
            self.client, '/robot_status', 'mirMsgs/RobotStatus')
        self.t_safetyInfo = roslibpy.Topic(
            self.client, '/safety_status', 'mirMsgs/SafetyStatus')
        self.s_state = roslibpy.Service(
            self.client, '/mirsupervisor/setRobotState', 'mirSupervisor/SetState')
        self.s_errorReset = roslibpy.Service(
            self.client, '/mirsupervisor/requestErrorReset', 'std_srv/Empty')

    def connect(self):
        self.client = roslibpy.Ros(host=self.host, port=self.port)
        self.client.run()
        
        if self.client.is_connected:
            self.__setupEndpoints()
        return self.client.is_connected

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
        s = self.s_state
        req = roslibpy.ServiceRequest({
            'robotState': 11,
            'web_session_id': self.id
        })
        rep = s.call(req)
        self.token = rep['joystick_token']

    def callPauseMode(self):
        s = self.s_state
        req = roslibpy.ServiceRequest({'robotState': 4})
        s.call(req)

    def move(self, x, z):
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

    def terminate(self):
        self.client.terminate()