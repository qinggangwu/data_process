

import math
import os
import random
import xlrd
import time
import xlsxwriter
import shutil
import cv2
import onnxruntime
import numpy as np


def resize_norm_img(img, image_shape):
    imgC, imgH, imgW = image_shape
    h = img.shape[0]
    w = img.shape[1]
    ratio = w / float(h)
    if math.ceil(imgH * ratio) > imgW:
        resized_w = imgW
    else:
        resized_w = int(math.ceil(imgH * ratio))
    resized_image = cv2.resize(img, (resized_w, imgH))
    resized_image = resized_image.astype('float32')
    if image_shape[0] == 1:
        resized_image = resized_image / 255
        resized_image = resized_image[np.newaxis, :]
    else:
        resized_image = resized_image.transpose((2, 0, 1)) / 255
    resized_image -= 0.5
    resized_image /= 0.5
    padding_im = np.zeros((imgC, imgH, imgW), dtype=np.float32)
    padding_im[:, :, 0:resized_w] = resized_image
    return padding_im


def decode(t, length, raw=False):    #   t 最大值列表。  length = 25
    alphabet = "0123456789:-"
    # alphabet = "0123456789.-{}<>="
    char_list = []
    for i in range(length):
        if t[i] != 0 and (not (i > 0 and t[i - 1] == t[i])):
            char_list.append(alphabet[t[i] - 1])
    return ''.join(char_list)

def read_img(img,shape,n = 30):
    x0,y0  = 40,44
    w0,h0 = 60,920
    wt,ht = 0,22
    img_list = []

    cat_timeimg = img[ (shape[0] - 37): (shape[0] - 20) , (shape[1] - 73) :(shape[1] - 73  + 40)]
    img_list.append(cat_timeimg)
    # cv2.rectangle(img, ((shape[0] - 37), (shape[1] - 73)), ((shape[0] - 20), (shape[1] - 73 + 40)), (0, 0, 255), 3)
    # cv2.imshow('test', img)
    # cv2.waitKey(500)
    for i in range(n):
        cat_img = img[ int(y0): int(y0 +ht), x0:(x0 +w0)]
        img_list.append(cat_img)
        y0 = int(y0 + ht)

    # cv2.rectangle(img, left_top, right_bottom, (0, 0, 255), 3)
    #     cv2.rectangle(img ,  (x0,y0 ),((x0 +w0) ,(y0 +ht)) ,(0, 0, 255), 3)
    #     cv2.imshow('test',img)
    #     cv2.waitKey(500)
    return img_list

def read_img2(img,shape,n = 30):
    x0,y0  = 42,100
    w0,ht = 60,23
    img_list = []

    cat_timeimg = img[ (shape[0] - 92): (shape[0]-76) , (shape[1] - 79) :(shape[1]-40)]
    img_list.append(cat_timeimg)
    cv2.imwrite("D:/tt/{}.jpg".format(random.randint(0,10000)), cat_timeimg)
    # cv2.rectangle(img, ((shape[1] - 79),(shape[0] - 92)), ((shape[1]-40),(shape[0]-76)), (0, 0, 255), 1)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)


    for i in range(n):
        cat_img = img[ int(y0): int(y0 +ht), x0:(x0 +w0)]
        img_list.append(cat_img)

        y0 = int(y0 + ht)

    #     cv2.rectangle(img ,  (x0,y0 ),((x0 +w0) ,(y0 +ht)) ,(0, 0, 255), 1)
    #     cv2.imshow('test',img)
    #
    #     # cv2.waitKey(500)
    #     y0 = int(y0 + ht)
    # cv2.waitKey(0)
    return img_list


def get_gp_imglist(path):
    # path = 'imgname'    # 图片名称
    img =  cv2.imread(path)
    if img != None:
        imgshape = img.shape
        if imgshape[0] == 1080:
            imglist = read_img(img,imgshape,43)
        elif imgshape[0]== 800:
            imglist = read_img(img, imgshape,30)
        elif imgshape[0]== 1050:
            imglist = read_img2(img, imgshape, 35)
        elif imgshape[0]== 960:
            pass
            # imglist = read_img(img, 35)
        else:
            return []

        return imglist

    return []

def read_excel(expath):
    try:
        book = xlrd.open_workbook(expath)  # 打开一个工作表
        sheet1 = book.sheet_by_index(0)  # 通过索引获取表
        nrows = sheet1.ncols  # 表的行数
        info_list= []
        for i in range(nrows):
            info_list.append(sheet1.col_values(i))
        return info_list
    except:
        return []

def write_excel(imglist,imgpath,expath,infolist = [] ):


    img_list =imglist
    for name in sorted(img_list):
        sj = name[11:16].replace("_",":")
        info = ['时间']
        info.append(sj)
        path = os.path.join( imgpath,name)
        img  = get_gp_imglist(path)
        rez= shibei(img)
        print(rez)
        info = info +rez
        infolist.append(info)
    workbook = xlsxwriter.Workbook(expath)  # 创建一个excel文件
    worksheet = workbook.add_worksheet('sheet1')

    for i in range(len(infolist)):
        for j in range(len(infolist[i])):
            worksheet.write(j, i, infolist[i][j])

    workbook.close()
    nwename = time.strftime("%Y-%m-%d", time.localtime())
    nwetxt= expath.replace('实时更新文件不要打开',str(nwename))
    # print(expath, nwetxt)
    # shutil.copy(expath, nwetxt)
    try:
        # print(expath, nwetxt)
        shutil.copy(expath, nwetxt)
    except:
        pass

def shuaxinfile(path,n:int):
    imglist = os.listdir(path)
    imglist = sorted(imglist)
    m = len(imglist)
    if m>n:
        return imglist[-(m-n):] ,m
    else:
        return [],m

def shibei(img_list):
    session = onnxruntime.InferenceSession("nu.onnx")
    input_name = getattr(session.get_inputs()[0], 'name')
    s = []
    for img in img_list:
        img = resize_norm_img(img, [3, 32, 100])
        preds = session.run([], {input_name: img[np.newaxis, :]})
        preds = np.unravel_index(np.argmax(preds[0][0], axis=1), preds[0][0].shape)[1]   # 获取每个预测位置上的最大值索引
        sim_pred = decode(preds, 25, raw=False)
        s.append(sim_pred)
    return s

def mian():
    expath = 'D:/实时更新文件不要打开.xls'
    imgpath = 'D:/2/'
    imgnu = 0

    while True:
        imglist ,imgnum =shuaxinfile(imgpath,imgnu)
        if imgnum >imgnu:
            infolist = read_excel(expath)
            if len(infolist)==0 or imgnu ==0:
                infolist =[]
                info = ['序号','截图时间','识别时间' ] +[str(i) for i in range(1,50) ]
                infolist.append(info)
                write_excel(imglist ,imgpath,expath,infolist)
            else:
                write_excel(imglist ,imgpath,expath,infolist)
            imgnu = imgnum
        time.sleep(6)

        if not os.path.exists(expath):
            imgnu = 0

if __name__ == '__main__':

    # mian()

    s = time.time()
    img_list = os.listdir('D:/tt/')
    list = []
    for name in img_list:
        img = cv2.imread('D:/tt/'+name)
        list.append(img)
        # print(shibei(list))

    wulist = wushibei(list)
    print(time.time() -s)

