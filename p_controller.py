#!/usr/bin/python3

from v_reader import VReader
from v_to_t import VtoT

def C_to_F(temp_c):

    return temp_c * 9.0/5.0 + 32.0

class PController:

    def __init__(self):

        self.vreader = VReader()

        self.v_to_t = VtoT()



    def read_T(self):

        v = self.vreader.get()
        return self.v_to_t.get(v)
    
    def update(self, target):

        T = self.read_T()
        print(str(T)+" C ("+str(C_to_F(T))+" F)")
