# -*- coding:utf-8 -*-

import cv2
import numpy as np
import random
import os
import imutils
from utils.util import changyongzi,get_label
import re


def get_allimg(path:str):
    imgList = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if os.path.splitext(filename)[-1] in ['.png','.jpg']:
                imgList.append(os.path.join(root,filename))
    return imgList

def get_imgpathDict(path:str):
    imgDict ={}
    imgfiledir = os.listdir(path)
    for filename in imgfiledir:
        if os.path.isdir(os.path.join(path,filename)):
            imgDict[filename] = get_allimg(os.path.join(path,filename))
    return imgDict

def roate_img(img ,ro =15):
    shape= img.shape     #shape (h,w,c)
    if len(shape) == 3:
        h,w,c = shape
    else:
        h, w, c = shape[0],shape[1],1
    imgD= np.ones((300, 300),dtype=np.uint8) * 255
    imgDi=cv2.cvtColor(imgD,cv2.COLOR_GRAY2BGR)
    x,y = (300 -w)//2 ,(300 -h)//2
    if c<3:
        imgDi[y:y + h, x:x + w] = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    else:
        imgDi[y:y+h, x:x+w] = img[:,:,:3]
    ron = random.randint(-ro,ro)

    rotated = imutils.rotate(imgDi, ron)

    reimg = rotated[y-5:y+h+5 ,x-5 :x+w+5]
    # cv2.imshow('ro',reimg)
    # cv2.waitKey(0)

    return reimg

def img2rgba(path,size,roate = False):
    # path = "D:/data/CASIA/test/01383/249616.png"
    # img = cv2.imread(path)
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    # cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    if roate:
        image_3 = cv2.resize(roate_img(img), (300,300))
    else:
        image_3 = cv2.resize(img, (300,300))

    gary_img = image_3[:,:,0]
    # print(path)
    erzhihua_img = cv2.adaptiveThreshold(cv2.resize(gary_img, (300,300)), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 2)
    # _ ,erzhihua_img = cv2.threshold(cv2.resize(gary_img, size), 250, 255 ,cv2.THRESH_BINARY|cv2.THRESH_OTSU )   # ,cv2.THRESH_BINARY|cv2.THRESH_OTSU
    # _ ,erzhihua_img = cv2.threshold(cv2.resize(gary_img, (300,300)), 250, 255 ,cv2.THRESH_BINARY)   # ,cv2.THRESH_BINARY|cv2.THRESH_OTSU
    # cv2.imshow('erzhihua_img', erzhihua_img)
    # cv2.waitKey(500)

    # 腐蚀操作，让书写更细
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    erode = cv2.dilate(erzhihua_img, kernel, iterations=1)
    erode = cv2.dilate(erode, kernel, iterations=1)
    # cv2.imshow('erode', erode)
    # cv2.waitKey(0)

    image = np.dstack([image_3, erode])

    return cv2.resize(image,size)

def cat_bgimg(bgList,n=3):
    path = random.choice(bgList)
    imagebg = cv2.imread(path)
    shape = imagebg.shape    #shape (h,w,c)
    # print(path,shape)
    if shape[1] <40*n+10 or shape[0] <50:
        imagebg = cv2.resize(imagebg, dsize=None, fx=2, fy=2)

    x = random.randint(0,shape[1]- 40*n+10 )
    y = random.randint(0,shape[0]- 50)
    img = imagebg[y:(y+50) , x:(x+40*n+10)]

    return cv2.resize(img,(100*n+50,120))


# def get_label(labeltype :str):
#     """
#     生成需要书写的数据 返回一个字符串
#     labeltype : 对应不同的 数据类型，有名字数据，
#
#
#     :param labeltype:
#     :return:
#     """
#
#     if labeltype == "bjx":
#         # bjxList = changyongzi('bjx')  # 获取百家姓
#         # bjxDict_num = {xing: 3000 for xing in bjxList}
#         global bjxList
#         xing_label = random.choice(bjxList)
#
#         mingziList =  changyongzi('500')[:10] # 获取常用2500字
#         mingzi_label = random.choices(mingziList, k=random.choice([1, 2, 2, 2, 2]))  # 随机获取一个字或者2个字
#         # label = xing_label + ''.join(mingzi_label)
#         return  (xing_label , ''.join(mingzi_label))





