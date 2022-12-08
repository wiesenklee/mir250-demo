# Quickstart MiR250

Links:

- Quickstart: https://www.mobile-industrial-robots.com/media/12722/mir250_quick_start_1-4_en.pdf
- Detailed Guide: https://www.mobile-industrial-robots.com/media/12739/mir250_user_guide_1-4_en.pdf
- Web-interface Guide: https://www.mobile-industrial-robots.com/media/13758/mir-robot-reference-guide-23_en.pdf

> **In this document the MiR250 roboter is referred as MiR**

## Using the web-interface

The MiR can be maintained and controlled by a web-interface. Access ist gained by connecting to the network the MiR is
connected to. These networks can be of two different types: The network **hosted** by the MiR itself or a network the
MiR is **connected** to.

### MiR-hosted network
Out of the box the MiR will host its own wifi-network. It will be present, even if the MiR is connected to multiple
other networks at the same time. Therefore, it can be used as a backup network, in case other networks fail.

The web-interface can then be accessed via http://mir.com

### Additional networks 
In order to add an additional network, connect to the MiR-hosted network and open the web-interface. Open the system tab and jump into Settings -> Wifi. Use 'Add connection' to add an additional network.

The web-interface will than be accessed via the IP-address the MiR will be given

> ⚠️ A connection to the MiR through an additional network is **very unstable**. Hint: Connect to MiR's own network and use your phone via USB tethering to have internet available on your device.

### Authorization
The web-interface will ask for authorization when it will be opened the first time. Once logged in, the credentials are saved via cookies.

Stock username and password are:

**Username**: Distributor -  **Password**: distributor

## Using MiR with REST API

> ⚠️ Manual Driving Mode not working with REST API

> **The the web-interface is based on the REST API.** In every situation the web-interface is used, the REST API will also work. 

Documentation: https://www.mobile-industrial-robots.com/media/13736/mir_mir250_rest_api_21302.pdf

### Getting Started

Look at some code-examples in [./rest_api](./rest_api). There is a unfinished library in [./rest_api/test.py](./rest_api/test.py)  to easy-controll the API. Code-snippets are also there.

## Using MiR with rosbridge

The *rosbridge* is a service hosted on the MiR that enables interaction with the ROS-system via network (a websocket). Thr MiR hosts a **server** and any network-device can connect as a **client**. There are java, javascript and python libraries that help with the client-server communication. For communication the JSON-standart is used.

Documentation: http://wiki.ros.org/rosbridge_suite

Python-Client: https://github.com/gramaziokohler/roslibpy

### Getting Started 

0. Having *python3* and *pip3* installed.
1. Install *python-client* for rosbridge

    `$ pip install roslibpy`
2. Connect to MiR's network
3. Run [./rosbridge/e_inspecting.py](./rosbridge/e_inspecting.py)

    `$ python3 ./rosbridge/e_inspecting.py`

    If a huge list of endpoints is returned, client-server communication is working.
4. Run [./rosbridge/e_manual_control.py](./rosbridge/e_manual_control.py)

    `$ python3 ./rosbridge/e_manual_control.py`

    Follow instructions and you should be able to manually control the MiR

For further informations, look at the package [./rosbridge/mir.py](./rosbridge/mir.py)

### Integrate MiR in other ROS system

The MiR can also act as a node in another ROS system. 

0. Having done [Getting Started](#getting-started-1) for rosbridge
1. Install *python-node* for ROS  

    `$ pip install rospy`
2. Make sure you are connected to MiR's network
3. Make sure your ROS core is running
4. Run [./rosbridge/e_ros.py](./rosbridge/e_ros.py)

    `$ python3 ./rosbridge/e_ros.py`

    Now, the topics `/mir/robotState` and `/mir/cmd_vel` are available.

For further informations, look at the package [./rosbridge/mir_ros.py](./rosbridge/mir_ros.py)

### Using Dockerfile
Docker can be used to obtain ROS-functionality on machines that is not nativly running ROS (e.g. Ubuntu 22.04 for noetic). To use this program with docker you first need to build an image using the [./Dockerfile](./Dockerfile) *(of course, docker needs to be installed)*

```
docker buid -t mir .
```

Then start a docker container. The option `-it` is used for having an interactive terminal. `--net="host"` will use the host network, so the MiR can be found via IP.

```
docker run -it --net="host" mir 
```

If you need a second terminal while container is running, use this:

```
docker exec -it <CONTAINER_ID> bash
$ source /opt/ros/<ROS_DISTRO>/setup.bash
```
