# EduROV server package

This package contains a server for use with the [circuit boards](https://github.com/simtind/edu-rover2-pcb) and [PC client](https://github.com/simtind/edu-rover2-client) from the pyedurov3 project, and the ROV chassis described on the EduROV webpage.

## Use
- To install, run ```pip install pyedurov3```.
  - If you got the warning ```The script normalizer is installed in * which is not on PATH.```, call ```source ~/.profile```.
- To run the server, run ```pyedurov3```.
- To start the server at boot, run ```pyedurov3 --runatstartup```.
- See ```pyedurov3 --help``` foor more options.

## Building package

Make sure the newest version of pip is installed: ```pip install --upgrade build```
Then from the edurov_server folder, run ```python -m build```

## Setting up Raspberry pi for EduROV

- Install Raspberry PI OS (32-bit), for example via [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
- In SD card, add the file "ssh", it should be empty.
- Insert sd card to raspberry pi
- Connect via ssh to raspberrypi.local
- Via raspi-config:
  - Under Interface Options
    - Enable camera
    - Enable Serial Port:
      - We do not want a login shell to be available.
      - We do want the serial port hardware to obe enabled.
  - Allow the raspberry pi to restart and reconnect the ssh session.
- For pyedurov3 to run at startup, we'll need to install and run it as sudo.
- Install pyedurov3 with ```sudo pip install pyedurov3```
- Call ```sudo pyedurov3 --runatstartup --name=yourname``` to set server to start at boot with "yourname" as the advertising name.
