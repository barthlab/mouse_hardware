import picamera
import time



if "__main__" == __name__:
    save_dir='vids/'

    # TODO how to record to desktop?

    with picamera.PiCamera() as camera:
        # TODO camera consistency?
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(10) # TODO need to determine when finished
        camera.start_recording(f"mouse_video_{time.time()}.h264")
        camera.wait_recording(30)
        camera.stop_recording()

    
