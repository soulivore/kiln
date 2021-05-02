#!/usr/bin/python3

import RPi.GPIO as GPIO

class Relay:

    def __init__(self):

        # initialize relay GPIO

        # set the GPIO module to work with the BCM GPIO controller's channel names
        # we have to do this because another module in this code is also doing it
        GPIO.setmode(GPIO.BCM)

        # set GPIO17 (pin 11) as an output
        self.pin = 17
        GPIO.setup(self.pin, GPIO.OUT)

        # private member variable indicating relay state
        self.__is_on = False

        # make sure it's actually off
        self.turn_off()

    def is_on(self):

        return self.__is_on

    def turn_on(self):

        GPIO.output(self.pin, GPIO.HIGH)
        self.__is_on = True

    def turn_off(self): 

        GPIO.output(self.pin, GPIO.LOW)
        self.__is_on = False
