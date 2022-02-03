from typing import Tuple, List

import cv2
import numpy as np
from matplotlib import pyplot as plt

from util import Task
from flags import FLAGS

LOWER_RED_HSV = np.array([0, 50, 50], dtype = "uint8")
UPPER_RED_HSV = np.array([15, 255, 255], dtype = "uint8")

LOWER_GREEN_HSV = np.array([36, 50, 50], dtype = "uint8")
UPPER_GREEN_HSV = np.array([86, 255, 255], dtype = "uint8")

class ObjectDetector:
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = True
    detector = cv2.SimpleBlobDetector_create(params)

    @staticmethod
    def detect_objects(image, task: Task) -> List[bool]:
        """Splits image into 5 vertical segments and return boolean for each segment
        in which a blob is detected"""
        # Append white column to left and right for equal split
        image = append_white_column_left_and_right(image)
        image = append_white_column_left_and_right(image)
        #cv2.imwrite("red_food.png", image)
        #image = image[:,:,::-1]
        plt.imshow(image)
        plt.show()
        #image = append_white_column_left_and_right(image)
        splitted_image = np.hsplit(image, 3)
        detected = []
        for image_part in splitted_image:
            #image_part = append_white_column_left_and_right(image_part)
            #image_part = append_white_row_top_and_bottom(image_part)
            hsv = cv2.cvtColor(image_part, cv2.COLOR_BGR2HSV)
            plt.imshow(image_part)
            plt.show()
            if task == Task.COLLECT_FOOD:
                mask = cv2.inRange(hsv, LOWER_RED_HSV, UPPER_RED_HSV)
            else:
                mask = cv2.inRange(hsv, LOWER_GREEN_HSV, UPPER_GREEN_HSV)
            count = np.count_nonzero(mask)
            has_color = np.count_nonzero(mask) > 50
            detected.append(has_color)
        return detected


def append_white_column_left_and_right(image):
    image = np.insert(image, 0, 255, axis=1)
    image = np.insert(image, image.shape[1], 255, axis=1)
    return image

def append_white_row_top_and_bottom(image):
    image = np.insert(image, 0, 255, axis=0)
    image = np.insert(image, image.shape[0], 255, axis=0)
    return image
