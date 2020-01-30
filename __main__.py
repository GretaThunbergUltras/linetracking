import cv2
import numpy as np
import time
import brickpi3

line_coordinates = 0, 0, 0, 0

def region_of_interest(edges2):
    height, width = edges2.shape
    print(width)
    print(height)
    mask2 = np.zeros_like(edges2)

    # only focus bottom half of the screen
    polygon = np.array([[
        (width * 1/3, height * 2 / 3),
        (width * 2/3, height * 2 / 3),
        (width * 2/3, height),
        (width * 1/3, height),
    ]], np.int32)

    cv2.fillPoly(mask2, polygon, 255)
    cropped_edges2 = cv2.bitwise_and(edges2, mask2)
    return cropped_edges2

def detect_line_segments(cropped_edges2):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 30  # minimal of votes
    line_segments2 = cv2.HoughLinesP(cropped_edges2, rho, angle, min_threshold,
                                    np.array([]), minLineLength=8, maxLineGap=1)
    return line_segments2

def average_slope_intercept(frame2, line_segments2):
    lane_lines = []
    if line_segments2 is None:
        return lane_lines

    height, width, _ = frame2.shape
    left_fit = []

    for line_segment in line_segments2:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            left_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:

        lane_lines.append(make_points(frame2, left_fit_average))

    return lane_lines

def make_points(frame3, line):
    height, width, _ = frame3.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 2 / 3)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    global line_coordinates
    line_coordinates = [x1, y1, x2, y2]
    return [[x1, y1, x2, y2]]

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=4):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image

def line_tracking(line_coordinates, edges):
    x1, y1, x2, y2 = line_coordinates
    height, width = edges.shape

    bottom_center = width * 1/2
    delta = bottom_center - x1
    if delta > -100 and delta < 100:
        if (delta < -10):
            print(bottom_center - x1)
            BP.set_motor_power(BP.PORT_B, 20)
            BP.set_motor_position(BP.PORT_D, 100)


        elif delta > 10:
            print(bottom_center - x1)
            BP.set_motor_power(BP.PORT_B, 30)
            BP.set_motor_position(BP.PORT_D, -20)

        else:
            print(bottom_center - x1)
            BP.set_motor_power(BP.PORT_B, 30)
            BP.set_motor_position(BP.PORT_D, 0)
    else:
        print(bottom_center - x1)
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_position(BP.PORT_D, 0)


BP = brickpi3.BrickPi3()

cap = cv2.VideoCapture(0)

while (True):

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 100, 40])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    edges = cv2.Canny(mask, 100, 200)
    cropped_edges = region_of_interest(edges)
    line_segments = detect_line_segments(cropped_edges)
    lane_lines2 = average_slope_intercept(frame, line_segments)
    cv2.imshow('edges', edges)
    cv2.imshow('cropped_edges', cropped_edges)
    lane_lines_image = display_lines(frame, lane_lines2)
    cv2.imshow("lane lines", lane_lines_image)

    #cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)

    print(line_coordinates)

    line_tracking(line_coordinates, edges)

    time.sleep(0.1)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_position(BP.PORT_D, 0)
        break

cv2.destroyAllWindows()
