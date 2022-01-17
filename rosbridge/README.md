# Module for communicating with MiR250 using rosbridge through websocket

## Requirements
 - python3
 - pip3
 - pip-packages:
    - roslibpy
    - rospy

## Packages 
[mir.py](./mir.py) can be used to communcate directly to the MiR through websocket.

**MirInspecting** - Class for listing all available topics/endpoints of the MiR

**MirManual** - Class for moving the MiR forward (linear-x) and rotate (agular-z) 

[mir_ros.py](./mir_ros.py) can be used to integrate MiR in another ROS system

**MirManual_Ros** - Class derived from *MirManual*. Will open `/mir/robotState` and `/mir/cmd_vel` topics in ROS system.

## Examples

Python scripts starting with `e_` are executable examples.