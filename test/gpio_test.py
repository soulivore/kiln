#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

# set the GPIO module to work with 
#   the BCM channel names associated with the internal GPIO controller
#   and NOT the pin numbers in the Raspberry Pi docs
#   ( https://www.raspberrypi.org/documentation/usage/gpio )
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

# set GPIO17 (pin 11) as an output
#pin = 11
pin = 17
GPIO.setup(pin, GPIO.OUT)

# turn the pin on and off, 5 seconds in each state, over 1 minute
for i in range(1):

    print("on")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2.0)

    print("off")
    GPIO.output(pin, GPIO.LOW)
    time.sleep(2.0)

GPIO.cleanup()




