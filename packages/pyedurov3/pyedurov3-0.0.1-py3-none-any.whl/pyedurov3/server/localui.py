import logging
import multiprocessing
import asyncio
import time
import os

from ..hardware import display,button,led

from ..errors import errorDictionary

BUTTON_GPIO = 26
GREEN_LED = 19

from ..utility import get_host_ip

SHUTDOWN_HOLD_TIME = 10
SCREEN_SWITCH_TIME = 10

UPLINK_TIMEOUT = 2.0

class LocalUi(multiprocessing.Process):
    """ Creates a new process"""
    def __init__(self, loglevel="INFO",system_status=multiprocessing.Manager().dict()):

        print("Local UI init")
        self.loglevel = loglevel
        self.start_time = time.time()
        self.ready = multiprocessing.Event()
        self.stop_event = multiprocessing.Event()

        self.system_status = system_status
        self.error_list = list()
        #self.button_down = multiprocessing.Value('b',0)

        self.menu_positions = [0,0]
        self.menu_level = 0

        self.click_event = multiprocessing.Event()
        self.double_click_event = multiprocessing.Event()
        self.long_press_event = multiprocessing.Event()

        self.button = None
        self.display = None
        self.led = None

        self.last_countdown_update = 0
        self.last_menu_update = 0

        self.last_system_check = 0

        self.error_count = 0

        super().__init__(target=self._runner, daemon=False)
        self.start()

    async def stop(self):
        self.stop_event.set()
        self.join()
        logging.debug("Local Ui process terminated")

    async def _wait_for_stop_event(self):
        while not self.stop_event.is_set():
            await asyncio.sleep(2)

    def _runner(self):
        asyncio.run(self._task())

    async def _task(self):
        logging.basicConfig(level=self.loglevel)
        self.logger = logging.getLogger("LocalUI")

        display_online = False

        display_online = self._init_display()

        while not display_online:
            display_online = self._init_display()
            await asyncio.sleep(5)

        error_active = multiprocessing.Value('i',0)

        self.led = led.Led(error_active)
        self.button = button.Button(BUTTON_GPIO,self.click_event,self.double_click_event,self.long_press_event,SHUTDOWN_HOLD_TIME)
        
        self.button.ready.wait()
        self.led.ready.wait()
        self.ready.set()

        while not self.stop_event.is_set():

            self.error_list = self._check_system_status()
            new_error_count = len(self.error_list)
            error_active.value = 1 if new_error_count > 0 else 0
            
            if( ( self.error_count==0 ) and ( new_error_count > 0 )):
                self.menu_positions[0] = 1
            elif(new_error_count < self.error_count):
                self.menu_positions[0] %= new_error_count+1

            if(new_error_count != self.error_count):
                self.logger.info("errors changed")
                self._update_display()
                self.last_menu_update = time.time()

            self.error_count = new_error_count

            if self.click_event.is_set():
                #print("showing next screen")
                self._next_screen()
                self.click_event.clear()
                self.last_menu_update = time.time()

            #if self.double_click_event.is_set():
            #    self._switch_level()
            #    self.double_click_event.clear()
            #    self.last_menu_update = time.time()

            if self.long_press_event.is_set():
                print("Shutdown !!!")
                self.display._clear_oled()
                self.long_press_event.clear()
                self.last_menu_update = time.time()
                os.system("sudo shutdown -h now") #Requires root priveliges or allowing the user to issue shutdown withour PW

            if not self.button.pressed():
                if (time.time()-self.last_menu_update) > SCREEN_SWITCH_TIME:
                    if self.menu_level == 0:
                        #print("showing next screen")
                        self._next_screen()
                    elif self.menu_level == 1:
                        self._switch_level()
                    self.last_menu_update = time.time()

            else:
                hold_time = self.button.hold_duration()
                if (hold_time > 5) and ((time.time()-self.last_menu_update) > 1):
                    self.display.show_shutdown_warning((SHUTDOWN_HOLD_TIME - round(hold_time)) + 1)
                    self.last_menu_update = time.time()
            
            await asyncio.sleep(0.2)

        self.led.show_status(0)
        self.button.stop()
        self.logger.info('Shutting down localui')
        finish = time.time()
        seconds = finish - self.start_time
        self.logger.debug(f'Server was live for {seconds:.1f} seconds')
    
    def _init_display(self):
        try:
            self.display = display.Display()
            return True
        except IOError as e:
            self.logger.info("IOError occoured during OLED init")
            self.logger.info(e)
            return False    

        except Exception as e:
            self.logger.info("IOError occoured during OLED init")
            self.logger.info(e)
            return False
        
    def _check_system_status(self):
        #self.logger.info(self.system_status)
        error_list = list()
        if ( self.system_status["ip"] == "0.0.0.0" ) or ( self.system_status["ip"] == "127.0.0.1" ):
            error_list.append(errorDictionary["E1"])

        if not self.system_status["cameraOnline"]:
            error_list.append(errorDictionary["E2"])

        time_since_last_msg = time.time() - self.system_status["lastUplinkMsg"]
        #self.logger.info(time_since_last_msg)
        if ( time_since_last_msg > UPLINK_TIMEOUT):
            error_list.append(errorDictionary["E3"])

        #TODO: the limit should later be updated to reflect the actual settings on the microcontroller.
        #This requires capturing them in the IO server and transferring them here through a managed object
        if self.system_status["batteryVoltage"] < 10.0 : 
            error_list.append(errorDictionary["E6"])

        #self.last_system_check = time.time()
        return error_list
    
    def _update_display(self):
        errorsAvailable = self.error_list

        if self.menu_level == 0:
            if self.menu_positions[0] == 0:
                ip = str(get_host_ip())
                self.system_status["ip"] = ip    
                content = "IP: "+str(ip) + " Voltage: " + str(self.system_status["batteryVoltage"]) + " V "
                content += "Errors: " + str(len(self.error_list))
                self.logger.info(content)
                self.display.show_status(content)
            elif errorsAvailable:
                error = self.error_list[self.menu_positions[0]-1]
                self.display.show_error(error)
        elif self.menu_level == 1:
            error = self.error_list[self.menu_positions[0]-1]
            if self.menu_positions[1] == 0:
                self.display.show_error_details(error)
            elif self.menu_positions[1] == 1:
                self.display.show_error_help(error)

    def _next_screen(self):
        if self.menu_level == 0:
            self.menu_positions[0] += 1
            if self.menu_positions[0] >= (len(self.error_list) + 1):
                self.menu_positions[0] = 0
        elif self.menu_level == 1:
            self.menu_positions[1] += 1
            self.menu_positions[1] %= 2 

        #print("Next Screen:" + str(self.menu_positions))
        self._update_display()

    def _switch_level(self):
        self.menu_positions[1] = 0
        self.menu_level = not self.menu_level
        self._update_display()
