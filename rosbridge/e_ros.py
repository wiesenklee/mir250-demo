from mir_ros import MirManual_Ros

id = '03bdbug5tprmn0q7l00b742vh7'  # extracted from web-interace
mir = MirManual_Ros(session_id=id)
mir.connectToRos()
mir.connectToMir()

input("Hit enter when you're done!")