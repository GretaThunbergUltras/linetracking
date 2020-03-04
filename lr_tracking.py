import numpy as np
import cv2
from controller import Controller

# RESOLUTION = (800, 600)

# (x, y, w, h)
class LineTracking():
    def __init__(self, cap):
        print("Init")

        self.set_resolution(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.video_capture = cap
        self.video_capture.set(3, 160)
        self.video_capture.set(4, 120)

    def set_resolution(self, width, height):
        self.resolution = (width, height)
        self.roi_w = self.resolution[0]//3
        self.roi_h = self.resolution[1]//2
        self.roi_x = self.resolution[0]//2 - self.roi_w//2
        self.roi_y = self.resolution[1] - self.roi_h
        
        self.roi_x2 = self.roi_x + self.roi_w
        self.roi_y2 = self.roi_y + self.roi_h

    def track_line(self):
        # Capture the frames
        print("Get frame")
        ret, frame = self.video_capture.read()

        if not ret:
            return None

        # Crop the image
        crop_img = frame[self.roi_y:self.roi_y2, self.roi_x:self.roi_x2]

        # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

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

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

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

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    lt = LineTracking()
    controller = Controller()
    while True:
        val = lt.track_line()
        if val:
            controller.controll(val)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
