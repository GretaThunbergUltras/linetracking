import sys

import cv2

if '--lr' in sys.argv:
    from lr_tracking import LineTracking
else:
    from contours_tracking import LineTracking

cap = cv2.VideoCapture('simpleline.mp4')
ln = LineTracking(cap)

while True:
    ln.track_line()
    cv2.waitKey(1)

test.release()
cv2.closeAllWindows()
