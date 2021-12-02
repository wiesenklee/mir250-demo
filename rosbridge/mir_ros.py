import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

from mir import MirManual

class MirManual_Ros():
    def __init__(self, host="mir.com", port=9090, session_id=None):        
        self.host = host
        self.port = port
        self.session_id = session_id

    def connectToMir(self):
        self.mir = MirManual(self.host, self.port, self.session_id)
        self.mir.connect()

    def connectToRos(self):
        rospy.init_node('mirmanual_ros')
        rospy.Subscriber('mir/cmd_vel', Twist, callback=self.__onCmdVel)
        rospy.Subscriber('mir/robotState', Int8, callback=self.__onRobotState)

    def __mirIsConnected(self):
        if self.mir.client.is_connected: return True
        print("can not reach mir...")
        return False

    def __onCmdVel(self, m):
        if not self.__mirIsConnected(): return 
        self.mir.move(m.linear.x, m.angular.z)

    def __onRobotState(self, m):
        if not self.__mirIsConnected(): return 
        if m.data == 11:
            self.mir.callManualMode()
        if m.data == 4:
            self.mir.callPauseMode()
