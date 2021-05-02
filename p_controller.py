#!/usr/bin/python3

from v_reader import VReader
from v_to_t import VtoT
from moving_average import MovingAverage
from t_profile import TProfile
import RPi.GPIO as GPIO

# the P controller turns the coils on and off with hysteresis
#   so that we don't constantly switch them and break the coils or relay
# the coils will be switched on  if the current temp is below the target by...
# the coils will be switched off if the current temp is above the target by...
T_tolerance = 10 # degrees C
# i.e. this is half of the width of the hysteresis loop

def C_to_F(temp_c):

    return temp_c * 9.0/5.0 + 32.0

# It's a PID controller, except there's no I or D
# Looks at current temp and target temp and decides whether
#   the coils should be on or off
class PController:

    # initializes with 
    #   an instance of the relay controller class 
    #   the filename of the temperature profile csv
    def __init__(self, relay, filename):

        # store instance of relay class that was initialized in Kiln
        self.relay = relay

        # initialize voltage reader
        self.vreader = VReader()

        # initialize voltage-to-temp converter
        self.v_to_t = VtoT()

        # initialize moving average with an appropriate number of samples
        self.ma = MovingAverage(20)

        # initialize the target temperature vs time
        self.t_profile = TProfile(filename)

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
        print("actual temp = "+str(T_avg)+" C ("+str(C_to_F(T_avg))+" F)")

        # determine what the temperature in the kiln should be right now
        T_target = self.t_profile.get_target()
        #print("target temp = "+str(T_target)+" C");


