#!/usr/bin/env python
from SimpleCV import Camera


if __name__ == "__main__":
    cam = Camera()

    while True:
        img = cam.getImage()
        img.show()
