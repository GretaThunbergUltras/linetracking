import sys

import cv2

cap = cv2.VideoCapture('simpleline.mp4')

if '--lr' in sys.argv:
    from lr_tracking import LRTracker
    ln = LRTracker(cap)
else:
    from contours_tracking import ContourTracker
    ln = ContourTracker(cap)

while True:
    ln.track_line()
    cv2.waitKey(1)

test.release()
cv2.closeAllWindows()
