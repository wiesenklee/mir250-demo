from mir import MirInspect

sdt_host = "mir.com"

print(f"Enter mir's network-address: (hit enter to use '{sdt_host}')")
usr_host = input()
print("OK, Trying to connect to MiR...")

# Connecting to MiR
host = usr_host if len(usr_host) > 0 else sdt_host
mir = MirInspect(host)
try: mir.connect()
except:
  print("Cloud not connect to mir! Leaving...")
  exit()
print("Connected!")

# Inspecting
mir.topic_list()
mir.topic_echo('/camera_floor_left/driver/color/image_raw')
#input("Hit enter when you're done!")

mir.terminate()
