import cv2
import numpy as np

# CHANGE 1


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

my_points = []

my_colors = [[57, 45, 99, 74, 255, 255],                # HSV values for dark green
             [161, 80, 137, 179, 255, 255],             # HSV values for pink
             [102, 98, 133, 124, 255, 255]]             # HSV values for blue

my_color_values = [[102, 204, 0],                       # RGB values for dark green
                   [102, 0, 204],                       # RGB values for pink
                   [255, 0, 0]]                         # RGB values for blue


def find_color(image, colors, color_values, points):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    count = 0
    for color in colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(img_hsv, lower, upper)
        x, y = get_contours(mask)
        cv2.circle(img_result, (x, y), 10, color_values[count], cv2.FILLED)
        if x != 0 and y != 0:
            points.append([x, y, count])
        count += 1


def get_contours(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:                                                # To ensure no noise
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y


def draw(points, color_values):
    for p in points:
        cv2.circle(img_result, (p[0], p[1]), 10, color_values[p[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img_result = img.copy()
    find_color(img, my_colors, my_color_values, my_points)
    if len(my_points) != 0:
        draw(my_points, my_color_values)
    cv2.imshow("Result", img_result)
    if cv2.waitKey(1) == ord('q'):
        break

