#!/usr/bin/env python
import cv2
import numpy as np


def hsv_callback(val):
    pass


def create_hsv_gui(hsv_vals):
    window = "hsv"
    cv2.namedWindow(window)
    cv2.createTrackbar("Hue Min", window, hsv_vals[0], 255, hsv_callback)
    cv2.createTrackbar("Hue Max", window, hsv_vals[3], 255, hsv_callback)
    cv2.createTrackbar("Sat Min", window, hsv_vals[1], 255, hsv_callback)
    cv2.createTrackbar("Sat Max", window, hsv_vals[4], 255, hsv_callback)
    cv2.createTrackbar("Val Min", window, hsv_vals[2], 255, hsv_callback)
    cv2.createTrackbar("Val Max", window, hsv_vals[5], 255, hsv_callback)


def draw_detection_area(video_frame):
    center_x = video_frame.shape[1] / 2
    center_y = video_frame.shape[0] / 2

    area_size = 10
    top_left = (center_x - area_size, center_y - area_size)
    bottom_right = (center_x + area_size, center_y + area_size)

    cv2.rectangle(video_frame, top_left, bottom_right, (0, 0, 255), 3)
    return video_frame


def pixel_get_hsv(video_frame):
    center_x = video_frame.shape[1] / 2
    center_y = video_frame.shape[0] / 2

    hsv_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2HSV)
    hsv = hsv_frame[center_y][center_x]
    hue = hsv[0]
    sat = hsv[1]
    val = hsv[2]

    print hue, sat, val

    return (hue, sat, val)


def update_hsv_gui(hsv, hue_range=50):
    hue, sat, val = hsv
    hue_min = hue - hue_range if hue - hue_range > 0 else 0
    hue_max = hue + hue_range if hue + hue_range < 255 else 255
    sat_min = 100
    sat_max = 255
    val_min = 100
    val_max = 255

    cv2.setTrackbarPos("Hue Min", "hsv", hue_min)
    cv2.setTrackbarPos("Sat Min", "hsv", sat_min)
    cv2.setTrackbarPos("Val Min", "hsv", val_min)

    cv2.setTrackbarPos("Hue Max", "hsv", hue_max)
    cv2.setTrackbarPos("Sat Max", "hsv", sat_max)
    cv2.setTrackbarPos("Val Max", "hsv", val_max)


def draw_on_tracked_obj(x, y, frame):
    cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)
    cv2.putText(frame, "Tracking!", (0, 0), 1, 1, (0, 255, 0), 2)


def detect(orig_frame, thres_frame, contour_area=300):
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(thres_frame, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(
        dilate,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # loop through discovered contour
    detected = []
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > contour_area:
            # obtain contour center and append to detected
            M = cv2.moments(contours[i])
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            detected.append((cx, cy))

            # draw detected contour
            cv2.drawContours(orig_frame, contours, i, (0, 255, 0), 3)

            # draw rectangle
            x, y, w, h = cv2.boundingRect(contours[i])
            cv2.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("Detected", orig_frame)

    return detected


def cleanup(capture):
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    CV_CAP_PROP_FRAME_WIDTH = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4

    width = 640
    height = 480

    hsv_vals = (
        20,  # hue_min
        0,  # sat_min
        0,  # val_min
        75,  # hue_max
        255,  # sat_max
        255,  # val_max
    )

    # find the webcam
    capture = cv2.VideoCapture(0)
    capture.set(CV_CAP_PROP_FRAME_WIDTH, width)
    capture.set(CV_CAP_PROP_FRAME_HEIGHT, height)

    # create gui
    create_hsv_gui(hsv_vals)

    # record video
    detection_area = False
    get_hsv = False
    while (capture.isOpened()):
        ret, frame = capture.read()
        key = cv2.waitKey(50)

        if ret:
            if key == 27 or key == ord('q'):
                cleanup(capture)
                break
            elif key == ord('d'):
                detection_area = not detection_area
            elif key == ord('h'):
                get_hsv = not get_hsv
            else:
                # draw detection area
                if detection_area:
                    draw_detection_area(frame)

                # detect hsv value in detection area and update hsv gui
                if get_hsv:
                    hsv = pixel_get_hsv(frame)
                    update_hsv_gui(hsv)

                # get hsv values from hsv gui
                lbound = (
                    cv2.getTrackbarPos("Hue Min", "hsv"),
                    cv2.getTrackbarPos("Sat Min", "hsv"),
                    cv2.getTrackbarPos("Val Min", "hsv")
                )

                ubound = (
                    cv2.getTrackbarPos("Hue Max", "hsv"),
                    cv2.getTrackbarPos("Sat Max", "hsv"),
                    cv2.getTrackbarPos("Val Max", "hsv")
                )

                # draw video and threshold windows
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                thres_frame = cv2.inRange(hsv_frame, lbound, ubound)

                cv2.imshow('Video Stream', frame)
                cv2.imshow('Threshold', thres_frame)
                detect(frame, thres_frame)
        else:
            break
