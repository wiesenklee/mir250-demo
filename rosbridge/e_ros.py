from mir_ros import MirManual_Ros

session_id = '03bdbug5tprmn0q7l00b742vh7'  # extracted from web-interace
sdt_host = "mir.com"

print(f"Enter mir's network-address: (hit enter to use '{sdt_host}')")
usr_host = input()
print("OK, Trying to connect to MiR...")

# Connecting to ROS and MiR
host = usr_host if len(usr_host) > 0 else sdt_host
mir = MirManual_Ros(host, 9090, session_id)

try: mir.connectToRos()
except:
  print("Cloud not connect to ROS! Leaving...")
  exit()
try: mir.connectToMir()
except:
  print("Cloud not connect to MiR! Leaving...")
  exit()

input("Hit enter when you're done!")