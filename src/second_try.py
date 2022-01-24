from __future__ import print_function

import time
import numpy as np
import threading
import robobo
import cv2
import sys
import signal
import prey

forward_bool = False
left_bool = False
right_bool = False
backwards_bool = False


def move_forward(rob):
    global forward_bool
    while True:
        if forward_bool:
            rob.move(20, 20, 50)


def turn_left(rob):
    global left_bool
    while True:
        if left_bool:
            rob.move(0, 5, 1)


def turn_right(rob):
    global right_bool
    while True:
        if right_bool:
            rob.move(20, 0, 50)


def move_backwards(rob):
    global backwards_bool
    while True:
        if backwards_bool:
            rob.move(-5, -5, 1)


def terminate_program(signal_number, frame):
    print("Ctrl-C received, terminating program")
    sys.exit(1)


def main():
    signal.signal(signal.SIGINT, terminate_program)
    global forward_bool
    global right_bool
    global left_bool
    global backwards_bool
    # rob = robobo.HardwareRobobo(camera=True).connect(address="192.168.1.7")
    rob = robobo.SimulationRobobo().connect(address='127.0.0.1', port=19997)

    rob.play_simulation()

    forward = threading.Thread(target=move_forward, args=(rob,))
    left = threading.Thread(target=turn_right, args=(rob,))
    right = threading.Thread(target=turn_right, args=(rob,))
    backwards = threading.Thread(target=move_backwards, args=(rob,))
    forward.start()
    left.start()
    right.start()
    backwards.start()
    # Following code moves the robot
    for i in range(100):
        data = rob.read_irs()
        print(data)
        if data[6] != False or data[5] != False or data[4] != False or data[3] != False:
            right_bool = True
            forward_bool = False
            backwards_bool = False
            left_bool = False
        else:
            forward_bool = True
            right_bool = False
            backwards_bool = False
            left_bool = False

        time.sleep(1)

    print("robobo is at {}".format(rob.position()))
    rob.sleep(1)

    # Following code moves the phone stand
    # rob.set_phone_pan(343, 100)
    # rob.set_phone_tilt(109, 100)
    # time.sleep(1)
    # rob.set_phone_pan(11, 100)
    # rob.set_phone_tilt(26, 100)

    # Following code makes the robot talk and be emotional
    # rob.set_emotion('happy')
    # rob.talk('Hi, my name is Robobo')
    # rob.sleep(1)
    # rob.set_emotion('sad')

    # Following code gets an image from the camera
    # image = rob.get_image_front()
    # IMPORTANT! `image` returned by the simulator is BGR, not RGB
    # cv2.imwrite("test_pictures.png",image)

    # time.sleep(0.1)

    # IR reading
    # for i in range(1000000):
    # print("ROB Irs: {}".format(np.log(np.array(rob.read_irs()))/10))
    # time.sleep(0.1)

    # pause the simulation and read the collected food
    rob.pause_simulation()

    # Stopping the simualtion resets the environment
    rob.stop_world()


if __name__ == "__main__":
    main()