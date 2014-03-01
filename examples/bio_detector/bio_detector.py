#!/usr/bin/env python
import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

# GLOBAL VARS


def detect(roi, detect_type, debug=False):
    colour_types = {
        "PROTEIN": {  # RED
            "lower_bound": np.array([0, 100, 0]),
            "upper_bound": np.array([10, 255, 150])
        },
        "GLUCOSE": {  # BLUE
            "lower_bound": np.array([75, 100, 100]),
            "upper_bound": np.array([130, 255, 255])
        }
    }
    hsv_img = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    thresh_img = cv2.inRange(
        hsv_img,
        colour_types[detect_type]["lower_bound"],
        colour_types[detect_type]["upper_bound"]
    )

    # identify contours
    detected = None
    contours, hierarchy = cv2.findContours(
        thresh_img,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    for i in range(len(contours)):
        if cv2.arcLength(contours[i], True) > 150:
            if detect_type == "PROTEIN":
                cv2.drawContours(roi, contours, i, (0, 255, 0), 3)
            elif detect_type == "GLUCOSE":
                cv2.drawContours(roi, contours, i, (0, 0, 255), 3)
            detected = contours[i]
            break

    # show detected regions
    if debug:
        cv2.imshow("Detected", roi)

    return detected


def segment_roi(img_path, debug=False):
    img = cv2.imread(img_path, 0)
    img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)

    # create threshold image
    img = cv2.inRange(img, 20, 255, cv2.cv.CV_THRESH_BINARY)
    if debug:
        cv2.imshow("Detection Paper Threshold", img)

    # find only the detection paper by finding the largest contour
    contours, hierarchy = cv2.findContours(
        img,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    largest = contours[0]
    largest_index = 0
    for i in range(len(contours)):
        if cv2.arcLength(contours[i], True) > cv2.arcLength(largest, True):
            largest = contours[i]
            largest_index = i
    x, y, w, h = cv2.boundingRect(largest)

    # draw detected area
    if debug:
        debug_img = cv2.imread(img_path)
        debug_img = cv2.resize(debug_img, (0, 0), fx=0.2, fy=0.2)
        cv2.drawContours(debug_img, contours, largest_index, (0, 255, 0), 3)
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow("Detection Paper", debug_img)

    # segemnt region of interst
    roi = cv2.imread(img_path)
    roi = cv2.resize(roi, (0, 0), fx=0.2, fy=0.2)
    roi = roi[y: y + h, x: x + w]

    return roi


if __name__ == "__main__":
    debug = True
    script_path = os.path.dirname(os.path.realpath(__file__))
    # img_path = os.path.join(script_path, "images/IMG_2813.jpg")
    # img_path = os.path.join(script_path, "images/IMG_2859.jpg")
    img_path = os.path.join(script_path, "images/IMG_2836.jpg")

    # get region of interest
    roi = segment_roi(img_path, False)

    # detect protein and gluecose
    protein = detect(roi, "PROTEIN", True)
    glucose = detect(roi, "GLUCOSE", True)

    # plot histogram
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.hist(protein.ravel(), 256, [0, 256])
    plt.hist(glucose.ravel(), 256, [0, 256])
    plt.show()

    # block till you receive keyboard event
    if debug:
        cv2.waitKey(0)
