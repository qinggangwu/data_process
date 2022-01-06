import cv2
import os
import random

def erzhihuatuxiang():
    path = 'D:/data/CASIA/train_num/00028/'
    imglist = os.listdir(path)

    sava_path = "D:/train_data/wu14CC/erzhihua/original/00028/"
    if not os.path.exists(sava_path):
        os.makedirs(sava_path)

    for name in imglist:
        img = cv2.imread(path+name,0)
        # cv2.imshow('test',img)
        # cv2.waitKey(300)
        ret, binary = cv2.threshold(img, 50, 255, cv2.THRESH_OTSU)
        img_ada_mean=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7,19)
        #膨胀
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 定义结构元素的形状和大小
        # dst = cv2.dilate(binary, kernel)
        cv2.imwrite(sava_path+name,binary)
        # cv2.imshow('test',binary)
        # cv2.waitKey(500)


def make_infotxt():
    path = 'D:/train_data/wu14CC/erzhihua/nu/'
    img_list = os.listdir(path)

    yuliao = []
    for name in img_list:
        label = name.split("_")[1]
        n=random.randint(1,1000000)
        if n%29 == 0:
            label = '-'+label
        yuliao.append(label + '\n')

    yuliao = list(set(yuliao))
    fyuliao = open('D:/train_data/wu14CC/erzhihua/nuinfo.txt','w')
    fyuliao.writelines(sorted(yuliao))
    fyuliao.close()


def make_yuliao_infotxt():
    path = 'D:/train_data/wu14CC/yn/'
    img_list = os.listdir(path)

    yuliao = []
    for name in img_list:
        label = name.split("_")[1]
        # n=random.randint(1,1000000)
        # if n%29 == 0:
        #     label = '-'+label
        yuliao.append(name+'\t'+label + '\n')

    yuliao = list(set(yuliao))
    fyuliao = open('D:/train_data/wu14CC/erzhihua/nuyuliao.txt','w')
    fyuliao.writelines(sorted(yuliao))
    fyuliao.close()

if __name__ == "__main__":
    erzhihuatuxiang()
    # pass