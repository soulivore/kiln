#!/usr/bin/python3

import csv
import time
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# the temperature vs time that you program the kiln with shall be 
#   written as (time, temp) coords
# they will be imported from a csv of the form
#   time, temp
#   time, temp
#   ...
# the times shall be given in hours (fractional hours are allowed)
# the temps shall be given in celcius
# the first coordinate shall be time = 0
#   (the first temp does not have to be zero)
# the time of the last coordinate is the shutoff time of the kiln
# there shall be at least 2 coordinates
# the csv shall have no header nor breaks between lines
#   a line that does not contain a time and temp will be treated as end of file

class TProfile:

    # argument is filename of the csv, including the ".csv" extension
    def __init__(self, filename):

        times = []
        temps = []

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:

                # if it's probaby a coordinate
                if len(row) == 2 :
                    times.append(float(row[0]))
                    temps.append(float(row[1]))

                # otherwise, assume it's the end of the file
                else :
                    break

        if len(times) < 2 :
            raise RuntimeError ("Not enough (time,temp) coordinates given. Aborting.")

        if len(times) != len(temps) :
            raise RuntimeError ("Lengths of times and temps did not match. Aborting.")

        if abs(times[0]) > 0.1 :
            raise RuntimeError ("First time in T profile was not 0. Aborting.")

        times = np.array(times)
        temps = np.array(temps)

        # output to terminal
        for i in range(len(times)):
            print(str(times[i])+" hours:    "+str(temps[i])+" C")

        self.tf = interp1d(times, temps)

        self.start_time = time.time()

    # return target temperature vs time (in hours) from the start time
    def get_temp_vs_time(self, dt_h):

        return self.tf(dt_h)

    # figure out what time it is and return the target temperature
    def get_target(self):
    
        current_time = time.time()

        # time difference in seconds
        dt = current_time - self.start_time # s

        # time difference in floating-point hours
        dt_h = float(dt)/60.0/60.0 # h

        # for now, if the current time exceeds the last time coordinate in the csv,
        #   just hold at the temperature of the last coordinate
        if 0 < dt_h and dt_h < self.tf.x[-1]:
            return self.get_temp_vs_time(dt_h)
        elif self.tf.x[-1] < dt_h:
            return self.tf.y[-1]
        else :
            raise RuntimeError ("Time delta "+str(dt_h)+" cannot be negative. Aborting.")



if __name__ == "__main__":

    t_profile = TProfile("profile_test.csv")

    while False :

        print(t_profile.get_target())

        time.sleep(1.0)
        
    print(t_profile.tf.x[-1])

    N = 1000
    times_interp = np.linspace(t_profile.tf.x[0], t_profile.tf.x[-1], N)
    temps_interp = [t_profile.get_temp_vs_time(dt_h) for dt_h in times_interp]

    plt.plot(times_interp, temps_interp)
    plt.xlabel("time (h)")
    plt.ylabel("temp ($^O$C)")
    plt.show()
