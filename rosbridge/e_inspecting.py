from mir import MirInspect

mir = MirInspect()
#mir = MirInspect("192.168.1.111")
mir.connect()

mir.topic_list()
#mir.topic_echo('/camera_floor_left/driver/color/image_raw')
#input("Hit enter when you're done!")

mir.terminate()
