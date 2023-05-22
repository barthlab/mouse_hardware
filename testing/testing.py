#!/bin/env python3

"""
Air puff stimulator for raspberry pi
"""

import csv
import random
import time

import GPIO
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

# TODO change these numbers
LICKPORT_PIN = -1
WATER_SOLENOID_PIN = -1
AIRPUFF_SOLENOID_PIN = -2
FAKE_SOLENOID_PIN = -3
AIRPUFF_TTL_PULSE = -7
VIDEO_TTL_PULSE = -8



def nano_to_milli(nano):
    return(int(nano // 1e6))



class PiCameraRecordingContextManager:
    def __enter__(self, filename):
        self._camera = picamera.PiCamera()
        self._camera.start_recording(filename)
        return self._camera

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._camera.stop_recording(filename)
        self._camera.close()
        return None



def sleep_and_do(time_to_sleep, func):
    # takes in an amount of time to sleep in seconds and a function
    # does the function until the amount of time specified has concluded
    # NOTE: if the function takes a really long time to do, it will affect the timing
    start_time = time.time()
    while (start_time + time_to_sleep * 1000 < time.time()):
        func()



def setup():
    """Set up all the pins and set their initial values"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LICKPORT_PIN, GPIO.IN)
    GPIO.setup(WATER_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(AIRPUFF_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(FAKE_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(AIRPUFF_TTL_PULSE, GPIO.OUT)
    GPIO.setup(VIDEO_TTL_PULSE, GPIO.OUT)

    GPIO.output(WATER_SOLENOID_PIN, GPIO.LOW)
    GPIO.output(AIRPUFF_SOLENOID_PIN, GPIO.LOW)
    GPIO.output(AIRPUFF_TTL_PULSE, GPIO.LOW)
    GPIO.output(VIDEO_TTL_PULSE, GPIO.LOW)



def main():
    """Run test"""
    time.sleep(initial_delay)

    count = 0

    filename = int(time.time()) # TODO save as day?

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

                    # air puff / fake air puff
                    GPIO.output(tmp_solenoid_pin, GPIO.HIGH)
                    solenoid_on = nano_to_milli(time.monotonic_ns())
                    GPIO.output(AIRPUFF_TTL_PULSE, GPIO.HIGH)
                    sleep_and_do(air_time, lambda x: csvwriter.writerow([puff_string, count, solenoid_on, solenoid_off, water_on, water_off, GPIO.input(LICKPORT_PIN)]))
                    GPIO.output(tmp_solenoid_pin, GPIO.LOW)
                    solenoid_off = nano_to_milli(time.monotonic_ns())
                    GPIO.output(AIRPUFF_TTL_PULSE, GPIO.LOW)

                    sleep_and_do(air_puff_to_water_release_time, lambda x: csvwriter.writerow([puff_string, count, solenoid_on, solenoid_off, water_on, water_off, GPIO.input(LICKPORT_PIN)]))

                    # water release / fake water release
                    GPIO.output(tmp_water_pin, GPIO.HIGH)
                    water_on = nano_to_milli(time.monotonic_ns())
                    GPIO.output(WATER_TTL_PULSE, GPIO.HIGH)
                    sleep_and_do(water_time, lambda x: csvwriter.writerow([puff_string, count, solenoid_on, solenoid_off, water_on, water_off, GPIO.input(LICKPORT_PIN)]))
                    GPIO.output(tmp_water_pin, GPIO.LOW)
                    water_off = nano_to_milli(time.monotonic_ns())
                    GPIO.output(WATER_TTL_PULSE, GPIO.LOW)

                    csvwriter.writerow([puff_string, count, solenoid_on, solenoid_off, water_on, water_off, GPIO.input(LICKPORT_PIN)])

                    count += 1

                time.sleep(train_delay)



if "__main__" == __name__:
    setup()
    main()
    GPIO.cleanup()

