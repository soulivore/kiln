#!/usr/bin/python3

from v_reader import VReader
from v_to_t import VtoT


class PController:

    def __init__(self):

        self.vreader = VReader()

        self.v_to_t = VtoT()



    def read_T(self):

        v = self.vreader.get()
        return self.v_to_t.get(v)
    
    def update(self, target):

        print(self.read_T())
