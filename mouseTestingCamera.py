import picamera
import time



if "__main__" == __name__:
    save_dir='videos'

    with picamera.PiCamera() as camera:
        camera.start_recording(f"{save_dir}/mouse_video_{time.time()}.h264")
        camera.wait_recording(30) # TODO need to determine when finished recording (in other code, passed to this code)
        camera.stop_recording()

    # TODO extract pupils using opencv
    # https://subscription.packtpub.com/book/application-development/9781785283932/4/ch04lvl1sec44/detecting-pupils
    # https://tech.paayi.com/pupil-detection-in-pyhton
    # https://stackoverflow.com/questions/31658729/detecting-exact-pupil-diameter-in-python-and-opencv
