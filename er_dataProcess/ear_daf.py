#!usr/bin/env python
# encoding:utf-8
from __future__ import division



import io
import os
import sys
import cv2
import time
import json
import base64
import random
import numpy
import datetime
import requests
from PIL import Image
from flask import *
from scipy import misc
import numpy as np
from matplotlib import pyplot as plt

plt.clf()
plt.figure(figsize=(10, 8))

demo = Image.open('E:/BaiduNetdiskDownload/orgimage/a.png')
h, w = demo.size

plt.subplot(2, 3, 1)
plt.imshow(demo)
plt.title("original")

img = cv2.imread('E:/BaiduNetdiskDownload/orgimage/a.png')
print(img.shape)
area = h * w
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

plt.subplot(2, 3, 2)
plt.imshow(hsv)
plt.title("HSV")

h, w, way = img.shape
total = h * w
print('h: ', h, 'w: ', w, 'area: ', total)
# 对号、错号
lower = [0, 40, 0]
upper = [179, 255, 255]
lower = np.array(lower, dtype="uint8")
upper = np.array(upper, dtype="uint8")
mask = cv2.inRange(hsv, lower, upper)
output = cv2.bitwise_and(hsv, img, mask=mask)

count = cv2.countNonZero(mask)
print('count: ', count)
now_ratio = round(int(count) / total, 3)
print('now_ratio: ', now_ratio)

plt.subplot(2, 3, 3)
plt.imshow(output)
plt.title("mask,ratio: " + str(now_ratio))

result = {}
result['count'], result['ratio'] = count, now_ratio
print('output: ', output)

plt.subplot(2, 3, 4)
plt.imshow(output)
plt.title('HSV2BGR')

gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
print('gray: ', gray)

plt.subplot(2, 3, 5)
plt.imshow(gray)
plt.title("gray")

ret, output = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('contours_num: ', len(contours))
count_dict = {}
areas, lengths = 0, 0
for i in range(len(contours)):
    one = contours[i]
    one_lk = one.tolist()
    if len(one_lk) >= 2:
        area = cv2.contourArea(one)
        length = cv2.arcLength(one, True)
        areas += area
        lengths += length
        left_list, right_list = [O[0][0] for O in one_lk], [O[0][1] for O in one_lk]
        minX, maxX, minY, maxY = min(left_list), max(left_list), min(right_list), max(right_list)
        A = abs(maxY - minY) * abs(maxX - minX)
        print('area: ', area, 'A: ', A, 'length: ', length)
        count_dict[i] = [A, area, length, [minX, maxX, minY, maxY]]
sorted_list = sorted(count_dict.items(), key=lambda e: e[1][0], reverse=True)
print(sorted_list[:10])
result['value'] = count_dict
cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

print('==========================================================================')
if sorted_list:
    filter_list = filterBox(sorted_list)
    for one_box in filter_list:
        print('one_box: ', one_box)
        A, area, length, [minX, maxX, minY, maxY] = one_box
        print('sorted_area: ', A, area)
        cv2.rectangle(img, (minX, maxY), (maxX, minY), (0, 255, 0), 10)

plt.subplot(2, 3, 6)
plt.imshow(img)
Sratio = round(areas / total, 3)
try:
    Lratio = round((2 * h + 2 * w) / lengths, 3)
except:
    Lratio = 0
plt.title("areas:" + str(round(areas, 1)) + ',len:' + str(round(lengths, 1))
          + '\nSratio:' + str(Sratio) + ',Lratio:' + str(Lratio))
plt.show()