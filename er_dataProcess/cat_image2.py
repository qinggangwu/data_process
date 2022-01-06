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

def se_info(index):
    rea = index
    qy = []
    lable = []
    # print(rea['recog_result'][0]['line_word_result'])
    try:
        id = rea['id']
        rea = rea['ocr_info']
        rea = json.loads(rea)
        rea = rea['ITRResult']
        for i in range(len(rea['recog_result'][0]['line_word_result'])):
            info_an = rea['recog_result'][0]['line_word_result'][i]
            info_an =info_an['word_content'][0]
            ss = info_an.split("=")[-1]
            # print(ss)
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

def sefs_info(index):
    rea = index
    qy = []
    lable = []
    # print(rea['recog_result'][0]['line_word_result'])
    try:
        id = rea['id']
        rea = rea['ocr_info']
        rea = json.loads(rea)
        rea = rea['ITRResult']
        for i in range(len(rea['recog_result'][0]['line_word_result'])):
            info_an = rea['recog_result'][0]['line_word_result'][i]
            info_an =info_an['word_content'][0]
            ss = info_an.split("=")[-1]
            if  'frac' in ss :

            # print(ss)
            # ss0 = re.sub('\s+', '', ss).strip()
            #
            # mm = re.findall(r'[0-9]*\.?[0-9]*',ss0)
            #
            # if len(mm) == 2:
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
        # rez = arr.argsort()[-3:][::-1]
        print(arr)
        rez = arr.argsort()[-5:][::-1]

        print(rez)
        x0,x1,x2 = list[rez[0]],list[rez[1]],list[rez[2]]
        L = [x0[0],x1[0],x2[0]]

        a = max(L)
        b = min(L)
        for i in range(len(L)):
            if b< list[rez[i]][0] < a:
                return list[rez[i]]
            elif b< list[rez[i]][0] and a == list[rez[i]][0]:
                return list[rez[i]]


def definefs_coordinate(list):
    if  len(list) <2:
        return None
    for i in range(len(list)-1):
        for j in list[i+1:]:
            a = abs(list[i][0] -j[0])
            b = abs(list[i][2] -j[2])
            c = abs(list[i][3] -j[3])
            s = abs(list[i][4] -j[4])

            if a<3 and b<3 and c<3 and s<10:
                return list[i]
    return None


    # list = sorted(list,key=lambda s:s[4],reverse=True)
    #
    # for i in list:
    #     n = 0
    #     for j in list2:
    #         cen = j[0]+0.5*j[2]
    #         if i[0] <cen < (i[0]+i[2]):
    #             n+=1
    #     if n<=1:
    #         return i
    # return None

