import cv2
import class_db
import json
import re
import os
import random
import numpy as np



def overlap_area(x1, y1, x2, y2, x3, y3, x4, y4): #计算两个矩形相交面积
    if (x2 <= x3 or x4 <= x1) and (y2 <= y3 or y4 <= y1):return 0
    lens = min(x2, x4) - max(x1, x3)
    wide = min(y2, y4) - max(y1, y3)
    return lens * wide

def se_info(index,i):
    rea = class_db.selecto(index,i)[0]
    id = rea['id']

    rea = rea['ocr_info']
    rea = json.loads(rea)
    rea = rea['ITRResult']
    qy = []
    lable = []
    # print(rea['recog_result'][0]['line_word_result'])
    try:

        for i in range(len(rea['recog_result'][0]['line_word_result'])):
            info_an = rea['recog_result'][0]['line_word_result'][i]
            info_an =info_an['word_content'][0]
            ss = info_an.split("=")[-1]
            ss0 = re.sub('\s+', '', ss).strip()

            mm = re.findall(r'[0-9]*\.?[0-9]*',ss0)

            if len(mm) == 2:
                lable.append(info_an)
                info = rea['multi_line_info']['imp_line_info'][i]
                zuobiao = info['imp_line_rect']['left_up_point_x'], info['imp_line_rect']['left_up_point_y'], \
                          info['imp_line_rect']['right_down_point_x'], info['imp_line_rect']['right_down_point_y']
                qy.append(zuobiao)
        return [id,qy,lable]
    except:
        return 0

def quyu(cat,ezhi):
    j = cat
    x,y,w,h = ezhi
    s = w * h
    if (x < j[2] and y < j[3] and (x + w) > j[2] and (y + h) > j[3]) and w < (j[2] - j[0]) and h < (j[3] - j[1]):
        sj = overlap_area(j[0], j[1], j[2], j[3], x, y, x + w, y + h)
        if sj / s > 0.8:
            j[2], j[3] = x + w+1, y + h+1
    elif x < j[2] and y < j[1] and x + w > j[2] and y + h > j[1] and w < (j[2] - j[0]) and h < (j[3] - j[1]):
        sj = overlap_area(j[0], j[1], j[2], j[3], x, y, x + w, y + h)
        if sj / s > 0.8:
            j[2], j[1] = x + w+1, y-1
    elif x < j[2] and y < j[1] and x + w > j[2] and y + h > j[3] and w < (j[2] - j[0]) and h > (j[3] - j[1]):
        sj = overlap_area(j[0], j[1], j[2], j[3], x, y, x + w, y + h)
        if sj / s > 0.8:
            j[1], j[2], j[3] = y-1, x + w, y + h+1
    return j

def define_coordinate(list):
    if len(list) <= 2:
        return None
    else:
        s = []
        for i in list:
            s.append(i[2])
        arr = np.array(s)
        rez = arr.argsort()[-3:][::-1]
        x0,x1,x2 = list[rez[0]],list[rez[1]],list[rez[2]]
        L = [x0[0],x1[0],x2[0]]

        a = max(L)
        b = min(L)
        for i in range(len(L)):
            if b< list[rez[i]][0] < a:
                return list[rez[i]]
            elif b< list[rez[i]][0] and a == list[rez[i]][0]:
                return list[rez[i]]

def qiefen(im_path,im_info,im_save_path):

    global sj
    im_path = im_path+str(im_info[0])+'.jpg'
    print(im_path)
    img = cv2.imread(im_path)
    img0 = img
    img2_warped = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    img2_warped_inv = cv2.adaptiveThreshold(img2_warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21,10)  # 自适应二值化ADAPTIVE_THRESH_GAUSSIAN_C
    contours, hierarchy = cv2.findContours(img2_warped_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('img1', img2_warped_inv)  # 显示图片
    # cv2.waitKey(0)

    for m in range(len(im_info[1])):
        j = list(im_info[1][m])
        Y = []
        # L = re.findall(u"[\u4e00-\u9fa5]+", str(im_info[2][m].split('=')[-1]))  #判断标签里面是否有中文
        # if len(L) ==0:
        for i in range(len(contours)):
            ezhi = cv2.boundingRect(contours[i])
            j_cat =quyu(j, ezhi)

        img_cat = img[j_cat[1]:j_cat[3], j_cat[0]:j_cat[2]]
        # cv2.imshow('img2', img_cat)  # 显示图片
        # cv2.waitKey(0)
        img2_warped = cv2.cvtColor(img_cat, cv2.COLOR_BGR2GRAY)
        img2_warped_inv = cv2.adaptiveThreshold(img2_warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 5)  # 自适应二值化

        contours0, hierarchy = cv2.findContours(img2_warped_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # print(len(contours0))
        for i in range(len(contours0)):

            x0, y0, w0, h0 = cv2.boundingRect(contours0[i])
            s = w0*h0
            if w0 > 2*h0 and (j_cat[3] - j_cat[1])*0.25 < y0 < (j_cat[3] - j_cat[1])*0.75:
                # cv2.rectangle(img, (j_cat[0]+x0, j_cat[1]+y0), (j_cat[0]+x0 + w0, j_cat[1]+y0 + h0), (153, 153, 0), 1)
                # cv2.imshow('img3', img)  # 显示图片
                # cv2.waitKey(1000)

                Y.append([x0,w0,s])
        # print(Y)
        zuob = define_coordinate(Y)


        if zuob ==None:
            continue
        else:
            j_cat[0] = j_cat[0] + zuob[0] + zuob[1] + 1  # j_cat[0]+ x0 + w0 +1  更新裁剪区域x0坐标
        yx = (j_cat[2]- j_cat[0])/(j_cat[3]- j_cat[1])
        if yx >1.5 or yx < 0.5  or ((j_cat[2]- j_cat[0])<10 or (j_cat[3]- j_cat[1])< 10 ):
            continue
        else:
            cropped = img[j_cat[1]:j_cat[3],j_cat[0]:j_cat[2]]  # 裁剪坐标为[y0:y1, x0:x1]
            # cv2.rectangle(img, (j_cat[0], j_cat[1] ), (j_cat[2] , j_cat[3]), (53, 53, 0), 1)
            # cv2.imshow('img3', img)  # 显示图片
            # cv2.waitKey(1000)

            ss = im_info[2][m].split("=")[-1]
            # label_path = 'wu_'+im_info[2][i] +'_.jpg'

            label_path = 'wu_' + str(ss) + '_'+str(im_info[0]) +'_'+str(random.randint(1,100000))+'.jpg'
            im_save_path0 = im_save_path + str(ss)+'/'

            if not os.path.exists(im_save_path0):
                os.makedirs(im_save_path0)
               # print(im_save_path0)
            im_save_path1 = im_save_path0 + label_path
            cv2.imwrite(im_save_path1, cropped)



    # cv2.rectangle(img, (j_cat[0], j_cat[1] ), (j_cat[2] , j_cat[3]), (53, 53, 0), 1)
    # cv2.imshow('img2', img)  # 显示图片
    # cv2.waitKey(0)



if __name__ == '__main__':
    # im_info =se_info(4, 1)
    im_path = 'E:/BaiduNetdiskDownload/num_orgiamge/'
    im_save_path = 'E:/BaiduNetdiskDownload/wu14CC/qiege/'

    for i in range(5000,5010):
        im_info = se_info(i, 1)
        # print(im_info)
        if im_info != 0 and len(im_info[2]) > 5:
            # print(im_info)
            try:
                qiefen(im_path, im_info, im_save_path)
            except:
                pass














