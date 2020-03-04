import numpy as np
#import cv2
from controller import Controller
from tracker import LineTracker

class LRTracker(LineTracker):
    def __init__(self, cap):
        super().__init__(cap)

    def track_line(self):
        roi = self._get_frame()
        if not frame:
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # Color thresholding
        ret, thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

        # Find the contours of the frame
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Find the biggest contour (if detected)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            if M['m00'] == 0:
                return None

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(roi,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(roi,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(roi, contours, -1, (0,255,0), 1)

            cv2.imshow('Preview', frame)

            if cx >= 100:
                print("Turn Right!")
            if cx < 100 and cx > 70:
                print("On Track!")
            if cx <= 70:
                print("Turn Left")
            print(cx)
            return cx
        return -1
