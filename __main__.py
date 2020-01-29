#!/usr/bin/python3

import cv2 as cv
import numpy as np

RESOLUTION = (800, 600)
# (x, y, w, h)
ROI_W = RESOLUTION[0]//3
ROI_H = RESOLUTION[1]//2 
ROI_X = RESOLUTION[0]//2 - ROI_W//2
ROI_Y = RESOLUTION[1] - ROI_H

ROI_X2 = ROI_X + ROI_W
ROI_Y2 = ROI_Y + ROI_H

def contours(img):
    ret, thresh = cv.threshold(img, 127, 255, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    edges = cv.Canny(img, 100, 200)
    cv.drawContours(img, contours, -1, (0, 255, 0), 3)

def canny(img):
    edges = cv.Canny(img, 50, 150, 3)
    lines = cv.HoughLinesP(edges, 1, np.pi/180, 200)
    if not isinstance(lines, np.ndarray):
        return
    for rho, theta, _, _ in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)

def main():
    cap = cv.VideoCapture('test.mp4')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        roi = frame[ROI_Y:ROI_Y2, ROI_X:ROI_X2]

        contours(roi)
        # canny(roi)

        cv.rectangle(frame, (ROI_X, ROI_Y), (ROI_X2, ROI_Y2), (255, 0, 0))

        cv.imshow('preview', frame)
        if cv.waitKey(0) == 27:
            break;

    cv.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    main()
