import picamera
import time

# TODO incorporate this into mouseTesting.py
SAVE_DIR='data'

if "__main__" == __name__:
  with picamera.PiCamera() as camera:
    camera.start_recording(f"{SAVE_DIR}/mouse_video_{time.time()}.h264")
    camera.wait_recording(30) # TODO need to determine when finished recording (in other code, passed to this code)
    camera.stop_recording()

    # TODO extract pupils using opencv
    # https://subscription.packtpub.com/book/application-development/9781785283932/4/ch04lvl1sec44/detecting-pupils
    # https://tech.paayi.com/pupil-detection-in-pyhton
    # https://stackoverflow.com/questions/31658729/detecting-exact-pupil-diameter-in-python-and-opencv
