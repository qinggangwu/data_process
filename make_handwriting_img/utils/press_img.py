

import cv2
import random
import imutils
import numpy as np
import math


class press_img(object):
    def __init__(self, zisize,n):
        self.zisize = (zisize[1],zisize[0])
        self.textleng = n
        # pass

    def roate_img(self, img, ro=15):
        shape = img.shape  # shape (h,w,c)
        if len(shape) == 3:
            h, w, c = shape
        else:
            h, w, c = shape[0], shape[1], 1


        imgD = np.ones((5*h, 5*w), dtype=np.uint8) * 255     # h,w
        imgDi = cv2.cvtColor(imgD, cv2.COLOR_GRAY2BGR)
        # x, y = (300 - w) // 2, (300 - h) // 2
        if c < 3:
            imgDi[2*h:3*h, 2*w:3*w] = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            imgDi[2*h:3*h, 2*w:3*w] = img[:, :, :3]
        ron = random.randint(-ro, ro)
        rotated = imutils.rotate(imgDi, ron, center=(int(2.5*w), int(2.5*h)))
        ypianzhi = int (abs(w/2 * math.sin(ron))//3)
        # print(ron , h,ypianzhi)
        reimg = rotated[2*h - ypianzhi :3*h + ypianzhi, 2*w - 3:3* w + 3]
        # cv2.imshow('ro',reimg)
        # cv2.waitKey(0)
        return reimg

    def img2rgba(self, img, roate=False):
        # path = "D:/data/CASIA/test/01383/249616.png"
        # img = cv2.imread(path)
        # img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        if roate:
            image_3 = cv2.resize(self.roate_img(img,10), (300*self.textleng, 300))

        else:
            image_3 = cv2.resize(img, (300*self.textleng, 300))

        gary_img = image_3[:, :, 0]
        # print(path)
        erzhihua_img = cv2.adaptiveThreshold(cv2.resize(gary_img, (300*self.textleng, 300)), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 2)
        # _ ,erzhihua_img = cv2.threshold(cv2.resize(gary_img, (300*self.textleng, 300)), 250, 255 ,cv2.THRESH_BINARY|cv2.THRESH_OTSU )   # ,cv2.THRESH_BINARY|cv2.THRESH_OTSU
        # _ ,erzhihua_img = cv2.threshold(cv2.resize(gary_img, (300*self.textleng, 300)), 250, 255 ,cv2.THRESH_BINARY)   # ,cv2.THRESH_BINARY|cv2.THRESH_OTSU
        # cv2.imshow('erzhihua_img', erzhihua_img)
        # cv2.waitKey(500)

        # 腐蚀操作，让书写更细
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        erode = cv2.dilate(erzhihua_img, kernel, iterations=1)
        # erode = cv2.dilate(erode, kernel, iterations=1)
        # cv2.imshow('erode', erode)
        # cv2.waitKey(0)
        image = np.dstack([image_3, erode])
        return cv2.resize(image, self.zisize)


    def cat_bgimg(self, imgbg, bg_size=(120,350)):

        shape = imgbg.shape  # shape (h,w,c)
        # print(path,shape)

        if shape[1] > bg_size[1] and shape[0] > bg_size[0] :
            x = random.randint(0, shape[1] - bg_size[1])
            y = random.randint(0, shape[0] - bg_size[0])
            img = imgbg[y:(y + bg_size[0] ), x:(x + bg_size[1])]

            return img

        elif shape[1] < bg_size[1]//3 or shape[0] < bg_size[0]//3 :
            rot = max(bg_size[1]/shape[1] +0.1 , bg_size[0]/shape[0] +0.1)
            imgbg = cv2.resize(imgbg, dsize=None, fx=rot, fy=rot)
            shape = imgbg.shape  # shape (h,w,c)

        x = random.randint(0, shape[1] - bg_size[1]//3)
        y = random.randint(0, shape[0] - bg_size[0]//3)
        img = imgbg[y:(y + bg_size[0]//3), x:(x +bg_size[1]//3)]

        return cv2.resize(img, (bg_size[1],bg_size[0] ))


    def pingjie_img(self,imglist,ziti_jianju ):
        """
        输入一个列表，存放需要拼接的图片
        :param imglist:   传入的图片列表
        :param ziti_jianju:  字符之间的间距
        :param n:  图片数量
        :return:
        """

        # imglist = [cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR) for path in imglist]



        imgshape_list = [img.shape for img in imglist ]

        n = len(imglist)
        bg_size = (max([ sh[0] for sh in imgshape_list ]) ,sum(sh[1] for sh in imgshape_list) + ziti_jianju*(n-1) )

        whitebg = np.ones(bg_size, np.uint8) * 255  # h,w
        whitebg = cv2.cvtColor(whitebg, cv2.COLOR_GRAY2BGR)

        # pre = press_img(bg_size, n)  # 实例化图像处理对象
        x, y = 0, (max([ sh[0] for sh in imgshape_list ]) -imgshape_list[0][0])//2     # 拼接第一张图片的位置
        for index,img in enumerate(imglist):
            # img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
            # 拼接字体
            # img = cv2.resize(img, size)

            imgsize = imgshape_list[index][:2]
            ah, aw = imgsize
            y = (max([ sh[0] for sh in imgshape_list ]) -ah)//2
            whitebg[y:y + ah, x:x + aw] = img
            x = x + aw + ziti_jianju
        return whitebg

def text():

  """
  高斯滤波，边缘模糊
  blur = cv2.GaussianBlur(img,(5,5),0)
  
  
  颜色滤镜
   enum
    {
        COLORMAP_AUTUMN = 0,
        COLORMAP_BONE = 1,
        COLORMAP_JET = 2,
        COLORMAP_WINTER = 3,
        COLORMAP_RAINBOW = 4,
        COLORMAP_OCEAN = 5,
        COLORMAP_SUMMER = 6,
        COLORMAP_SPRING = 7,
        COLORMAP_COOL = 8,
        COLORMAP_HSV = 9,
        COLORMAP_PINK = 10,
        COLORMAP_HOT = 11
    }
    import cv2
    im_gray = cv2.imread("pluto.jpg", cv2.IMREAD_GRAYSCALE)
    im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)
  """