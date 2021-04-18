#!/usr/bin/python3

import csv
import numpy as np
from scipy.interpolate import interp1d



# AD8495 breakout board specs
C = 0.005 # V/deg C
Vref = 1.25 # V
Vmax = 5.2 - 0.1 # V # raspberry pi 5V pin output - 0.1 V diode drop in AD8495 breakout board



class VtoT:

    def __init__(self):

        T = []
        V = []

        with open('AD8495_linearization.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:

                T.append(float(row[0]))
                V.append(float(row[2]))

        T = np.array(T)
        V = np.array(V) + Vref

        self.tf = interp1d(V, T)

    # returns temperature as a function of voltage going into the MCP3008 (from the AD8495 board)
    # function is based on NIST calibrations of AD8495 chips
    def get(self, v):

        return self.tf(v)




if __name__ == "__main__":

    v_to_t = VtoT()
    
    v = 4.9

    print("At V = "+str(v))
    print("T_ideal  = "+str((v-Vref)/C))
    print("T_actual = "+str(v_to_t.get(v)))
