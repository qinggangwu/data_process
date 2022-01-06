

import cv2
import shutil
import os


def qiegebiankuang(img):
    h,w = img.shape
    xi,yi,xa,ya = w,h,0,0
    for i in range(h):
        for j in range(w):
            if img[i][j] != 255 :
                ya = i
                if i < yi:
                    yi = i
    for i in range(w):
        for j in range(h):
            if img[j][i] != 255 :
                xa = i
                if i < xi :
                    xi = i
    # print(xi,yi,xa,ya)
    if yi >1 and xi > 1:
        imgcat = img[(yi-2) : (ya+2) ,(xi-2) :(xa +2)]
    elif xi >1:
        imgcat = img[(yi): (ya + 2), (xi - 2):(xa + 2)]
    elif yi >1:
        imgcat = img[(yi-2 ): (ya + 2), xi:(xa + 2)]
    else:
        imgcat = img[yi: (ya + 2), xi:(xa + 2)]

    imgcat = cv2.resize(imgcat ,dsize=(96,96))

    return imgcat


def cat_img():
    path  = 'E:/ksall/'
    save_path = 'E:/ks_test/'


    # img_list = open('D:/Backup/桌面/cat_er.txt').readlines()
    img_list = os.listdir(path)
    # print(img_list);quit()
    n = len(img_list)
    m = 0
    for name in img_list:
        m+=1
        # name = 'xs_933.04_528797.png'
        img = cv2.imread(path+name ,0)
        try:
            imgcat = qiegebiankuang(img)
            cv2.imwrite(save_path + name, imgcat)
            # print('cg');quit()
        except:
            print(name)

        if m %3000 == 0:
            print('完成进度 ：{}%'.format(round(m/n ,2)))

        # h, w = img.shape
        # xi, yi, xa, ya = 0, 0, 0, h
        # for i in range(w):
        #     for j in range(h):
        #         if img[j][i] != 255:
        #             xa = i
        # imgcat = img[yi: ya, xi:xa]
        # imgcat = cv2.resize(imgcat, dsize=(96, 96))




        # cv2.imshow('img' ,img)
        # cv2.imshow('imgcat',imgcat)
        # cv2.waitKey(0)



if __name__== '__main__':
    cat_img()
