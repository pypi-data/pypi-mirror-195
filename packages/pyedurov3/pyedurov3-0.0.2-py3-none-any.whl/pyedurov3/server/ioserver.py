import json
import logging
import multiprocessing
import asyncio
import time

import websockets as websockets

from ..hardware import arduino
from ..hardware import system
from ..utility import get_host_ip


class IOServer(multiprocessing.Process):
    """ Creates a new process that Exposes the Arduino, sense hat, and system sensors and actuators as a websocket data stream """
    def __init__(self, arduino_serial_port=None, arduino_baud_rate=115200, loglevel="INFO", port=8082, system_status = dict()):
        self.port = port
        self.serial_port = arduino_serial_port
        self.baud_rate = arduino_baud_rate
        self.loglevel = loglevel
        self.sensors = dict()
        self.actuators = dict()
        self.start_time = time.time()
        self.sensor_queue = None
        self.actuator_queue = None
        self.server = None
        self.ready = multiprocessing.Event()
        self.stop_event = multiprocessing.Event()
        self.logger = logging.getLogger("IOServer")

        self.system_status = system_status

        super().__init__(target=self._runner, daemon=True)
        self.start()

    async def stop(self):
        self.stop_event.set()
        self.join()
        logging.debug("I/O process terminated")
    
    async def _collect_autopilot_board_upstream(self,system_status):
        while not self.stop_event.is_set():
            # Don't get arduino data if we're not serving clients.
            try:
                message = await self.arduino.get_upstream()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                self.logger.info("arduino message exception")
                await asyncio.sleep(5)
            #self.logger.info(message)
            
            if message.get("sensors",{}).get("batteryVoltage"):
                system_status["lastUplinkMsg"] = time.time()
                system_status["batteryVoltage"] = message["sensors"]["batteryVoltage"]
                #self.logger.info(self.system_status["batteryVoltage"]) Works
            
            if self.server:
                if self.server.ws_server.websockets:
                    await self.sensor_queue.put(message)
                    await self.sensor_queue.join()
            #else:
             #   await asyncio.sleep(1)

    async def _collect_system_data(self):
        raspberry = system.SystemMonitor()
        while not self.stop_event.is_set():
            # Don't get arduino data if we're not serving clients.
            if self.server:
                if self.server.ws_server.websockets:
                    logging.debug("Get system data")
                    await self.sensor_queue.put(await raspberry.get_system_data())
                    await self.sensor_queue.join()
            
            await asyncio.sleep(1)

    async def _send_upstream(self, websocket):
        while not self.stop_event.is_set():
            # empty the sensor queue before sending the data update.
            sensorMsg = dict()
            while not self.stop_event.is_set():
                sensorMsg = await self.sensor_queue.get()
                empty = self.sensor_queue.empty()
                self.sensor_queue.task_done()
                if empty:
                    break
            
            #self.logger.debug("Send arduino data to client")
            if( sensorMsg.get("outputSettings")):
                self.logger.info(f"Autopilot Board <- settings data {sensorMsg}")
            await websocket.send(json.dumps(sensorMsg))

        # Drain the sensor queue so the other tasks can exit as well.
        while not self.sensor_queue.empty():
            self.sensors.update(await self.sensor_queue.get()) 
            self.sensor_queue.task_done()

    async def _receive_input(self, websocket):
        while not self.stop_event.is_set():
            #self.logger.debug("Wait for incoming websocket data")
            jsonString = await websocket.recv()
            data = json.loads(jsonString)
            if( data.get("outputSettings")):
                self.logger.info(f"Frontend -> settings data {data}")

            self.arduino.send_downstream(json.dumps(data))

    async def _handler(self, websocket, path):
        self.logger.info(f"I/O server received connection from {path}")
        await websocket.recv()
        send = asyncio.create_task(self._send_upstream(websocket))
        receive = asyncio.create_task(self._receive_input(websocket))
        await websocket.wait_closed()
        await send
        await receive

    def _init_websocket(self):
        try:
            self.server = websockets.serve(self._handler, get_host_ip(), self.port)
            return True
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.logger.info("Websocket failed")
            self.logger.info(e)
            return False

    def _runner(self):
        asyncio.run(self._task())

    async def _task(self):
        logging.basicConfig(level=self.loglevel)
        self.logger = logging.getLogger("I/OServer")
        self.sensor_condition = asyncio.Condition()
        self.actuator_lock = asyncio.Lock()
        self.sensor_queue = asyncio.Queue()
        self.actuator_queue = asyncio.Queue()

        #while not self._init_websocket:
           # await asyncio.sleep(5)

        self.server = websockets.serve(self._handler, get_host_ip(), self.port)
        
        self.logger.info(f"I/O websocket server started at ws://{get_host_ip()}:{self.port}")

        async with arduino.Arduino(self.serial_port, self.baud_rate) as self.arduino:
            arduino_task = asyncio.create_task(self._collect_autopilot_board_upstream(self.system_status))
            #hat_task = asyncio.create_task(self._collect_sense_hat_sensors())
            system_task = asyncio.create_task(self._collect_system_data())
            self.logger.debug("Ready to send sensor data")

            self.ready.set()

            await self.server
            await arduino_task
            #await hat_task
            await system_task


        self.ready.set()
        self.logger.info('Shutting down server')
        finish = time.time()
        seconds = finish - self.start_time
        self.logger.debug(f'Server was live for {seconds:.1f} seconds')
