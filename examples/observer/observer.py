#!/usr/bin/env python
import os

import cv2
import numpy as np


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

    return (hue, sat, val)


def update_hsv_gui(hsv):
    hue, sat, val = hsv
    hsv_range = 20

    hue_min = hue - hsv_range if hue - hsv_range > 0 else 0
    hue_max = hue + hsv_range if hue + hsv_range < 255 else 255

    sat_min = sat - hsv_range if sat - hsv_range > 0 else 0
    sat_max = sat + hsv_range if sat + hsv_range < 255 else 255

    val_min = val - hsv_range if val - hsv_range > 0 else 0
    val_max = val + hsv_range if val + hsv_range < 255 else 255

    cv2.setTrackbarPos("Hue Min", "hsv", hue_min)
    cv2.setTrackbarPos("Sat Min", "hsv", sat_min)
    cv2.setTrackbarPos("Val Min", "hsv", val_min)

    cv2.setTrackbarPos("Hue Max", "hsv", hue_max)
    cv2.setTrackbarPos("Sat Max", "hsv", sat_max)
    cv2.setTrackbarPos("Val Max", "hsv", val_max)


def draw_on_tracked_obj(x, y, frame):
    cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)
    cv2.putText(frame, "Tracking!", (0, 0), 1, 1, (0, 255, 0), 2)


def morph_op(orig_frame, thres_frame):
    # erode_el = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # frame = cv2.erode(frame, erode_el)
    # frame = cv2.erode(frame, erode_el)

    dilate_el = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    frame = cv2.dilate(thres_frame, dilate_el)
    frame = cv2.dilate(frame, dilate_el)
    frame = cv2.dilate(frame, dilate_el)
    frame = cv2.dilate(frame, dilate_el)
    frame = cv2.dilate(frame, dilate_el)

    contours = find_contours(frame)

    for contour in contours:
        if cv2.contourArea(contour) > 300:
            # moment = cv2.moments(contour)

            # try:
            #     cx = int(moment["m10"] / moment["m00"])
            #     cy = int(moment["m01"] / moment["m00"])
            # except Exception:
            #     cx = 0
            #     cy = 0

            # area_size = 10
            # top_left = (cx - area_size, cy - area_size)
            # bottom_right = (cx + area_size, cy + area_size)
            # cv2.rectangle(orig_frame, top_left, bottom_right, (0, 255, 0), 3)
            cv2.drawContours(orig_frame, contours, 0, (0, 255, 0), 3)
    cv2.imshow("Detected", orig_frame)

    return frame


def show_adaptive_gaussian_threshold(video_frame):
    cv2.imwrite('/tmp/opencv.jpg', video_frame)
    img = cv2.imread('/tmp/opencv.jpg', 0)
    img = cv2.medianBlur(img, 5)
    img = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    cv2.imshow('Adaptive Threshold', img)
    os.unlink("/tmp/opencv.jpg")

    return img


def find_contours(frame):
    img = cv2.Canny(frame, 100, 200)
    contours, hierarchy = cv2.findContours(
        img,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), -1)

    return contours


def find_circles(frame):
    # img = cv2.Canny(frame, 100, 200)
    # cv2.imshow("canny edge detection", img)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    cv2.imwrite('/tmp/opencv_circles.jpg', frame)
    img = cv2.imread('/tmp/opencv_circles.jpg', 0)
    img = cv2.medianBlur(img, 5)

    circles = cv2.HoughCircles(
        img,
        cv2.cv.CV_HOUGH_GRADIENT,
        1,
        20,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=50
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

            # draw the center of the circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imshow('detected circles', frame)


def hsv_callback(val):
    pass


def cleanup(capture, video_writer):
    capture.release()
    video_writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    CV_CAP_PROP_FRAME_WIDTH = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4

    width = 640
    height = 480

    hsv_vals = (
        0,  # hue_min
        0,  # sat_min
        0,  # val_min
        255,  # hue_max
        255,  # sat_max
        255,  # val_max
    )

    # find the webcam
    capture = cv2.VideoCapture(0)
    capture.set(CV_CAP_PROP_FRAME_WIDTH, width)
    capture.set(CV_CAP_PROP_FRAME_HEIGHT, height)

    # video recorder config
    # fourcc = cv2.cv.CV_FOURCC(*'IYUV')
    video_writer = cv2.VideoWriter("output.avi", -1, 20, (width, height))

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
                cleanup(capture, video_writer)
            elif key == ord('d'):
                detection_area = not detection_area
            elif key == ord('h'):
                get_hsv = not get_hsv
            else:
                # video_writer.write(frame)

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
                # cv2.imshow('Detection', frame)
                cv2.imshow('Morph', morph_op(frame, thres_frame))
                # img = show_adaptive_gaussian_threshold(frame)
                # find_circles(frame)
                # img = find_contours(frame)
                # cv2.imshow("Contours", img)
                # find_circles(frame)
        else:
            break
