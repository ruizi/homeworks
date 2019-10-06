import os

import cv2
import numpy as np
from numpy.matlib import random


def get_random():
    x = random.randint(0, 17)
    y = random.randint(0, 13)
    return x, y


def draw_line(img, x0, y0, x, y):
    # cv2.line(img, (x0, y0), (x, y), (0, 0, 255))
    return x, y


def draw_random_line(img, loc, number):
    a = np.zeros((number, number))
    temp = 0
    for i in range(number):
        for j in range(number):
            if temp == 2:
                temp = 0
                break
            else:
                a[i][j] = random.randint(0, 2)
                if a[i][j] == 1:
                    temp += 1
    # print(a)
    for i in range(number):
        for j in range(number):
            if a[i][j] == 1:
                cv2.line(img, loc[i], loc[j], (0, 0, 0))

    return img


def add_point(imgPath, number):
    number = int(number)
    print(number)
    print(imgPath)
    img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
    w, h = img.shape[:2]
    print(w, h)
    w_l = int(w / 50)
    h_l = int(h / 50)
    # print(w_l)
    # print(h_l)
    # print(w_l * h_l)
    points = 0
    loc = []
    x0 = 0
    y0 = 0
    # loc = np.array(loc)
    for points in range(number):
        x, y = get_random()
        while (x, y) in loc:
            x, y = get_random()
        cv2.circle(img, (x * 50 + 25, y * 50 + 25), 15, (225, 0, 0), 2)
        points += 1
        cv2.putText(img, str(points), (x * 50 + 15, y * 50 + 25), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 225), 1)
        loc.append((x * 50 + 25, y * 50 + 25))
        x0, y0 = draw_line(img, x0, y0, x * 50 + 25, y * 50 + 25)

    img = draw_random_line(img, loc, number)
    imgPath_pre = imgPath.split('.')[0]
    imgPath_pre += "_out."
    imgPath_pre_change = imgPath_pre.split('image')[0] + "\image\image_processed" + imgPath_pre.split('image')[1]
    imgPath_out = imgPath_pre_change + imgPath.split('.')[1]
    cv2.imwrite(imgPath_out, img)
    return loc, imgPath_out

# cv2.circle(vis, (x1, y1), 10, (0, 255, 0))
# add_point(30)
