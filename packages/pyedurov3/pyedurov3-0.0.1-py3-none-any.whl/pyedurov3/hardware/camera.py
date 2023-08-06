import logging
import picamera
from ..errors import errorDictionary

from ..utility import StreamingOutput


class Camera(object):
    def __init__(self, video_resolution, fps,error_list=list()):
        self.logger = logging.getLogger("Camera")
        self.stream = StreamingOutput()
        self.logger.info("video resolution: " + str(video_resolution))
        self.error_list = error_list
        try:
            self.camera = picamera.PiCamera(resolution=video_resolution, framerate=fps)
            self.camera.start_recording(self.stream, format='mjpeg')
        except Exception as e:
            self.logger.warning(e)
            self.logger.warning("Camera initialization failed, camera is not available")
            self.camera = None
            self.error_list.append(errorDictionary["cameraError1"])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.camera is not None:
            self.camera.close()
