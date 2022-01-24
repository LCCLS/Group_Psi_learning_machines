#!/usrrob=None python2
from __future__ import print_function

import time
import numpy as np
import threading
import robobo
import cv2
import sys
import signal
import prey
import queue

my_queue = "doing"

def get_action(rob):
    global my_queue
    data = rob.read_irs()
    if data[6] != False or data[5] != False or data[4] != False or data[3] != False:
        my_queue = "right"
    else:
        my_queue = "forward"

def terminate_program(signal_number, frame):
    print("Ctrl-C received, terminating program")
    sys.exit(1)

def main():
    signal.signal(signal.SIGINT, terminate_program)
    global my_queue
    # rob = robobo.HardwareRobobo(camera=True).connect(address="192.168.1.7")
    rob = robobo.SimulationRobobo().connect(address='127.0.0.1', port=19997)

    rob.play_simulation()

    # Following code moves the robot

    for i in range(1000):
        get_action_thread = threading.Thread(target=get_action, args=(rob,))
        if my_queue == "forward":
            get_action_thread.start()
            rob.move(5,5,20)
        else:
            get_action_thread.start()
            rob.move(5,0,20)
        print(threading.active_count())


    print("robobo is at {}".format(rob.position()))
    rob.sleep(1)


    # Following code moves the phone stand
    #rob.set_phone_pan(343, 100)
    #rob.set_phone_tilt(109, 100)
    #time.sleep(1)
    #rob.set_phone_pan(11, 100)
    #rob.set_phone_tilt(26, 100)

    # Following code makes the robot talk and be emotional
    #rob.set_emotion('happy')
    #rob.talk('Hi, my name is Robobo')
    #rob.sleep(1)
    #rob.set_emotion('sad')

    # Following code gets an image from the camera
    #image = rob.get_image_front()
    # IMPORTANT! `image` returned by the simulator is BGR, not RGB
    #cv2.imwrite("test_pictures.png",image)

    #time.sleep(0.1)

    # IR reading
    #for i in range(1000000):
        #print("ROB Irs: {}".format(np.log(np.array(rob.read_irs()))/10))
        #time.sleep(0.1)

    # pause the simulation and read the collected food
    rob.pause_simulation()
    
    # Stopping the simualtion resets the environment
    rob.stop_world()


if __name__ == "__main__":
    main()
