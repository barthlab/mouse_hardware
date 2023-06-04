#!/bin/env python3

"""
Encoder test script for raspberry pi
"""

import RPi.GPIO as GPIO



ENCODER_A_PIN = 24
ENCODER_B_PIN = 22



def A(pin):
    print("A")



def B(pin):
    print("B")



def setup():
    """Set up all the pins and set their initial values"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LICKPORT_PIN, GPIO.IN)

    GPIO.add_event_detect(ENCODER_A_PIN, GPIO.RISING, callback=A)
    GPIO.add_event_detect(ENCODER_B_PIN, GPIO.RISING, callback=B)



def main():
    while True:
        pass



if "__main__" == __name__:
    setup()
    main()
    GPIO.cleanup()

