#!/usr/bin/env python2
from __future__ import print_function

import time
import numpy as np

import robobo
import cv2
import sys
import signal


def terminate_program(signal_number, frame):
    print("Ctrl-C received, terminating program")
    sys.exit(1)

def main():
    signal.signal(signal.SIGINT, terminate_program)
    rob = robobo.SimulationRobobo().connect(address='127.0.0.1', port=19997)
    rob.play_simulation()

    rob.set_phone_tilt(0.4, 100)
    rob.move(-14, 141233, 2000)





    rob.pause_simulation()
    rob.stop_world()


if __name__ == "__main__":
    main()
