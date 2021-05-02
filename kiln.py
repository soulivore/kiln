#!/usr/bin/python3

import sys
import time
from signal import signal, SIGINT, SIGTERM
from p_controller import PController
from relay import Relay
import RPi.GPIO as GPIO

# this top-level class mostly just handles errors
class Kiln:

    # initializes with the filename of the temperature profile csv
    def __init__(self, filename):

        # initialize relay controller
        self.relay = Relay()
        
        # initialize P controller
        self.p_ctrl = PController(self.relay, filename)

    def run(self):

        # initialize shutdown signal receivers
        signal(SIGINT, self.shutdown)
        signal(SIGTERM, self.shutdown)

        try :

            self.is_running = True

            while self.is_running:

                # update p controller with target temperature
                self.p_ctrl.update(0.0)

                time.sleep(1.0)

            self.shutdown("finished")

        except :

            if sys.exc_info()[0] != SystemExit :

                print("exception caught:")
                sys.excepthook(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])

                self.shutdown("exception caught")

    def shutdown(self, signal_received = None, frame = None):

        if   signal_received == 2 :
            signal_received = "ctrl+C"
        elif signal_received == 15 :
            signal_received = "SIGTERM"

        print("shutdown signal received: "+str(signal_received))

        # turn off the relay
        self.relay.turn_off()

        print("relay off")

        # un-initialize GPIOs
        GPIO.cleanup()

        sys.exit(0)


if __name__ == "__main__":

    # parse the argument of the command line call:
    #   the filename of the temperature profile csv
    if len(sys.argv) == 2 and sys.argv[1] != "":

        kiln = Kiln(sys.argv[1])

        kiln.run()

    else :
        print("ERROR: you must execute the script with the form: ./kiln.py [temp_profile.csv]")
        print("     sys.argv = "+str(sys.argv))
        print("     Aborting.")
        sys.exit(0)
