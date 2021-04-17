#!/usr/bin/python3

import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn



# output actual voltage as a function of read voltage
def get_v_actual(v_read):
    return 1.59025 * v_read - 0.00303



class VReader:

    def __init__(self):

        # create the spi bus
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        
        # create the cs (chip select)
        self.cs = digitalio.DigitalInOut(board.D22)
        
        # create the mcp object
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        
        # create an analog input channel on pin 0
        self.chan0 = AnalogIn(self.mcp, MCP.P0)

    def get(self):

        # get raw voltage reading
        v_read = self.chan0.voltage

        # convert it to actual voltage and return
        return get_v_actual(v_read)



if __name__ == "__main__":

    vreader = VReader()

    while True :

        print('ADC Voltage (rescaled): ' + str(vreader.get()) + 'V')
    
        time.sleep(1.0)




