#!/usr/bin/python3

import os
from datetime import date
import csv

# how often to log data (in seconds)
log_interval = 60.0 # s

class Logger:

    # initializes with an optional string that goes into the filename
    #   that may provide additional information about the data being logged
    def __init__(self, description = ""):

        # create an output filename that isn't already taken
        i = 0
        while True :
            self.filename = "output/log_"+str(date.today())+"_"+str(description)+"_"+str(i)+".csv"
            if os.path.isfile(self.filename):
                i += 1
            else :
                break

        self.times = []
        self.temps = []
        self.relay_states = []

        self.last_time = None

    # decide if it's been long enough since the last log event to log another set of data
    # if so, log it
    # or, if force is True, log anyway
    def log(self, time, temp, relay_state, force = False):

        if force or self.last_time is None or (self.last_time is not None and time - self.last_time > log_interval):

            self.times.append(time)
            self.temps.append(temp)
            self.relay_states.append(relay_state)

            self.last_time = time

    def write(self):

        # open the file for writing
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)

            for i in range(len(self.times)):
                writer.writerow([self.times[i], self.temps[i], self.relay_states[i]])

        print("log file written")


if __name__ == "__main__":

    logger = Logger("test")

    logger.log(1.2,2.3,True)
    logger.log(1.2+1.0/30.0,2.4,True)
    logger.log(3.3,4.4,False)
    logger.log(5.4,6.5,True)

    logger.write()

