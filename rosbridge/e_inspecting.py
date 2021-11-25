import roslibpy
import json

def createTopic(c, t_name):
    try:
        t_type = c.get_topic_type(t_name, callback=None)
    except:
        print("error getting topic informations")
        return 0
    return roslibpy.Topic(c,t_name,t_type)


# Connecting to MiR
client = roslibpy.Ros(host="mir.com", port=9090)
client.run()

topics = client.get_topics(callback=None)
print(json.dumps(topics, indent=3))

topic = createTopic(client, '/camera_floor_left/driver/color/image_raw')
topic.subscribe(lambda m: print(m))

input()

