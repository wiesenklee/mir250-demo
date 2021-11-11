import time
import keyboard
import roslibpy

class MirManual:
    def __init__(self, host, port, session_id):
        self.host = host if len(host) > 0 else "mir.com"
        self.port = port if port else 9090
        self.id = session_id

    def connect(self):
        self.client = roslibpy.Ros(host=self.host, port=self.port)
        self.client.run()
        if self.client.is_connected:
            self.setupEndpoints()
        return self.client.is_connected

    def setupEndpoints(self):
        self.vel_topic = roslibpy.Topic(
            self.client, '/joystick_vel', 'mirMsgs/JoystickVel')
        self.info_topic = roslibpy.Topic(
            self.client, '/robot_status', 'mirMsgs/RobotStatus')
        self.state_service = roslibpy.Service(
            self.client, '/mirsupervisor/setRobotState', 'mirSupervisor/SetState')

    def subToInfo(self):
        l = self.info_topic
        def set_info(i):
            self.info = i
        l.subscribe(set_info)

    def callManualMode(self):
        s = self.state_service
        req = roslibpy.ServiceRequest({
            'robotState': 11,
            'web_session_id': self.id
        })
        rep = s.call(req)
        self.token = rep['joystick_token']

    def move(self, x, z):
        t = self.vel_topic
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


def controlling_robot(mir):
    mir.callManualMode()
    input("press blue button on robot")

    while True:

        if keyboard.read_key() == "p":
            break

        while keyboard.read_key() == "w":
            mir.move(0.2, 0)

        while keyboard.read_key() == "s":
            mir.move(-0.2, 0)

        while keyboard.read_key() == "a":
            mir.move(0, 0.2)

        while keyboard.read_key() == "d":
            mir.move(0, -0.2)

        mir.move(0, 0)

    mir.terminate()

def main():
    session_id = '03bdbug5tprmn0q7l00b742vh7'
    mir = MirManual("192.168.1.111", 9090, session_id)
    mir.connect()

    # Making sure the connection to MIR is always closed savely
    try:
        controlling_robot(mir)
    except KeyboardInterrupt:
        mir.terminate()

main()