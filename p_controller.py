#!/usr/bin/python3

import sys
import time
from relay import Relay
from v_reader import VReader
from v_to_t import VtoT
from moving_average import MovingAverage
from t_profile import TProfile
from logger import Logger
import RPi.GPIO as GPIO
from colorama import Fore, Back, Style

# the P controller turns the coils on and off with hysteresis
#   so that we don't constantly switch them and break the coils or relay
# the coils will be switched on  if the current temp is below the target by...
# the coils will be switched off if the current temp is above the target by...
T_tolerance = 10 # degrees C
# i.e. this is half of the width of the hysteresis loop

# strip a string segment from the end of a string and return the result
def chop_off_end(instr, suffix):

    i = instr.rfind(suffix)
    if i != -1 :
        return instr[:i]
    else :
        return instr

def C_to_F(temp_c):
    return temp_c * 9.0/5.0 + 32.0

# It's a PID controller, except there's no I or D
# Looks at current temp and target temp and decides whether
#   the coils should be on or off
class PController:

    # initializes with the filename of the temperature profile csv
    def __init__(self, filename):

        # initialize relay controller
        self.relay = Relay()

        # initialize voltage reader
        self.vreader = VReader()

        # initialize voltage-to-temp converter
        self.v_to_t = VtoT()

        # initialize moving average with an appropriate number of samples
        self.ma = MovingAverage(20)

        # initialize the target temperature vs time
        self.t_profile = TProfile(filename)

        # initialize data logger
        self.logger = Logger(chop_off_end(filename, ".csv"))

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
        T_avg = -self.ma.append(T)

        # determine what the temperature in the kiln should be right now
        T_target = self.t_profile.get_target()

        # determine if the coil state needs to be switched
        # if it switches, log it
        switched = False
        if not self.relay.is_on() and T_avg < T_target - T_tolerance:
            self.relay.turn_on()
            switched = True

        elif self.relay.is_on() and T_avg > T_target + T_tolerance:
            self.relay.turn_off()
            switched = True

        # log the data 
        self.logger.log(time.time(), T_avg, self.relay.is_on(), switched)

        # output to the console
        print("target temp = "+str(int(T_target))+" C     ("+str(int(C_to_F(T_target)))+" F)          ")
        print("actual temp = "+str(int(T_avg))+" C     ("+str(int(C_to_F(T_avg)))+" F)          ")
        if self.relay.is_on(): 
            print("relay: "+Back.GREEN+Fore.BLACK+"ON"+Style.RESET_ALL)
        else :
            print("relay: "+Back.RED+Fore.BLACK+"OFF"+Style.RESET_ALL)
        print("\033[A\033[A\033[A\033[A\r") # reset print location to beginning of the above text block




if __name__ == "__main__":

    print(chop_off_end("test.csv",".csv"))
    print(chop_off_end("test",".csv"))

