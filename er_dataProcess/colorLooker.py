#!usr/bin/env python
# encoding:utf-8
from __future__ import division

'''
功能： HSV空间图片色素范围查看器
'''

import cv2
import numpy as np


def nothing(x):
    pass


def colorLooker(pic='1.png'):
    '''
    HSV空间图片色素范围查看器
    '''
    # 图像加载
    image = cv2.imread(pic)
    # 窗口初始化
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # 创建拖动条
    # Opencv中Hue取值范围是0-179
    cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'image', 0, 255, nothing)
    # 设置默认最大值
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)
    # 初始化设置
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0
    while (1):
        # 实时获取拖动条上的值
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')
        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')
        # 设定HSV的最大和最小值
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])
        # BGR和HSV颜色空间转化处理
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)
        # 拖动改变阈值的同时，实时输出调整的信息
        if ((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
            hMin, sMin, vMin, hMax, sMax, vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax
        # 展示由色素带阈值范围处理过的结果图片
        cv2.imshow('image', result)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    colorLooker(pic='E:/BaiduNetdiskDownload/orgimage/a.png')

