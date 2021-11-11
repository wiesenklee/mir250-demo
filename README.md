# Quickstart MiR250

Links:

- Quickstart: https://www.mobile-industrial-robots.com/media/12722/mir250_quick_start_1-4_en.pdf
- Detailed Guide: https://www.mobile-industrial-robots.com/media/12739/mir250_user_guide_1-4_en.pdf
- Web-interface Guide: https://www.mobile-industrial-robots.com/media/13758/mir-robot-reference-guide-23_en.pdf

> In this document the MiR250 roboter is referred as MiR

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

### Authorization
The web-interface will ask for authorization when it will be opened the first time. Once logged in, the credentials are saved via cookies.

Stock username and password are:

**Username**: Distributor -  **Password**: distributor

## Using the REST API

> The REST API is working parallel to the web-interface. In every situation the web-interface is used, the REST API will also work.

> 🚨  MANUAL DRIVING MODE NOT WOKRING 

Documentation: https://www.mobile-industrial-robots.com/media/13736/mir_mir250_rest_api_21302.pdf

### Get Started with Python

Look at some code-examples in [./RESTAPI](./RESTAPI). In [./RESTAPI/test.py](./RESTAPI/test.py) there is a unfinished library to easy-controll the API. Code-snippets are also there

## Using the ROSBRIDGE