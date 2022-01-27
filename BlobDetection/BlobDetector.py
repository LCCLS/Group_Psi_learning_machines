from typing import Tuple, List

import cv2
import numpy as np
from matplotlib import pyplot as plt

from flags import FLAGS

LOWER_GREEN = np.array([0, 150, 0], dtype = "uint8")
UPPER_GREEN = np.array([150, 255, 150], dtype = "uint8")

class BlobDetector:
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = True
    detector = cv2.SimpleBlobDetector_create(params)

    @staticmethod
    def detect_blobs(image) -> List[bool]:
        """Splits image into 5 vertical segments and return boolean for each segment
        in which a blob is detected"""
        # Append white column to left and right for equal split
        image = append_white_column_left_and_right(image)
        #image = append_white_column_left_and_right(image)
        splitted_image = np.hsplit(image, 5)
        detected = []
        for image_part in splitted_image:
            #image_part = append_white_column_left_and_right(image_part)
            #image_part = append_white_row_top_and_bottom(image_part)
            mask = cv2.inRange(image_part, LOWER_GREEN, UPPER_GREEN)
            has_green = np.any(mask)
            detected.append(has_green)
            keypoints = BlobDetector.detector.detect(image_part)
            # detected.append(len(keypoints) > 0)
            if FLAGS.pictures:
                im_with_keypoints = cv2.drawKeypoints(image_part, keypoints, np.array([]), (0, 0, 255),
                                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                plt.imshow(im_with_keypoints)
                plt.show()
        return detected


def append_white_column_left_and_right(image):
    image = np.insert(image, 0, 255, axis=1)
    image = np.insert(image, image.shape[1], 255, axis=1)
    return image

def append_white_row_top_and_bottom(image):
    image = np.insert(image, 0, 255, axis=0)
    image = np.insert(image, image.shape[0], 255, axis=0)
    return image
