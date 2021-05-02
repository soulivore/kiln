#!/usr/bin/python3

from v_reader import VReader
from v_to_t import VtoT
from moving_average import MovingAverage
import RPi.GPIO as GPIO

def C_to_F(temp_c):

    return temp_c * 9.0/5.0 + 32.0

class PController:

    def __init__(self, relay):

        # store instance of relay class that was initialized in Kiln
        self.relay = relay

        # initialize voltage reader
        self.vreader = VReader()

        # initialize voltage-to-temp converter
        self.v_to_t = VtoT()

        # initialize moving average with an appropriate number of samples
        self.ma = MovingAverage(20)



    def read_T(self):

        v = self.vreader.get()
        return self.v_to_t.get(v)
    
    # update the relay state 
    #   based on the given target temperature
    #   and the read temperature
    # arguments are:
    #   target temp
    def update(self, target):

        # determine the temperature in the kiln right now
        T = self.read_T()
        T_avg = self.ma.append(T)

        print(str(T_avg)+" C ("+str(C_to_F(T_avg))+" F)")
