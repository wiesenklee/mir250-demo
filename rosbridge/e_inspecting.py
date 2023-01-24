import json

from mir import MirInspect

# Set Host
sdt_host = "192.168.12.20"

print(f"Enter mir's network-address (hit enter to use '{sdt_host}'): ", end="")
usr_host = input()
print("Trying to connect to MiR...")

# Connecting to MiR
host = usr_host if len(usr_host) > 0 else sdt_host
mir = MirInspect(host)
try: mir.connect()
except:
  print("Cloud not connect to mir! Leaving...")
  exit()
print("Connected!\n")

# Command Mode

c = None

while True:
  print("\nAvailable commands:")
  print("l - list all topics")
  print("e - echo specific topic")
  print("x - terminate and exit")
  print("> ", end="")
  c = input()
  print()

  match c[0]:

    case "l":
      print("Getting all topics...")
      l = mir.topic_list()
      l.sort()
      for i in l: print(i)

    case "e":
      t_name = c[2:] # Get topic name from command
      if len(c) <= 1:
        print("Give a topic to echo: ", end="")
        t_name = input()
      t = mir.topic_start_echo(t_name)
      print("Started echoing, press enter to stop ...")
      input()
      mir.topic_stop_echo(t)
    
    case "x":
      mir.terminate()
      exit()

    case _:
      print("Unknown command!")