# global bjxDict_num
def make_bjx_img():

    mingziList = changyongzi('500')[:10]   # 获取常用2500字

    bjxList = changyongzi('bjx')[:10]  # 获取百家姓
    bjxDict_num = {xing: 10 for xing in bjxList}
    num = sum(bjxDict_num.values())
    xing_Imgdict = {xing:get_allimg("D:/data/CASIA/train/" + xing) for xing in bjxList if len(xing) == 1}
    xing_Imgdictfx1 = {xing[0]:get_allimg("D:/data/CASIA/train/" + xing[0]) for xing in bjxList if len(xing) == 2}
    xing_Imgdictfx2 = {xing[1]:get_allimg("D:/data/CASIA/train/" + xing[1]) for xing in bjxList if len(xing) == 2}


    # mingzi_Imgdict = get_imgpathDict("D:/data/CASIA/train/")    #  获取所有字符，时间较长
    mingzi_Imgdict = {xing:get_allimg("D:/data/CASIA/train/" + xing) for xing in mingziList }     # 获取mingziList 字符
    # mingzi_Imgdict = xing_Imgdict

    # print(xing_Imgdict.keys());quit()


    for ind in range(num):
        if ind % 100 ==0:
            print("已经创建{}个，已经完成{}%".format(ind, round(ind/num,3)))      #没创建100个输出一次
        imgpathList =[]
        label = get_label('bjx',(list(bjxDict_num.keys()) ,mingziList ))
        # xing_label = random.choice(list(bjxDict_num.keys()))
        xing_label = label[0]
        if len(xing_label) ==2:
            imgpathList.append(random.choice(xing_Imgdictfx1[xing_label[0]]) )
            imgpathList.append(random.choice(xing_Imgdictfx2[xing_label[1]]) )
        else:
            xing_imgpath = random.choice(xing_Imgdict[xing_label])
            imgpathList.append(xing_imgpath)

        # mingzi_label = random.choices(list(mingzi_Imgdict.keys()),k=random.choice([1,2,2,2,2]))     # 随机获取一个字或者2个字
        mingzi_label = label[1]
        label = xing_label + mingzi_label
        print(label)
        mingzi_imgpath = [random.choice(mingzi_Imgdict[ll]) for ll in mingzi_label ]
        imgpathList = imgpathList + mingzi_imgpath
        if bjxDict_num[xing_label] > 0:
            bjxDict_num[xing_label] -=1
        elif bjxDict_num[xing_label] == 0:
            del bjxDict_num[xing_label]
            # bjxList.remove(xing_label)

        bgList = [os.path.join('D:/bg/',name) for name in os.listdir('D:/bg/')]
        # imagebg = cv2.resize(cv2.imread(random.choice(bgList)),(350,120))
        imagebg = cat_bgimg(bgList,len(label))     # 背景截取长度和字符长度成正比
        # pathList = get_allimg("D:/data/CASIA/wutest/")

        x, y = 10, 10
        falg_ro = random.choice([True, False])  # 随机选择是否旋转字体 默认不旋转
        for imgpath in imgpathList:
            size = (100,100)
            img = img2rgba(imgpath,size,roate=falg_ro)
            alpha_image_3 = img[:, :, 3] / 255.0
            alpha_image = 1 - alpha_image_3
            aw, ah = size
            for c in range(0, 3):
                imagebg[y:y + ah, x:x + aw, c] = ((alpha_image_3 * imagebg[y:y + ah, x:x + aw, c]) + (alpha_image * (img[0:ah, 0:aw, c] // 6 - 1)))
                # image_1[ya:ya+ah, xa:xa +aw, c] = ((alpha_image_3 * image_1[ya:ya+ah, xa:xa +aw, c]) + (alpha_image * (image_3[0:ah, 0:aw,c]//4 )))
            x, y = x + aw + random.randint(-10, 5), y
            # cv2.imshow('test',cv2.resize(imagebg,dsize=None,fy=0.4,fx=0.4))
            # cv2.imshow('test',imagebg)
            # cv2.waitKey(0)


        if falg_ro:
            # cv2.imencode('.png', imagebg)[1].tofile("E:/make_img/qianming/roate/xm_{}_{}.png".format(label,random.randint(100000,999999)))  # 保存图片
            cv2.imshow('test', imagebg)
            cv2.waitKey(50)
        else:
            # cv2.imencode('.png', imagebg)[1].tofile("E:/make_img/qianming/noroate/xm_{}_{}.png".format(label,random.randint(100000,999999)))  # 保存图片
            cv2.imshow('test', imagebg)
            cv2.waitKey(50)


def make_yuliaoku():
    label = open('E:/Pytorch/PaddleOCR-release-2.2/train_data/chiese_all_train.txt','r',encoding= 'utf-8').readlines()
    labelList = []
    yuliao = open('E:/Pytorch/make_handwriting_img/yuliaokufuhao.txt','w',encoding= 'utf-8')

    for ss in label:
        ss = ss[:-1].split('\t')[1]
        infoch = re.findall('[\u4e00-\u9fa5，。：]', ss)


        fhList = ['，', '。','：']


        num = 0
        for s in infoch:
            if s in fhList:
                num+=1
        if len(infoch)>num :
            if infoch[0] in fhList:
                infoch.pop(0)
            labelList.append(''.join(infoch) + "\n")

    yuliao.writelines(labelList)
    yuliao.close()
    print(len(labelList))
    print(labelList)


def get_yuliaoku_zifu():
    yuliao = open('E:/Pytorch/make_handwriting_img/yuliaoku.txt', 'r', encoding='utf-8')

    yulist = []
    for s in yuliao:
        for ss in s:
            yulist.append(ss)
    return list(set(yulist))


def make_zifutxt():
    fw = open('D:\data\CASIA/train.txt','w',encoding='utf-8')
    l = []
    pathdim = "D:/data/CASIA/train/"
    imglist = os.listdir(pathdim)
    for name in imglist:
        paht = pathdim +name
        for imgname in get_allimg(paht):
            ss = name + ' ' + imgname + '\n'
            l.append(ss)

    fw.writelines(l)
    fw.close()





if __name__ =="__main__":

    # make_bjx_img()
    make_zifutxt()



    # eer = []
    # zifu3500 = changyongzi('3500')
    # oslist = os.listdir("D:\data\CASIA/train/")
    #
    # yuliao = get_yuliaoku_zifu()
    # print(len(yuliao))
    # for s in yuliao:
    #     # if s not in zifu3500 and s in oslist:
    #     if s not in  oslist:
    #         eer.append(s)
    # print(len(eer))
    # print(eer)
    # for i in range(100):
    #     wu_ss()


