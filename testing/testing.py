#!/bin/env python3

"""
Air puff stimulator for raspberry pi
"""

import csv
import random
import time

import GPIO


# for trouble shooting or testing, use initialDelay = 1000, trialDelay = 500, airTime=10, offTime = 250
# a, initial delay between plugging in arduino and first trial start
initial_delay = 100 # seconds
# b, delay between trains
train_delay = 0 # seconds
# y, open solenoid duration
air_time = 0.5 # seconds
# z, time between end of puff and beginning of next puff within a train
inter_puff_delay = 19.5 # seconds
# x, number of  puffs in a train
num_puffs_in_train = 20
# n, number of trains in a trial
num_trains_in_trial = 1
# probability of receiving water
water_prob = 50 # %

dir = "../data"

# TODO change these numbers
SOLENOID_PIN = 2
TTL_PULSE_PIN = 7
FAKE_SOLENOID_PIN = 3
BUILTIN_LED_PIN = 1

def nano_to_milli(nano):
    return(int(nano // 1e6))

def setup():
    """Set up all the pins and set their initial values"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(FAKE_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(TTL_PULSE_PIN, GPIO.OUT)
    GPIO.setup(BUILTIN_LED_PIN, GPIO.OUT)

    GPIO.output(SOLENOID_PIN, GPIO.LOW)
    GPIO.output(TTL_PULSE_PIN, GPIO.LOW)
    GPIO.output(BUILTIN_LED_PIN, GPIO.LOW)

def main():
    """Run test"""
    time.sleep(initial_delay)

    count = 0

    with open(f"{dir}/{int(time.time())}.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for train_counter in range(num_trains_in_trial):
            for puff_counter in range(num_puffs_in_train):

                # randomly choose whether to use a real solenoid or a fake one
                tmp_solenoid_pin = FAKE_SOLENOID_PIN
                puff_string = "fake"
                if (random.random() * 100 > water_prob):
                    tmp_solenoid_pin = SOLENOID_PIN
                    puff_string = "real"

                # air puff / fake air puff
                GPIO.output(tmp_solenoid_pin, GPIO.HIGH)
                solenoid_on = nano_to_milli(time.monotonic_ns())
                GPIO.output(TTL_PULSE_PIN, GPIO.HIGH)
                time.sleep(air_time)
                GPIO.output(tmp_solenoid_pin, GPIO.LOW)
                solenoid_off = nano_to_milli(time.monotonic_ns())
                GPIO.output(TTL_PULSE_PIN, GPIO.LOW)
                count += 1

                csvwriter.writerow([puff_string, count, solenoid_on, solenoid_off])

            time.sleep(train_delay)



if "__main__" == __name__:
    setup()
    main()
    GPIO.cleanup()

