import picamera
import picamera.array
import time
import cv2
from matplotlib import pyplot as plt

with picamera.PiCamera() as camera:
    cap=picamera.array.PiRGBArray(camera)
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(3)
    camera.capture(cap,format="bgr")
    img=cap.array
    
plt.figure().canvas.set_window_title("Hello Raspberry Pi")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
