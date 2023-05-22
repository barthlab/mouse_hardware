# TODO this

import math

import cv2
import numpy as np

img = cv2.imread('ghjk.jpg')
scaling_factor = 1.5

img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(~img, cv2.COLOR_BGR2GRAY)

ret, thresh_gray = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#cv2.imshow('contours', thresh_gray)

for contour in contours:
    area = cv2.contourArea(contour)
    rect = cv2.boundingRect(contour)
    x, y, width, height = rect
    print(rect)
    centerx, centery = (x + width/2, y + height/2)
    radius = 0.25 * (width + height)

    fill_condition = (abs(1 - (area / (math.pi * math.pow(radius, 2.0)))) <= 0.2)

    if fill_condition:
        cv2.circle(img, (int(x + radius), int(y + radius)), int(1.3*radius), (0,180,0), -1)

cv2.imshow('Pupil Detector', img)

c = cv2.waitKey()
cv2.destroyAllWindows()


# TODO extract pupils using opencv
# https://subscription.packtpub.com/book/application-development/9781785283932/4/ch04lvl1sec44/detecting-pupils
# https://tech.paayi.com/pupil-detection-in-pyhton
# https://stackoverflow.com/questions/31658729/detecting-exact-pupil-diameter-in-python-and-opencv
