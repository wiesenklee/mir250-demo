import time
import json
import roslibpy
import curses

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


def log(string, line, screen):
    screen.addstr(line, 0, string)
    screen.clrtoeol()
    screen.refresh()


def start_controlling(mir, screen):
    mir.callManualMode()
    mir.subToSafetyInfo()
    # waiting for data from mir
    while not hasattr(mir, 'safetyInfo'):
        pass

    log("Press blue button on robot to unlock manual mode.", 0, screen)
    # waiting for button press
    while mir.safetyInfo['is_manual_mode_restart_required']:
        pass
    log("Now use the arrowkeys to move robot. Press 'q' to quit.", 0, screen)

    x = 0
    z = 0

    while True:
        arrow_key = curses.initscr().getch()

        if arrow_key == ord('q'):
            break

        if arrow_key == curses.KEY_UP:
            x = 0.3
        elif arrow_key == curses.KEY_DOWN:
            x = -0.3
        else: x = 0

        if arrow_key == curses.KEY_RIGHT:
            z = -0.3
        elif arrow_key == curses.KEY_LEFT:
            z = 0.3
        else: z = 0

        log(f"X: {str(x)} Y:{str(z)}", 1, screen)
        mir.move(x, z)

def end_controlling(mir, screen):
    # Close websocket connectin to mir
    mir.callPauseMode()
    mir.terminate()

    # Restore terminal
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def main():
    session_id = '03bdbug5tprmn0q7l00b742vh7'  # extracted from web-interace
    sdt_host = "mir.com"

    print(f"Enter mir's network-address: (hit enter to use '{sdt_host}')")
    usr_host = input()
    print("OK, Trying to connect to MiR...")

    # Connecting to MiR
    host = usr_host if len(usr_host) > 0 else sdt_host
    mir = MirManual(host, 9090, session_id)

    try:
        mir.connect()
    except:
        print("Cloud not connect to mir! Leaving...")
        return

    print("Connected!")
    print("Starting user interface for manual control...\n")

    # Setting up user-interface
    screen = curses.initscr()
    screen.keypad(True)
    curses.noecho()
    curses.cbreak()

    try:
        start_controlling(mir, screen)
    finally:
        # Making sure the connection to MIR is always closed savely
        end_controlling(mir, screen)
        print("Back to terminal and closed connection to mir safely.")

main()