def zuobiao_intersect(x0,list):
    # f = True
    for i in list:
        if x0> i[0] and x0<(i[0]+i[1]):
            return True
    return False


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
        Y0=[]
        # L = re.findall(u"[\u4e00-\u9fa5]+", str(im_info[2][m].split('=')[-1]))  #判断标签里面是否有中文
        # if len(L) ==0:
        for i in range(len(contours)):
            ezhi = cv2.boundingRect(contours[i])
            j_cat =quyu(j, ezhi)

        img_cat = img[j_cat[1]:j_cat[3], j_cat[0]:j_cat[2]]

        # src_image = cv2.imread('img1.jpg')
        # 读取图片转换为为灰度图像
        # image_gray = cv2.cvtColor(img_cat, cv2.COLOR_BGR2GRAY)
        # 边缘检测之前先进行滤波，降噪，滤波方式为高斯滤波
        # filter_image = cv2.GaussianBlur(image_gray, (5, 5), 0)
        # # 调用canny算子，进行边缘检测 48,170是一个调整范围，根据实际情况选用
        # canny_image = cv2.Canny(filter_image, 48, 70)  # 48是最小阈值,170是最大阈值
        # cv2.imshow('img2', img_cat)  # 显示图片
        # cv2.waitKey(1000)
        img2_warped = cv2.cvtColor(img_cat, cv2.COLOR_BGR2GRAY)
        img2_warped_inv = cv2.adaptiveThreshold(img2_warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21,10)  # 自适应二值化

        contours0, hierarchy = cv2.findContours(img2_warped_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours0)):
            x0, y0, w0, h0 = cv2.boundingRect(contours0[i])
            s = w0*h0
            if w0 > 2*h0 and (j_cat[3] - j_cat[1])*0.25 < y0 < (j_cat[3] - j_cat[1])*0.75:
                Y.append([x0, y0, w0, h0,s])
                # cv2.rectangle(img, (j_cat[0] + x0, j_cat[1] + y0), (j_cat[0] + x0 + w0, j_cat[1] + y0 + h0), (153, 153, 0), 1)
                # cv2.rectangle(img_cat, ( x0,  y0), (x0 + w0,  y0 + h0), (253, 253, 0), 1)
                # cv2.imshow('img4', img_cat)  # 显示图片
                # cv2.waitKey(0)
        # print(Y)
            # else:
            #     Y0.append([x0, y0, w0, h0,s])

        #
        # contours1, hierarchy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # for ii in range(len(contours1)):
        #     x1, y1, w1, h1 = cv2.boundingRect(contours1[ii])
        #     if h1>10 :
        #         Y0.append([x1, w1, h1])
                # cv2.rectangle(img, (j_cat[0] + x1, j_cat[1] + y1), (j_cat[0] + x1 + w1, j_cat[1] + y1 + h1), (153, 153, 0), 1)
                # cv2.imshow('img4', img)  # 显示图片
                # cv2.waitKey(100)

        zuob = definefs_coordinate(Y)
        # print(zuob)

        if zuob ==None:
            continue
        else:
            # print(zuob ,j_cat)
            j_cat[0] = j_cat[0] + zuob[0] + int(zuob[2]) + 1  # j_cat[0]+ x0 + w0 +1  更新裁剪区域x0坐标

        yx = (j_cat[2]- j_cat[0])/(j_cat[3]- j_cat[1])   # yx是切割图片的w/h
        ss = im_info[2][m].split("=")[-1].replace('\\frac','')
        # print(ss)
        ss = ss.replace('} {','-')

        if yx < 0.3 or ((j_cat[2]- j_cat[0])<10 or (j_cat[3]- j_cat[1])< 10 ) :

            continue
        else:
            cropped = img[j_cat[1]:j_cat[3],j_cat[0]:j_cat[2]]  # 裁剪坐标为[y0:y1, x0:x1]


            # cv2.rectangle(img, (j_cat[0], j_cat[1] ), (j_cat[2] , j_cat[3]), (53, 53, 0), 1)
            # cv2.imshow('qffs', img)  # 显示图片
            # cv2.waitKey(1000)

            # ss = im_info[2][m].split("=")[-1]
            # label_path = 'wu_'+im_info[2][i] +'_.jpg'

            label_path = 'wu_' + str(ss) + '_'+str(im_info[0]) +'_'+str(random.randint(1,1000))+'.jpg'
            label_path = ''.join(label_path.split(" "))
            # im_save_path0 = im_save_path + str(ss)+'/'
            # im_save_path0 = ''.join(im_save_path0.split(" "))
            #
            if not os.path.exists(im_save_path):
                os.makedirs(im_save_path)
            im_save_path1 = os.path.join(im_save_path , label_path)
            cv2.imwrite(im_save_path1, cropped)
            # print('已经成功保存{}图片'.format(label_path))



    # cv2.rectangle(img, (j_cat[0], j_cat[1] ), (j_cat[2] , j_cat[3]), (53, 53, 0), 1)
    # cv2.imshow('img2', img)  # 显示图片
    # cv2.waitKey(0)



if __name__ == '__main__':
    # im_info =se_info(4, 1)

    im_path = 'E:/BaiduNetdiskDownload/fs_orgiamge/'
    # im_save_path = 'E:/BaiduNetdiskDownload/wu14CC/qiegefs/2'

    # db1=class_db.db()
    # re = db1.select('select id,image,ocr_info from a_kousuan_pigai limit {},{}'.format(2, 1))
    for x in range(1,16):
        rea = class_db.selectofs(x)
        im_save_path = 'E:/BaiduNetdiskDownload/wu14CC/qiegefs/{}'.format(x)
        for i in rea:
            im_info = sefs_info(i)
            if im_info != 0 and len(im_info[2]) > 5:
                # print(im_info)
                try:
                    qiefen(im_path, im_info, im_save_path)
                except:
                    pass














