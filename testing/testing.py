#!/bin/env python3

"""
Air puff stimulator for raspberry pi
"""

import csv
import random
import time

import RPi.GPIO as GPIO
import picamera


# delay between running script and first trial start
initial_delay = 100 # seconds
# delay between trains
train_delay = 0 # seconds
# air puff duration
air_time = 0.5 # seconds
# water drip duration
water_time = 0.01 # seconds
# time between end of air puff and beginning of water release
air_puff_to_water_release_time = 0.8 # seconds
# time between last puff of one train and first puff of other train
inter_puff_delay = 19.5 # seconds
# number of puffs per train
num_puffs_in_train = 20
# number of trains in a trial
num_trains_in_trial = 1
# probability of receiving water
water_prob = 50 # %

SAVE_DIR = "../data"

LICKPORT_PIN = 21 # TODO add to code, use interrupts to count the licks on the lickport sensor
WATER_SOLENOID_PIN = 8
AIRPUFF_SOLENOID_PIN = 10
FAKE_SOLENOID_PIN = 12
AIRPUFF_TTL_PULSE = 11
VIDEO_TTL_PULSE = 36



def nano_to_milli(nano):
    return(int(nano // 1e6))



class PiCameraRecordingContextManager:
    def __init__(self, filename):
        self._filename = filename

    def __enter__(self):
        self._camera = picamera.PiCamera()
        self._camera.start_recording(self._filename)
        return self._camera

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._camera.stop_recording()
        self._camera.close()
        return None



def setup():
    """Set up all the pins and set their initial values"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LICKPORT_PIN, GPIO.IN)
    GPIO.setup(WATER_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(AIRPUFF_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(FAKE_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(AIRPUFF_TTL_PULSE, GPIO.OUT)
    GPIO.setup(VIDEO_TTL_PULSE, GPIO.OUT)

    GPIO.output(WATER_SOLENOID_PIN, GPIO.HIGH)
    GPIO.output(AIRPUFF_SOLENOID_PIN, GPIO.HIGH)
    GPIO.output(FAKE_SOLENOID_PIN, GPIO.HIGH)
    GPIO.output(AIRPUFF_TTL_PULSE, GPIO.LOW)
    GPIO.output(VIDEO_TTL_PULSE, GPIO.LOW)


def main():
    """Run test"""
    count = 0

    filename = input("what do you want to save the experiment as?\n")

    time.sleep(initial_delay)

    with open(f"{SAVE_DIR}/{filename}.csv", "w") as csvfile:

        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        with PiCameraRecordingContextManager(f"{SAVE_DIR}/mouse_video_{filename}.h264") as camera:
            GPIO.output(VIDEO_TTL_PULSE, GPIO.HIGH) # send a short pulse
            GPIO.output(VIDEO_TTL_PULSE, GPIO.LOW)
            for train_counter in range(num_trains_in_trial):
                for puff_counter in range(num_puffs_in_train):

                    camera.wait_recording(0) # checks to see if still recording video

                    # randomly choose whether to use a real solenoid or a fake one
                    puff_string = "fake"
                    tmp_solenoid_pin = FAKE_SOLENOID_PIN
                    tmp_water_pin = FAKE_SOLENOID_PIN
                    if (random.random() * 100 > water_prob):
                        puff_string = "real"
                        tmp_water_pin = WATER_SOLENOID_PIN
                        tmp_solenoid_pin = AIRPUFF_SOLENOID_PIN

                    print(puff_string)

                    # air puff / fake air puff
                    GPIO.output(tmp_solenoid_pin, GPIO.LOW)
                    solenoid_on = nano_to_milli(time.monotonic_ns())
                    GPIO.output(AIRPUFF_TTL_PULSE, GPIO.HIGH)
                    time.sleep(air_time)
                    GPIO.output(tmp_solenoid_pin, GPIO.HIGH)
                    solenoid_off = nano_to_milli(time.monotonic_ns())
                    GPIO.output(AIRPUFF_TTL_PULSE, GPIO.LOW)

                    time.sleep(air_puff_to_water_release_time)

                    # water release / fake water release
                    GPIO.output(tmp_water_pin, GPIO.LOW)
                    water_on = nano_to_milli(time.monotonic_ns())
                    time.sleep(water_time)
                    GPIO.output(tmp_water_pin, GPIO.HIGH)
                    water_off = nano_to_milli(time.monotonic_ns())

                    time.sleep(train_delay)

                    csvwriter.writerow([puff_string, count, solenoid_on, solenoid_off, water_on, water_off])

                    count += 1



if "__main__" == __name__:
    setup()
    main()
    GPIO.cleanup()

