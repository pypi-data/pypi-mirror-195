import logging
import multiprocessing
import asyncio
import time

from pathlib import Path

from ..utility import get_host_ip

from ..errors import errorDictionary


"""
Sever classes used in the web method
"""

import http.server
import socketserver

class WebServer(multiprocessing.Process):
    """ Creates a new process that Exposes the raspberry pi camera as a websocket image stream """
    def __init__(self, loglevel="INFO", port=8080):
        self.port = port
        self.loglevel = loglevel

        self.start_time = time.time()
        self.server = None
        self.ready = multiprocessing.Event()
        self.stop_event = multiprocessing.Event()

        super().__init__(target=self._runner, daemon=True)
        self.start()

    async def stop(self):
        self.stop_event.set()
        self.join()
        logging.debug("Webserver process terminated")

    async def _wait_for_stop_event(self):
        while not self.stop_event.is_set():
            await asyncio.sleep(2)

    def _runner(self):
        asyncio.run(self._task())

    async def _task(self):
        webdir = Path(__file__).parent.parent.joinpath("web")

        logging.basicConfig(level=self.loglevel)
        self.logger = logging.getLogger("WebServer")
        
        print("Starting HTTP Server")

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=webdir, **kwargs)


        server_online = False

        while not self.stop_event.is_set():

            while not server_online:
                try:
                    httpd = socketserver.TCPServer(("", self.port), Handler)
                    server_online = True
                except Exception as e:
                    self.logger.info("failed to init socket")
                    server_online = False
                    await asyncio.sleep(5)

            with httpd:
                print("serving at port", self.port)
                self.ready.set()
                httpd.serve_forever()

        self.logger.info('Shutting down webserver')
        finish = time.time()
        seconds = finish - self.start_time
        self.logger.debug(f'Server was live for {seconds:.1f} seconds')

