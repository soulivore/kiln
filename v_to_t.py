#!/usr/bin/python3

import csv
import time
import numpy as np
from scipy.interpolate import interp1d
from v_reader import VReader
from conversions import C_to_F

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

        # If our reported voltage is outside the interpolation range,
        #   it would probably be best in general to use a different v->t conversion.
        # However, if this happens, we know something went horrible wrong,
        #   so we'll just throw an error
        if v < self.tf.x[0] or self.tf.x[-1] < v:
            raise RuntimeError ("Voltage "+str(v)+" outside interpolation range of ("+str(self.tf.x[0])+", "+str(self.tf.x[-1])+"). Aborting.")

        return self.tf(v)




if __name__ == "__main__":

    vreader = VReader()
    v_to_t = VtoT()

    print(v_to_t.tf.x)
    print(v_to_t.tf.y)

    while True :

        v = vreader.get()
        print("V = "+str(v)+" V")

        t_ideal = (v-Vref)/C
        t_actual = v_to_t.get(v)

        print("T_ideal   = "+str(t_ideal) +" C    ("+str(C_to_F(t_ideal ))+" F)")
        print( "T_actual = "+str(t_actual)+" C    ("+str(C_to_F(t_actual))+" F)")
        print("")

        time.sleep(1.0)
