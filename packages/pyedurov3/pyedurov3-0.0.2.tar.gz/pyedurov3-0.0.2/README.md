# EduROV server package

This package contains a companion computer code for use with the eduROV 4 hardware. The package is called pyedurov3. It is supposed to run on a Raspberry Pi 3 or 4.

## Use
- To install, run ```pip install pyedurov3```.
  - If you got the warning ```The script normalizer is installed in * which is not on PATH.```, call ```source ~/.profile```.
- To run the server, run ```pyedurov3```.
- To start the server at boot, run ```sudo pyedurov3 --runatstartup```.
- See ```pyedurov3 --help``` for more options.

## Setting up Raspberry Pi for EduROV with a fresh image
-Install the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/) tool
- Insert your SD card into a card reader
- Use the tool to install Raspberry PI OS (32-bit) onto the card
- Don't forget to configure the image to use SSH before writing it
- Insert sd card to Raspberry Pi
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

## Building package (and tips for developers)

For development, you will have to build modified versions of the package from source.
Make sure the newest version of pip is installed: ```pip install --upgrade build```
Then navigate into the upper pyedurov3 folder and run ```python -m build``` (you might have to use sudo for that).

In development it can be helpful to quickly reinstall the package without debendencies. A helpful command is this:
python3 -m pip install --upgrade --force-reinstall --no-deps dist/pyedurov3-0.0.0.tar.gz.
The source code can alos be run from the run.py file so you don't have to rebuild the package every time you change something. Just navigate into the upper pyedurov3 folder and type ```python3 -m run.py```


