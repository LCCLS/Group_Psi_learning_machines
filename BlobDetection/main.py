from flags import FLAGS
import cv2
import numpy as np
from Robot import Robot


def main():
    # Print chosen options
    robobo = Robot(simulated=True)
    robobo.train()


if __name__ == "__main__":
    main()
