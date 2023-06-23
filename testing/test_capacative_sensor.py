#!/bin/env python3

"""
Lickport test script for raspberry pi
"""

import RPi.GPIO as GPIO



LICKPORT_PIN = 21



def rising(pin):
    print("touch detected")



def setup():
    """Set up all the pins and set their initial values"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LICKPORT_PIN, GPIO.IN)

    GPIO.add_event_detect(LICKPORT_PIN, GPIO.RISING, callback=rising)



def main():
    while True:
        pass



if "__main__" == __name__:
    setup()
    main()
    GPIO.cleanup()

