import logging
import time
import asyncio
import multiprocessing

import RPi.GPIO as GPIO

MID_PRESS_DURATION = 2

UPDATE_INTERVAL = 0.1

class Button(multiprocessing.Process):
    def __init__(self, gpio, click_event, mid_press_event, long_press_event, long_press_duration=10, loglevel="INFO"):

        self.loglevel = loglevel
        
        self.gpio = gpio

        self.click_event =click_event
        self.mid_press_event = mid_press_event
        self.long_press_event = long_press_event

        self.long_press_duration=long_press_duration

        self.last_down = multiprocessing.Value('d',0)
        self.last_up = multiprocessing.Value('d',0)

        self.pulse_count = multiprocessing.Value('i',0)

        self.ready = multiprocessing.Event()
        self.stop_event = multiprocessing.Event()

        self.detection_started = multiprocessing.Event()

        self.mid_event_sent = multiprocessing.Event()

        self._setup_gpio()

        super().__init__(target=self._runner, daemon=True)
        self.start()
    
    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.gpio, GPIO.BOTH,callback=self._button_callback,bouncetime=20)

    def pressed(self):
        return GPIO.input(self.gpio) == 0

    def hold_duration(self):
        duration = 0
        if self.detection_started.is_set():
            duration = time.time() - self.last_down.value
        return duration

    async def stop(self):
        self.stop_event.set()
        GPIO.remove_event_detect(self.gpio)
        GPIO.cleanup()
        self.join()
        logging.debug("Button process terminated")

    def _runner(self):
        asyncio.run(self._task())

    def _button_callback(self,channel):
        if GPIO.input(channel) == 0:
            #print("Down")
 
            self.last_down.value = time.time()
            self.detection_started.set()     

        else:
            #print("Up")
            self.last_up.value = time.time()

            if self.detection_started.is_set():
                if self.hold_duration() < MID_PRESS_DURATION:
                    self.click_event.set()
                self.detection_started.clear()
                self.mid_event_sent.clear()
            
            if hasattr(self,'logger'):
                self.logger.info("button was held down for:" + str(self.last_up.value - self.last_down.value) + " s")

    async def _task(self):
        
        logging.basicConfig(level="INFO")
        self.logger = logging.getLogger("Button")
        self.ready.set()

        while not self.stop_event.is_set():
            
            if  self.detection_started.is_set() and not self.pressed(): # Up Edge was not detected by interrupt, happens quite often
                    self.click_event.set()
                    self.mid_event_sent.clear()
                    self.detection_started.clear()

            if self.detection_started.is_set():

                duration = self.hold_duration()
                #print(duration)

                if (duration > MID_PRESS_DURATION) and not self.mid_event_sent.is_set():
                    print("Mid press detected")
                    self.mid_press_event.set()
                    self.mid_event_sent.set()

                if duration > self.long_press_duration:
                    print("Long Press detected")
                    self.long_press_event.set()
                    self.detection_started.clear()

            await asyncio.sleep(UPDATE_INTERVAL)