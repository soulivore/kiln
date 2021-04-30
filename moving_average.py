#!/usr/bin/python3

import numpy as np

class MovingAverage:

    def __init__(self, N):

        # init array of nans
        self.recent = np.zeros(N)*np.nan

    # shift every element in the array to the next 
    #   element space in ascending numerical order
    #   (i.e. 1->2, 2->3, etc)
    # set element 0 to the new value 
    #   (element N-1) is dropped in the process)
    # return the average of the array contents
    def append(self, val):

        self.recent = np.roll(self.recent, 1)

        self.recent[0] = val

        return np.nanmean(self.recent)



if __name__ == "__main__":

    ma = MovingAverage(5)

    for i in range(10):

        print( ma.append(i) )
