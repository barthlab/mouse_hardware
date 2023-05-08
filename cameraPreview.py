import picamera
import time



if "__main__" == __name__:
    with picamera.PiCamera() as camera:
        # TODO camera consistency?
        camera.resolution = (1024, 768)
        camera.start_preview()
        # TODO just hit ctrl+C to exit?
