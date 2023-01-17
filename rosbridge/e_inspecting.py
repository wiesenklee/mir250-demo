import json

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
print("Connected!\n")

# Inspecting
print("Getting all available topics:")
l = mir.topic_list()
print(json.dumps(l, indent=3))

print()
print("Give a topic to echo (Press any key to aboard): ")
t = None
while t not in l: t = input()
t = mir.topic_start_echo(t)
input()
mir.topic_stop_echo(t)
mir.terminate()
