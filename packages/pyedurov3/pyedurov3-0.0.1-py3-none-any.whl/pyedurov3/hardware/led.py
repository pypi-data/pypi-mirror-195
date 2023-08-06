import board
import digitalio
import logging
import time
import asyncio
import multiprocessing

class Led(multiprocessing.Process):
    def __init__(self, error_active, loglevel="INFO"):
        self.pin = board.D19
        self.led = None
        self.loglevel = loglevel
        self.ready = multiprocessing.Event()
        self.stop_event = multiprocessing.Event()
        self.interval = 1

        self.led = None
        self.error_active = error_active

        self._setup_led()
        super().__init__(target=self._runner, daemon=True)
        self.start()
    
    async def stop(self):
        self.stop_event.set()
        self.join()
        logging.debug("led process terminated")

    def _runner(self):
        asyncio.run(self._task())

    async def _task(self):
        logging.basicConfig(level=self.loglevel)
        self.logger = logging.getLogger("Led")
        self.ready.set()
        
        while not self.stop_event.is_set():
            
            if bool(self.error_active.value):
                self.interval = 0.3
            else:
                self.interval = 1.0

            await asyncio.sleep(self.interval)
            self.led.value = not self.led.value

    def _setup_led(self):
        self.led = digitalio.DigitalInOut(self.pin)
        self.led.direction = digitalio.Direction.OUTPUT