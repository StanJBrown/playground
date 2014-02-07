#!/usr/bin/env python
import cv2


def draw_detection_area(video_frame):
    cv2.rectangle(video_frame, (10, 10), (100, 100), (0, 255, 0), 3)


if __name__ == "__main__":
    # find the webcam
    capture = cv2.VideoCapture(0)

    # video recorder config
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video_writer = cv2.VideoWriter("output.avi", fourcc, 20, (680, 480))

    # record video
    while (capture.isOpened()):
        ret, frame = capture.read()
        if ret:
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # video_writer.write(frame)

            cv2.imshow('Video Stream', frame)
            # cv2.imshow('HSV', hsv_frame)

        else:
            break

    capture.release()
    video_writer.release()
    cv2.destroyAllWindows()
