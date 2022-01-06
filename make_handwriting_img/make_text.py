# -*- coding:utf-8 -*-

import cv2
import time
import os
import random
import numpy as np
import utils.util as util
from utils.press_img import press_img


def gasuss_noise(image, mean=0, var=0.001):
    '''
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    #cv.imshow("gasuss", out)
    return out


def sp_noise(image,prob):
    '''
    添加椒盐噪声
    prob:噪声比例
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def xuhua_peroce():
    imgdir = 'E:/make_img/text/ro/'
    imgList = util.get_allimg(imgdir)

    for imgPath in imgList:
        saveName = imgPath.replace('ro','xuhua').replace('la','xh')
        xhFlag = random.choice([True,False])
        noiseFlag = random.choice([True,False])
        k = random.choice([3,5,7,9,11,13])
        if xhFlag:
            img = cv2.imdecode(np.fromfile(imgPath, dtype=np.uint8), cv2.IMREAD_COLOR)
            if noiseFlag:
                img = gasuss_noise(img)
                # img = sp_noise(img,0.01)
            blur = cv2.GaussianBlur(img, (k, k), 0)

        else:
            continue
        cv2.imencode('.png', blur)[1].tofile(saveName)
            # "E:/make_img/text/noro/la_{}_{}.png".format(label, random.randint(100000, 999999)))  # 保存图片





def main():

    textList = util.changyongzi('yuliao')
    # Imgdict = {zi: util.get_allimg("D:/data/CASIA/train/" + zi) for zi in textList }
    Imgdict = util.getFormtxt_imgDict(textList, 'D:/data/CASIA/train.txt')
    # print(Imgdict);quit()

    labeltxt = open('E:/Pytorch/make_handwriting_img/yuliaoku.txt','r',encoding= 'utf-8').readlines()

    text_num = 1000000    # 生成图片的数量
    for text_ in range(text_num):
        ziti_jianju = random.randint(0, 20)      # 字体间距
        ziti_size = random.randint(14, 24)
        size = (5 * ziti_size, 5 * ziti_size)  # 字体图片缩放大小

        # labeltxt = ['缥饯禅杳', '饯孜', '戮禅', '褶禅褶禅褶禅褶禅杳峨禅', '褶禅', '孜峨孜', '孜霄', '褶禅禅', '褶禅孜', '寰孜', '鲈孜',]

        label = util.get_label('text', labeltxt)

        if len(label) <= 0:
            continue
        # print(label)
        if text_ % 1000 == 0:
            print("{}   已经创建{}个，已经完成{}%".format(time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())) , text_, round(text_/text_num,3)))      #没创建100个输出一次

        # 创建白色背景
        # x, y =0,0
        # bg_size = (5 * ziti_size , 5 * ziti_size *len(label)+ ziti_jianju*(len(label)-1))

        # print(bg_size)

        imgpathList = [random.choice(Imgdict[zi]) for zi in label]
        imglist = [cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR) for path in imgpathList]
        imgshape_list = [img.shape for img in imglist ]

        bg_size = (max([ sh[0] for sh in imgshape_list ]) ,sum(sh[1] for sh in imgshape_list) + ziti_jianju*(len(label)-1) )

        pre = press_img(bg_size, len(label))  # 实例化图像处理对象
        whitebg = pre.pingjie_img(imglist,ziti_jianju)

        # 拼接图片
        # whitebg = np.ones(bg_size, np.uint8) * 255  # h,w
        # whitebg = cv2.cvtColor(whitebg, cv2.COLOR_GRAY2BGR)
        #
        # x, y = 0, (max([ sh[0] for sh in imgshape_list ]) -imgshape_list[0][0])//2     # 拼接第一张图片的位置
        # for index,img in enumerate(imglist):
        #     # img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        #     # 拼接字体
        #     # img = cv2.resize(img, size)
        #
        #     imgsize = imgshape_list[index][:2]
        #     ah, aw = imgsize
        #     y = (max([ sh[0] for sh in imgshape_list ]) -ah)//2
        #     whitebg[y:y + ah, x:x + aw] = img
        #     x = x + aw + ziti_jianju

        roflag = random.choice([True,False])
        iamgergba = pre.img2rgba(whitebg, roflag)

        # 创建背景
        bgList = [os.path.join('D:/bg/', name) for name in os.listdir('D:/bg/')]
        pathbg = random.choice(bgList)
        xbg, ybg = random.randint(3,20), random.randint(3,8)
        bg_sizebg = (bg_size[0] +ybg,bg_size[1]+xbg)
        imagebg = pre.cat_bgimg(cv2.imread(pathbg), bg_sizebg)  #

        alpha_imagebg = iamgergba[:, :, 3] / 255.0
        alpha_image = 1 - alpha_imagebg
        ahbg , awbg, =  bg_size


        for c in range(0, 3):
            imagebg[ybg: ybg + ahbg, xbg: xbg+ awbg, c] = ((alpha_imagebg * imagebg[ybg: ybg + ahbg, xbg: xbg+ awbg, c]) + (alpha_image * (iamgergba[0:ahbg, 0:awbg, c]//6-1)))
            # image_1[ya:ya+ah, xa:xa +aw, c] = ((alpha_image_3 * image_1[ya:ya+ah, xa:xa +aw, c]) + (alpha_image * (image_3[0:ah, 0:aw,c]//4 )))

        # cv2.imencode('.png', imagebg)[1].tofile(
        #     "E:/make_img/text/test/la_{}_{}.png".format(label, random.randint(100000, 999999)))  # 保存图片
        if roflag:
            cv2.imencode('.png', imagebg)[1].tofile("E:/make_img/text/ro/la_{}_{}.png".format(label,random.randint(100000,999999)))  # 保存图片
        else:
            cv2.imencode('.png', imagebg)[1].tofile("E:/make_img/text/noro/la_{}_{}.png".format(label, random.randint(100000, 999999)))  # 保存图片


if __name__ == "__main__":
    # main()
    xuhua_peroce()