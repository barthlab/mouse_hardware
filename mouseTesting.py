#!/bin/env python3

"""
Air puff stimulator for raspberry pi
"""
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
# delay in-between puff and water
puff_water_delay = 0.5 # seconds
# time for water duration
water_duration = 0.075 # seconds
# z, time between end of puff and beginning of next puff within a train
puff_puff_delay = 19.5 # seconds
# x, number of  puffs in a train
num_puffs_in_train = 20
# n, number of trains in a trial
num_trains_in_trial = 1
# probability of receiving water
water_prob = 50 # %


# TODO change these numbers
SOLENOID_PIN = 2
TTL_PULSE_PIN = 7
FAKE_SOLENOID_PIN = 3
WATER_PIN = 4 # TODO rename
BUILTIN_LED_PIN = 1

def setup():
    """Set up all the pins and set their initial values"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(FAKE_SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(TTL_PULSE_PIN, GPIO.OUT)
    GPIO.setup(WATER_PIN, GPIO.OUT)
    GPIO.setup(BUILTIN_LED_PIN, GPIO.OUT)

    GPIO.output(SOLENOID_PIN, GPIO.LOW)
    GPIO.output(TTL_PULSE_PIN, GPIO.LOW)
    GPIO.output(WATER_PIN , GPIO.LOW)
    GPIO.output(BUILTIN_LED_PIN, GPIO.LOW)

def main():
    """Run test"""
    time.sleep(initial_delay)

    for train_counter in range(num_trains_in_trial):
        for puff_counter in range(num_puffs_in_train):

            # randomly choose whether to use a real solenoid or a fake one
            tmp_solenoid_pin = FAKE_SOLENOID_PIN
            if (random.random() * 100 > water_prob):
                tmp_solenoid_pin = SOLENOID_PIN

            # air puff / fake air puff
            GPIO.output(tmp_solenoid_pin, GPIO.HIGH)
            ms_on = time.time()
            GPIO.output(TTL_PULSE_PIN, GPIO.HIGH)
            time.sleep(air_time)
            GPIO.output(tmp_solenoid_pin, GPIO.LOW)
            ms_off = time.time()
            GPIO.output(TTL_PULSE_PIN, GPIO.LOW)

            time.sleep(puff_water_delay)

            # TODO ??? what does water pin do?
            GPIO.output(WATER_PIN, GPIO.HIGH)
            w_on = time.time()
            time.sleep(water_duration)
            GPIO.output(WATER_PIN, GPIO.LOW)
            w_off = time.time()
            time.sleep(puff_puff_delay)
            puff_counter += 1
            print(f"Puff, {ct}, {ms_on}, {ms_off}, {w_on}, {w_off}") # TODO time formatting?

        time.sleep(train_delay)

    # TODO if can't get ip address from CMU, then make it flash the lights



if "__main__" == __name__:
    setup()
    main()
    GPIO.cleanup()

