import argparse
import logging
from ..system import setup_startup

def run():

    parser = argparse.ArgumentParser(
        description='Start the Engage eduROV web server')
    parser.add_argument(
        '-r',
        metavar='RESOLUTION',
        type=str,
        default='1280x720',
        help='''resolution, use format WIDTHxHEIGHT (default 1280x720)''')
    parser.add_argument(
        '-fps',
        metavar='FRAMERATE',
        type=int,
        default=30,
        help='framerate for the camera (default 30)')
    parser.add_argument(
        '-port',
        metavar='SERVER_PORT',
        type=int,
        default=8080,
        help="which port the server should serve it's main page (default 80)")
    parser.add_argument(
        '-serial',
        metavar='SERIAL_PORT',
        type=str,
        default=None,
        help="which serial port the script should try to use to communicate with the Arduino module")
    parser.add_argument(
        '--loglevel',
        type=str,
        default='INFO',
        help='Set log level')
    parser.add_argument(
        '--runatstartup',
        action='store_true',
        help='Setup server to run at startup and exit program. Must be run as sudo')
    parser.add_argument(
        '--name',
        type=str,
        default='edurov',
        help='Set server advertising name. Defaults to "edurov"')

    args = parser.parse_args()

    if args.runatstartup:
        print("Setting up pyedurov3 to execute at startup.")
        setup_startup(args.name)
        return

    from .cameraserver import CameraServer
    from .ioserver import IOServer
    from .webserver import WebServer
    from .advertising import AdvertisingServer, wait_until_available
    
    from .localui import LocalUi

    import multiprocessing
    
    manager = multiprocessing.Manager()
    #manager.start()

    system_status = manager.dict()

    #For testing
    from ..errors import errorDictionary
    
    #activeErrors.append(errorDictionary["cameraError1"])

    system_status["batteryVoltage"] = 0.0
    system_status["ip"]="0.0.0.0"
    system_status["lastUplinkMsg"]=0
    system_status["lastDownlinkMsg"]=0
    system_status["cameraOnline"]=False

    logging.basicConfig(level=args.loglevel)

    wait_until_available()

    logging.info("Network service is available, starting servers.")

    ioserver = IOServer(args.serial, loglevel=args.loglevel,system_status=system_status)
    camera = CameraServer(args.r, args.fps, args.loglevel,system_status=system_status)
    uiserver = LocalUi(loglevel=args.loglevel,system_status=system_status)
    #advertisingserver = AdvertisingServer(loglevel=args.loglevel, name=args.name)
    webserver = WebServer(loglevel=args.loglevel, port = args.port)

    #ioserver.ready.wait()
    #camera.ready.wait()

    #webserver.ready.wait()
    uiserver.ready.wait()

    uiserver.join() # The local ui is the very last thing that should be alive

    try:
        ioserver.join()
    except KeyboardInterrupt:
        logging.info("Stopped by Keyboard interrupt")
        logging.info("Killing other services and exiting program.")
        camera.stop()
        uiserver.stop()
        manager.close()
    
    logging.info("I/O server stopped. Killing other services and exiting program.")

    camera.stop()
    uiserver.stop()
    manager.close()
    
if __name__ == '__main__':
    run()
