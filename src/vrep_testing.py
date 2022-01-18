#!/usr/bin/env python2
from __future__ import print_function
import numpy as np
import robobo
import sys
import signal
from helper_functions import input_processing

def terminate_program(signal_number, frame):
    print("Ctrl-C received, terminating program")
    sys.exit(1)


def main():
    signal.signal(signal.SIGINT, terminate_program)
    rob = robobo.SimulationRobobo().connect(address='127.0.0.1', port=19997)

    rob.play_simulation()

    starting_pos = [-3.4506836128234863, 0.9749576449394226, 0.03710094094276428]
    stop = False

    while not stop:

        if rob.position() == starting_pos:
            stop = True

        sensor_values = input_processing(np.array(rob.read_irs()))
        front_sensors = sensor_values[3:]

        rob.move(20, 20, 1000)
        print(front_sensors)
        """if any(front_sensors):
            for i in range(10):
                rob.move(5, -5, 100)

        else:
            for i in range(10):
                rob.move(20, 20, 1000)"""

    rob.pause_simulation()
    rob.stop_world()


if __name__ == "__main__":
    main()
