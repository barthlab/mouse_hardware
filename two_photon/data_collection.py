#!/bin/env python3

"""
Air puff stimulator for raspberry pi
"""


import csv
import random
import time

import RPi.GPIO as GPIO
import picamera

# TODO make constants.py file for everything?
CAMERA_RESOLUTION = (1024, 768)


# Delay between running script and first trial start
initial_delay = 100 # seconds
# Delay between end of final trial and program termination
final_delay = 100 # seconds
# Air puff duration
air_time = 0.5 # seconds
# Water drip duration
water_time = 0.01 # seconds
# Time between end of air puff and beginning of water release
air_puff_to_water_release_time = 0.8 # seconds
# Time between last puff of one train and first puff of other train
inter_puff_delay = 19.5 # seconds
# Number of puffs per train
num_puffs_in_train = 20
# Number of trains in a trial
num_trains_in_trial = 1
# Probability of receiving water
water_prob = 50 # %

SAVE_DIR = "../data"

LICKPORT_PIN = 21 # TODO add to code, use interrupts to count the licks on the lickport sensor
WATER_SOLENOID_PIN = 8
AIRPUFF_SOLENOID_PIN = 10
FAKE_SOLENOID_PIN = 12
ENCODER_A_PIN = 24
ENCODER_B_PIN = 22 # To be able to tell direction
AIRPUFF_TTL_PULSE = 11
VIDEO_TTL_PULSE = 36



def nano_to_milli(nano):
    return(int(nano // 1e6))


# TODO remove this from here and put into post_processing.py
def extract_speeds_from_distance_marker_times(times):
    wheel_perimeter = 46.5 / 100 # Meters
    encoder_divisions = 1250 # Divisions
    num_datapoints = len(times)
    time_diffs = [times[1 + i] - times[i] for i in range(num_datapoints - 1)]
    speeds = [wheel_perimeter / encoder_divisions / time_diffs[i] for i in range(num_datapoints - 1)]
    return speeds


class PiCameraRecordingContextManager:
    def __init__(self, filename):
        self._filename = filename

    def __enter__(self):
        self._camera = picamera.PiCamera()
        self._camera.resolution = CAMERA_RESOLUTION
        self._camera.start_recording(self._filename)
        return self._camera

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._camera.stop_recording()
        self._camera.close()
        return None



def encoder_step_A(pin):
    global distance_marker_times
    distance_marker_times.append(time.monotonic_ns() / 1e9) # Seconds



def lick(pin):
    global lick_times
    lick_times.append(time.monotonic_ns() / 1e9) # Seconds



def setup():
    """Set up all the pins and set their initial values"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LICKPORT_PIN, GPIO.IN)
    GPIO.setup(WATER_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(AIRPUFF_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(ENCODER_A_PIN, GPIO.IN)
    GPIO.setup(ENCODER_B_PIN, GPIO.IN)
    GPIO.setup(FAKE_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(AIRPUFF_TTL_PULSE, GPIO.OUT)
    GPIO.setup(VIDEO_TTL_PULSE, GPIO.OUT)

    GPIO.output(WATER_SOLENOID_PIN, GPIO.HIGH)
    GPIO.output(AIRPUFF_SOLENOID_PIN, GPIO.HIGH)
    GPIO.output(FAKE_SOLENOID_PIN, GPIO.HIGH)
    GPIO.output(AIRPUFF_TTL_PULSE, GPIO.LOW)
    GPIO.output(VIDEO_TTL_PULSE, GPIO.LOW)

    GPIO.add_event_detect(ENCODER_A_PIN, GPIO.RISING, callback=encoder_step_A)
    GPIO.add_event_detect(LICKPORT_PIN, GPIO.RISING, callback=lick)



def main():
    """Run test"""

    global distance_marker_times
    global lick_times

    count = 0

    filename = input("what do you want to save the experiment as?\n")

    with open(f"{SAVE_DIR}/puff_data_{filename}.csv", "w") as puff_data_file:
        with open(f"{SAVE_DIR}/run_data_{filename}.csv", "w") as run_data_file:
            with open(f"{SAVE_DIR}/lick_data_{filename}.csv", "w") as lick_data_file:

                puff_writer = csv.writer(puff_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                run_writer = csv.writer(run_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                lick_writer = csv.writer(lick_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                with PiCameraRecordingContextManager(f"{SAVE_DIR}/mouse_video_{filename}.h264") as camera:
                    # Send a short pulse
                    GPIO.output(VIDEO_TTL_PULSE, GPIO.HIGH)
                    GPIO.output(VIDEO_TTL_PULSE, GPIO.LOW)

                    time.sleep(initial_delay)

                    for train_counter in range(num_trains_in_trial):
                        for puff_counter in range(num_puffs_in_train):

                            # Check to see if still recording video
                            camera.wait_recording(0)

                            # Randomly choose whether to use a real solenoid or a fake one
                            puff_string = "fake"
                            tmp_solenoid_pin = FAKE_SOLENOID_PIN
                            tmp_water_pin = FAKE_SOLENOID_PIN
                            if (random.random() * 100 > water_prob):
                                puff_string = "real"
                                tmp_water_pin = WATER_SOLENOID_PIN
                                tmp_solenoid_pin = AIRPUFF_SOLENOID_PIN

                            print(puff_string)

                            # Air puff / fake air puff
                            GPIO.output(tmp_solenoid_pin, GPIO.LOW)
                            solenoid_on = nano_to_milli(time.monotonic_ns())
                            GPIO.output(AIRPUFF_TTL_PULSE, GPIO.HIGH)
                            time.sleep(air_time)
                            GPIO.output(tmp_solenoid_pin, GPIO.HIGH)
                            solenoid_off = nano_to_milli(time.monotonic_ns())
                            GPIO.output(AIRPUFF_TTL_PULSE, GPIO.LOW)

                            time.sleep(air_puff_to_water_release_time)

                            # Water release / fake water release
                            GPIO.output(tmp_water_pin, GPIO.LOW)
                            water_on = nano_to_milli(time.monotonic_ns())
                            time.sleep(water_time)
                            GPIO.output(tmp_water_pin, GPIO.HIGH)
                            water_off = nano_to_milli(time.monotonic_ns())

                            time.sleep(inter_puff_delay)

                            # Convert distance_marker_times to speeds
                            prev_distance_marker_times, distance_marker_times = distance_marker_times, []
                            speeds = extract_speeds_from_distance_marker_times(prev_distance_marker_times)

                            # Save current lick_times
                            prev_lick_times, lick_times = lick_times, []

                            # Save data
                            for data in list(zip(prev_distance_marker_times, speeds)):
                                run_writer.writerow(data)
                            puff_writer.writerow([puff_string, count, solenoid_on, solenoid_off, water_on, water_off])
                            for data in prev_lick_times:
                                lick_writer.writerow([data])

                            count += 1

                    time.sleep(final_delay)

                    prev_distance_marker_times, distance_marker_times = distance_marker_times, []
                    speeds = extract_speeds_from_distance_marker_times(prev_distance_marker_times)

                    for data in list(zip(prev_distance_marker_times, speeds)):
                        run_writer.writerow(data)



if "__main__" == __name__:
    distance_marker_times = [] # Time that the marker was hit
    lick_times = [] # Time that the mouse licked
    setup()
    main()
    GPIO.cleanup()

