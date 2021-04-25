#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

# set the GPIO module to work with the pin numbers in the Raspberry Pi docs
#   ( https://www.raspberrypi.org/documentation/usage/gpio )
#   and NOT the BCM channel names associated with the internal GPIO controller
#   The reason for this choice is that the RPi.GPIO docs give no instruction
#   on how to do the latter
GPIO.setmode(GPIO.BOARD)

# set GPIO17 (pin 11) as an output
pin = 11
GPIO.setup(pin, GPIO.OUT)

# turn the pin on and off, 5 seconds in each state, over 1 minute
for i in range(6):

    print("on")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(5.0)

    print("off")
    GPIO.output(pin, GPIO.LOW)
    time.sleep(5.0)

GPIO.cleanup()




