import random
import os
import cv2
import numpy as np
import shutil
import imutils
from multiprocessing.dummy import Pool

# def zhengshu_pj(num:int,img_list):
#     for i in range(num):
#         # pass
#         path1 = random.choice(img_list)
#         path2 = random.choice(img_list)
#         path3 = random.choice(img_list)
#         label = path1.split('_')[2] + path2.split('_')[2] +path3.split('_')[2]
#         img1 = cv2.imread(path1,0)
#         w1,h1 = img1.shape
#         print(label)
#         img2 = cv2.imread(path2,0)
#         img2 = cv2.resize(img2,dsize=(h1, w1))
#         img3 = cv2.imread(path3,0)
#         img3 = cv2.resize(img3,dsize=(h1, w1))
#
#         img_out = np.concatenate((img1, img2), axis=1)
#         img_out = np.concatenate((img_out, img3), axis=1)
#
#         cv2.imwrite('D:/train_data/wu14CC/erzhihua/make_nu/thr_nu/nu3_{}_{}.png'.format(label,random.randint(1,999999)),img_out)
#         # cv2.imshow('test',img_out)
#         # cv2.waitKey(0)

def img_List():
    path = "D:/train_data/wu14CC/erzhihua/original/"
    file_list = os.listdir(path)
    img_list = []
    for file in file_list:
        if len(file) == 1 and file not in  ['-' ,'=','^']:
            imgname_list = os.listdir(os.path.join(path , file))
            for img in imgname_list:
                img_list.append(os.path.join(path , file, img))
            # print(file)
    return img_list

def zhengshu_pj(num:int,img_list):
    for i in range(num):
        h = 96
        w = 600
        imgDi = np.ones((h,w))*255
        j = random.randint(2, 6)
        path = []
        for n in range(j):
            path.append(random.choice(img_list))
        w0 = random.randint(2, 20)
        label = ''
        try:
            for name in path:
                la = name.split('_')[2]
                label +=la
                img = cv2.imread(name, 0)
                img = xuanzhuan_nu(img)
                img = qiegebiankuang_ro(img)

                ht, wt = img.shape
                global_y0 = (h - ht) // 2 + random.randint(-5,5)
                global_x0 = w0
                imgDi[global_y0:ht + global_y0, global_x0:wt + global_x0] = img
                w0 = global_x0 + wt + random.randint(-1, 30)
            cv2.imwrite('D:/train_data/wu14CC/erzhihua/make_over2/nu/nu{}_{}_{}.png'.format(j,label, random.randint(1, 999999)), qiegebiankuangfs(imgDi))
            print(label)
        except:
            pass

def add_alpha_channel(img):
    """ 为jpg图像添加alpha通道 """

    b_channel, g_channel, r_channel = cv2.split(img)  # 剥离jpg图像通道
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道

    img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))  # 融合通道
    return img_new

def merge_img(jpg_img, png_img, y1, y2, x1, x2):
    """ 将png透明图像与jpg图像叠加
        y1,y2,x1,x2为叠加位置坐标值
    """

    # 判断jpg图像是否已经为4通道
    if jpg_img.shape[2] == 3:
        jpg_img = add_alpha_channel(jpg_img)

    '''
    当叠加图像时，可能因为叠加位置设置不当，导致png图像的边界超过背景jpg图像，而程序报错
    这里设定一系列叠加位置的限制，可以满足png图像超出jpg图像范围时，依然可以正常叠加
    '''
    yy1 = 0
    yy2 = png_img.shape[0]
    xx1 = 0
    xx2 = png_img.shape[1]

    if x1 < 0:
        xx1 = -x1
        x1 = 0
    if y1 < 0:
        yy1 = - y1
        y1 = 0
    if x2 > jpg_img.shape[1]:
        xx2 = png_img.shape[1] - (x2 - jpg_img.shape[1])
        x2 = jpg_img.shape[1]
    if y2 > jpg_img.shape[0]:
        yy2 = png_img.shape[0] - (y2 - jpg_img.shape[0])
        y2 = jpg_img.shape[0]

    # 获取要覆盖图像的alpha值，将像素值除以255，使值保持在0-1之间
    alpha_png = png_img[yy1:yy2, xx1:xx2, 3] / 255.0
    alpha_jpg = 1 - alpha_png

    # 开始叠加
    for c in range(0, 3):
        # jpg_img[y1:y2, x1:x2, c] = ((alpha_jpg * jpg_img[y1:y2, x1:x2, c]) + (alpha_png * png_img[yy1:yy2, xx1:xx2, c]))
        jpg_img[y1:y2, x1:x2, c] = ((alpha_png * jpg_img[y1:y2, x1:x2, c]) + (alpha_jpg * png_img[yy1:yy2, xx1:xx2, c]))

    return jpg_img

def zhengshu_pj_RGBA(num:int,img_list):
    for i in range(num):
        h = 200
        w = 300
        imgDi = np.ones((h,w))*255
        imgDi =cv2.merge((imgDi,imgDi,imgDi,imgDi))
        # print(imgDi.shape)
        #
        # cv2.imshow('imgDi', imgDi)
        # cv2.waitKey(0)
        j = random.randint(2, 4)
        path = []
        for n in range(j):
            path.append(random.choice(img_list))
        w0 = random.randint(0, 20)
        label = ''
        tela = ''

        try:
            for name in path:
                la = name.split('_')[2]
                label +=la
                tela += name[41:] + '\t'
                img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
                img = cv2.merge((img,img,img,img))

                ht, wt,_ = img.shape
                global_y0 = (h - ht) // 2
                global_x0 = w0
                imgDi = merge_img( imgDi,  img, global_y0, (ht + global_y0), global_x0, (wt + global_x0))

                w0 = global_x0 + wt + random.randint(-5, 0)
            save_path ='D:/train_data/wu14CC/erzhihua/make_nu/nu_RGBA/nu{}_{}_{}.png'.format(j,label, random.randint(1, 999999))
            cv2.imwrite(save_path, cv2.resize(qiegebiankuang(imgDi),dsize=(104,64)) )
            print(save_path[46:],'\t',tela)
        except:
            pass

# def dange_zhengshu_pj(n,img_list ,boolro = True,ro =15):
def dange_zhengshu_pj(img_list  ,n =1,boolro = True,ro =15):
    h = 200
    w = 300
    imgDi = np.ones((h,w))*255
    # j = random.randint(1, n)
    path = []
    for i in range(n):
        path.append(random.choice(img_list))
    # w0 = random.randint(0, 20)
    # path = [img_list]   # 单个多线程
    w0 = random.randint(20, 30)
    label = ''
    try:
        for name in path:
            la = name.split('_')[2]
            label +=la
            img = cv2.imread(name, 0)
            if boolro:
                img = xuanzhuan_nu(img, ro)
                img = qiegebiankuang_ro(img)
            ht, wt = img.shape
            global_y0 = (h - ht) // 2  +random.randint(-5,5)
            global_x0 = w0
            imgDi[global_y0:ht + global_y0, global_x0:wt + global_x0] = img
            # w0 = global_x0 + wt + random.randint(60, 100)
            w0 = global_x0 + wt + random.randint(-1, 15)
        # cv2.imshow('t',imgDi)
        # cv2.waitKey(0)
        # cv2.imwrite('D:/train_data/wu14CC/erzhihua/make_over2/test/wu_{}_{}.png'.format(label, random.randint(1, 999999)),qiegebiankuangfs(imgDi))
        # print(label)
        return imgDi ,label
    except:
        pass
def fushu_pj(num:int,img_list ,fs_list):
    for i in range(num):
        h = 96
        w = 200
        imgDi = np.ones((h,w))*255

        j = random.randint(1,3)
        path  = []
        for n in range(j):
            path.append(random.choice(img_list))
        label = ''.join([x.split('_')[2] for x in path])

        fs_path = random.choice(fs_list)
        fs_img = cv2.imread(fs_path,0)
        hf, wf = fs_img.shape
        global_y0 = (h - hf) // 2
        global_x0 = random.randint(0, 20)
        imgDi[global_y0:hf + global_y0, global_x0:wf + global_x0] = fs_img

        w0 = global_x0 +wf +random.randint(0,5)
        label = fs_path.split('_')[2] +label
        try:
            for name in path:
                img = cv2.imread(name, 0)
                ht, wt = img.shape
                global_y0 = (h - ht) // 2
                global_x0 = w0
                imgDi[global_y0:ht + global_y0, global_x0:wt + global_x0] = img
                w0 = global_x0 +wt + random.randint(0,15)
            cv2.imwrite('D:/train_data/wu14CC/erzhihua/make_nu/fus/fnu/fnu_{}_{}.png'.format(label, random.randint(1, 999999)),  cv2.resize(qiegebiankuang(imgDi),dsize=(104,64)))
            print(label)
        except:
            pass
def fushu_xiaoshu_pj(num:int,img_list ,fs_list,dian_list):
    for i in range(num):
        h = 96
        w = 200
        imgDi = np.ones((h,w))*255
        j = random.randint(2,3)
        path  = []
        for n in range(j):
            path.append(random.choice(img_list))

        path.append(random.choice(dian_list))
        random.shuffle(path)


        fh_path = random.choice(fs_list)
        fs_img = cv2.imread(fh_path,0)
        hf, wf = fs_img.shape
        global_y0 = (h - hf) // 2
        global_x0 = random.randint(0, 20)
        imgDi[global_y0:hf + global_y0, global_x0:wf + global_x0] = fs_img

        w0 = global_x0 +wf +random.randint(0,15)
        label = fh_path.split('_')[2]
        n = len(path)-1

        if '.' == path[0].split("_")[2] or '.' == path[n].split("_")[2]:
            continue
        try:
            for name in path:
                la = name.split("_")[2]
                if la == '.':
                    img = cv2.imread(name, 0)
                    ht, wt = img.shape
                    global_y0 = h0 -wt -random.randint(2,20)
                    global_x0 = w0
                    imgDi[global_y0:ht + global_y0, global_x0:wt + global_x0] = img
                    w0 = global_x0 + wt + random.randint(0, 5)
                else:
                    img = cv2.imread(name, 0)
                    ht, wt = img.shape
                    global_y0 = (h - ht) // 2
                    global_x0 = w0
                    imgDi[global_y0:ht + global_y0, global_x0:wt + global_x0] = img
                    w0 = global_x0 +wt + random.randint(0,15)
                    h0 = global_y0 + ht
                label += la
            imgDi = cv2.resize(qiegebiankuang(imgDi),dsize=(104,64))
            # cv2.imshow('test',imgDi)
            # cv2.waitKey(0)
            cv2.imwrite('D:/train_data/wu14CC/erzhihua/make_nu/fus/fxs/fxs_{}_{}.png'.format(label, random.randint(100000, 999999)),  imgDi)
            print(label)
        except:
            pass
def xiaoshu_pj(num:int,img_list ,dian_list):
    for i in range(num):
        h = 96
        w = 600
        imgDi = np.ones((h,w))*255
        j = random.randint(2,5)
        path  = []
        for n in range(j):
            path.append(random.choice(img_list))

        path.append(random.choice(dian_list))
        random.shuffle(path)


        w0 = random.randint(2,20)
        label = ''
        n = len(path)-1

        if '.' == path[0].split("_")[2] or '.' == path[n].split("_")[2]:
            continue
        try:
            for name in path:
                la = name.split("_")[2]
                if la == '.':
                    img = cv2.imread(name, 0)
                    ht, wt = img.shape
                    global_y0 = h0 -wt -random.randint(2,20)
                    global_x0 = w0
                    imgDi[global_y0:ht + global_y0, global_x0:wt + global_x0] = img
                    w0 = global_x0 + wt + random.randint(0, 15)
                else:
                    img = cv2.imread(name, 0)
                    ht, wt = img.shape
                    global_y0 = (h - ht) // 2   + random.randint(-10,10)
                    global_x0 = w0
                    imgDi[global_y0:ht + global_y0, global_x0:wt + global_x0] = img
                    w0 = global_x0 +wt + random.randint(-1,15)
                    h0 = global_y0 + ht
                label += la
            imgDi = qiegebiankuangfs(imgDi)
            # cv2.imshow('test',imgDi)
            # cv2.waitKey(0)
            cv2.imwrite('D:/train_data/wu14CC/erzhihua/make_over2/xs/xs_{}_{}.png'.format(label, random.randint(100000, 999999)),  imgDi)
            print(label)
        except:
            pass
def qiegebiankuangfs(img ):   # 留2个像素
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

    # imgcat = img[yi : ya ,xi :xa]
    imgcat = img[yi-random.randint(0,2) : ya+random.randint(0,2) ,xi-random.randint(1,5) :xa+random.randint(1,5)]
    # cv2.imshow('t', imgcat)
    # cv2.waitKey(0)
    return imgcat
def qiegebiankuang(img):
    h,w,_ = img.shape
    # h,w = img.shape
    xi,yi,xa,ya = w,h,0,0
    for i in range(h):
        for j in range(w):
            if img[i][j][0] != 255 :
                ya = i
                if i < yi:
                    yi = i
    for i in range(w):
        for j in range(h):
            if img[j][i][0] != 255 :
                xa = i
                if i < xi :
                    xi = i
    print(xi, yi, xa, ya)
    if yi >1 and xi > 1:
        imgcat = img[(yi-2) : (ya+2) ,(xi-2) :(xa +2)]
    elif xi >1:
        imgcat = img[(yi): (ya + 2), (xi - 2):(xa + 2)]
    elif yi >1:
        imgcat = img[(yi-2 ): (ya + 2), xi:(xa + 2)]
    else:
        imgcat = img[yi: (ya + 2), xi:(xa + 2)]

    # print(xi,yi,xa,ya)
    # imgcat = img[yi : ya ,xi :xa]

    return imgcat
    # cv2.imshow( 't' ,imgcat)
    # cv2.waitKey(0)
def qiegebiankuang_ro(img):   # 不留边框
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
    # print(xi, yi, xa, ya)
    if yi >1 and xi > 1:
        imgcat = img[(yi-2) : (ya+2) ,(xi-2) :(xa +2)]
    elif xi >1:
        imgcat = img[(yi): (ya + 2), (xi - 2):(xa + 2)]
    elif yi >1:
        imgcat = img[(yi-2 ): (ya + 2), xi:(xa + 2)]
    else:
        imgcat = img[yi: (ya + 2), xi:(xa + 2)]

    # print(xi,yi,xa,ya)
    # imgcat = img[yi : ya ,xi :xa]

    return imgcat
    # cv2.imshow( 't' ,imgcat)
    # cv2.waitKey(0)
def fengshu_pj(num:int,img_list,henxian_list):
    for i in range(num):
        h = 400
        w = 400
        imgDi = np.ones((h, w)) * 255
        hen_path = random.choice(henxian_list)
        try:
            m = random.randint(1,2)
            imgfz, lafz = dange_zhengshu_pj( img_list,m,True,15)
            # imgfz = xuanzhuan_nu(imgfz, 30)
            imgfz = cv2.resize(qiegebiankuang_ro(imgfz), dsize=None, fy=0.6, fx=0.6)
            n = random.randint(1, 2)
            imgfm, lafm = dange_zhengshu_pj( img_list,n,True,10)
            # imgfm = xuanzhuan_nu(imgfm, 15)
            imgfm = cv2.resize(qiegebiankuang_ro(imgfm), dsize=None, fy=0.6, fx=0.6)
            label = '{' + '{}#{}'.format(lafz, lafm) + '}'

            imghx = cv2.imread(hen_path, 0)
            imghx = cv2.resize(imghx,dsize=None ,fy=0.6,fx=1)
            hhx, whx = imghx.shape
            global_y0 = (h - hhx) // 2
            global_x0 = random.randint(5, 20)
            imgDi[global_y0:hhx + global_y0, global_x0:whx + global_x0] = imghx

            hfz, wfz = imgfz.shape
            global_yfz = global_y0 - hfz
            global_xfz = global_x0 + whx//2 - wfz//2 + random.randint(-20,20)
            imgDi[global_yfz:hfz + global_yfz, global_xfz:wfz + global_xfz] = imgfz

            hfm, wfm = imgfm.shape
            global_yfm = global_y0 +hhx
            global_xfm = global_x0 + whx//2 - wfm//2 + random.randint(-20,20)
            imgDi[global_yfm:hfm + global_yfm, global_xfm:wfm + global_xfm] = imgfm
            cv2.imwrite(
                'D:/train_data/wu14CC/erzhihua/make_over2/fs/fs_{}_{}.png'.format(label, random.randint(100000, 999999)), qiegebiankuang_ro(imgDi))
            print(label)
        except:
            pass
    # cv2.imshow('t', imgDi)
    # cv2.waitKey(0)
    # print( imgfz.shape,imgfm.shape,la)
    # pass
def jiafengshu_pj(img_list):
    hen_list = [name for name in img_list if '-50' in name]
    nu_list = [name for name in img_list if not ( '-50' in name) ]

    for i in range(10000):
        h = 400
        w = 400
        imgDi = np.ones((h, w)) * 255

        hen_path = random.choice(hen_list)
        try:
            # 整数
            zs_path = random.choice(nu_list)
            zs = zs_path.split('_')[2]
            # label += la
            imgzs = cv2.imread(zs_path, 0)
            imgzs = cv2.resize(imgzs, dsize=None, fy=0.6, fx=0.6)
            hzs, wzs = imgzs.shape
            global_y0 = (h - hzs) // 2
            global_xzs = random.randint(5,20)
            imgDi[global_y0:hzs + global_y0, global_xzs:wzs + global_xzs] = imgzs
            w0 = global_xzs + wzs + random.randint(1, 5)



            m = random.randint(1,2)
            imgfz, lafz = dange_zhengshu_pj(m, nu_list,True,30)
            imgfz = cv2.resize(qiegebiankuang_ro(imgfz), dsize=None, fy=0.6, fx=0.6)
            n = random.randint(1, 3)
            imgfm, lafm = dange_zhengshu_pj(m, nu_list,True,15)
            imgfm = cv2.resize(qiegebiankuang_ro(imgfm), dsize=None, fy=0.6, fx=0.6)
            label = zs+'{' + '{}#{}'.format(lafz, lafm) + '}'

            imghx = cv2.imread(hen_path, 0)
            imghx = cv2.resize(imghx,dsize=None ,fy=0.6,fx=1.2)
            hhx, whx = imghx.shape
            global_y0 = (h - hhx) // 2
            # global_x0 = random.randint(5, 20)
            global_x0 = w0
            imgDi[global_y0:hhx + global_y0, global_x0:whx + global_x0] = imghx

            hfz, wfz = imgfz.shape
            global_yfz = global_y0 - hfz
            global_xfz = global_x0 + whx//2 - wfz//2+ random.randint(-10,10)
            imgDi[global_yfz:hfz + global_yfz, global_xfz:wfz + global_xfz] = imgfz

            hfm, wfm = imgfm.shape
            global_yfm = global_y0 +hhx
            global_xfm = global_x0 + whx//2 - wfm//2+ random.randint(-10,10)
            imgDi[global_yfm:hfm + global_yfm, global_xfm:wfm + global_xfm] = imgfm
            cv2.imwrite(
                'D:/train_data/wu14CC/erzhihua/make_over/test/jfs_{}_{}.png'.format(label, random.randint(100000, 999999)),
                qiegebiankuangfs(imgDi))
            print(label)
        except:
            pass
    # cv2.imshow('t', imgDi)
    # cv2.waitKey(0)
    # print( imgfz.shape,imgfm.shape,la)
    # pass

# 旋转符号：
def xuanzhuan_fh(fh_list ,num = 1):

    for i in range(num):
        h = 300
        w = 300
        imgDi = np.ones((h, w)) * 255
        # fh_path = random.choice(fh_list)
        fh = fh_list.split('_')[2]

        imgfh = cv2.imread(fh_list, 0)
        hfh, wfh = imgfh.shape
        global_yfh = (h - hfh) // 2
        global_xfh = (w - wfh) // 2
        imgDi[global_yfh:hfh + global_yfh, global_xfh:wfh + global_xfh] = imgfh


        # ro = random.randint(-15,30)
        # rotated = imutils.rotate(imgDi, ro)
        # cv2.imshow('test', rotated)
        # cv2.waitKey(500)

        # if ro <0 :
        #     cat_img = rotated[0:150 , 30 :100]
        # else:
        #     cat_img = rotated[60:200 , 30 :100]

        # cat_img = rotated[110:190, 110:190]
        cat_img = qiegebiankuangfs(imgDi)
        # save_img = cv2.resize(cat_img,dsize=(104,64))
        # cv2.imwrite(
        #     'D:/train_data/wu14CC/erzhihua/make_nu/fuhao/wu_{}_{}.png'.format(fh, random.randint(100000, 999999)),
        #     save_img)
        cv2.imwrite(  'D:/train_data/wu14CC/erzhihua/make_over/fh/fh_{}_{}.png'.format(fh, random.randint(100000, 999999)),       cat_img)
        # print('正在保存图片 {}'.format(fh))



        # cv2.imshow('test2',save_img)
        # cv2.waitKey(0)
        # print(fh,ro);quit()
def xuanzhuan_nu(img,rod =15):

    # for i in range(num):
    h = 400
    w = 400
    imgDi = np.ones((h, w)) * 255
    # fh_path = random.choice(fh_list)
    # fh = fh_path.split('_')[2]
    #
    # imgfh = cv2.imread(fh_path, 0)
    hfh, wfh = img.shape
    global_yfh = (h - hfh) // 2
    global_xfh = (w - wfh) // 2
    imgDi[global_yfh:hfh + global_yfh, global_xfh:wfh + global_xfh] = img

    ro = random.randint(-rod,rod)
    rotated = imutils.rotate(imgDi, ro)

    cat_img = rotated[160:260, 160:260]

    # cat_img = qiegebiankuangfs(cat_img)
    # save_img = cv2.resize(cat_img,dsize=(104,64))


    return cat_img


        # cv2.imshow('test2',save_img)
        # cv2.waitKey(0)
        # print(fh,ro);quit()


def find_erimg():
    txt_info = open('D:/train_data/wu14CC/erzhihua/make_nu/RGBA_make.txt').readlines()
    # img_list = os.listdir('D:/train_data/wu14CC/erzhihua/make_nu/er/q/')
    re_list =[]
    h_list = ['wu_1_2363762.png', 'wu_3_20171.png', 'wu_3_2545302.png', 'wu_7_1902953.png', 'wu_7_1754351.png', 'wu_8_3336856.png', 'wu_8_1562623.png', 'wu_8_2054769.png', 'wu_9_1711358.png', 'wu_9_2211265.png', 'wu_3_2545302.png', 'wu_7_1902953.png', 'wu_8_3107895.png', 'wu_8_2687875.png', 'wu_8_1648737.png', 'wu_8_2101630.png', 'wu_8_2906875.png', 'wu_9_2320734.png', 'wu_9_2320734.png', 'wu_8_2160389.png', 'wu_8_1902954.png', 'wu_8_1180635.png', 'wu_8_2054769.png', 'wu_8_1816987.png', 'wu_1_2614868.png', 'wu_6_1676148.png', 'wu_7_2336321.png', 'wu_8_1707452.png', 'wu_8_2520918.png', 'wu_8_2371593.png', 'wu_9_1711358.png', 'wu_9_2168235.png', 'wu_9_1723090.png', 'wu_9_2101631.png', 'wu_9_1711358.png', 'wu_9_1180636.png', 'wu_9_1816988.png', 'wu_1_3399444.png', 'wu_3_2534850.png', 'wu_3_2545302.png', 'wu_6_1707450.png', 'wu_7_1385160.png', 'wu_8_2101630.png', 'wu_8_68387.png', 'wu_8_2687875.png', 'wu_8_2371593.png', 'wu_9_2520919.png', 'wu_9_1899052.png', 'wu_9_1711358.png', 'wu_1_1503935.png', 'wu_1_1503935.png', 'wu_3_20171.png', 'wu_7_1902953.png', 'wu_8_2774560.png', 'wu_9_1813080.png', 'wu_9_2211265.png', 'wu_9_1899052.png', 'wu_9_2211265.png', 'wu_9_2211265.png', 'wu_3_2534850.png', 'wu_7_1754351.png', 'wu_7_1754351.png', 'wu_7_2434131.png', 'wu_8_1156597.png', 'wu_8_2449819.png', 'wu_8_3080067.png', 'wu_8_1515714.png', 'wu_8_1180635.png', 'wu_8_1816987.png', 'wu_8_3013934.png', 'wu_6_88363.png', 'wu_7_1777866.png', 'wu_9_433778.png', 'wu_9_68388.png', 'wu_3_1699625.png', 'wu_9_3257168.png', 'wu_9_1156598.png', 'wu_9_2265928.png', 'wu_9_414775.png', 'wu_9_433778.png', 'wu_9_1707453.png', 'wu_9_2211265.png', 'wu_0_128447.png', 'wu_1_3166715.png', 'wu_1_2363762.png', 'wu_3_1699625.png', 'wu_8_402718.png', 'wu_8_2039127.png']
    q_list = ['wu_2_1648731.png', 'wu_5_2722583.png', 'wu_8_72507.png', 'wu_1_2097701.png', 'wu_6_2573156.png', 'wu_6_1734798.png', 'wu_7_237062.png', 'wu_7_1317140.png', 'wu_2_274783.png', 'wu_2_1361317.png', 'wu_5_196839.png', 'wu_5_1875631.png', 'wu_7_2238616.png', 'wu_8_2426318.png', 'wu_1_331020.png', 'wu_2_3121783.png', 'wu_8_158159.png', 'wu_8_410753.png', 'wu_0_158151.png', 'wu_0_1789601.png', 'wu_0_2882478.png', 'wu_1_2269824.png', 'wu_1_1353276.png', 'wu_1_2238610.png', 'wu_1_1196725.png', 'wu_1_434845.png', 'wu_1_1397255.png', 'wu_2_1236956.png', 'wu_2_2527881.png', 'wu_2_16100.png', 'wu_2_3069635.png', 'wu_3_1617437.png', 'wu_3_2281583.png', 'wu_3_2461476.png', 'wu_3_194359.png', 'wu_3_56307.png', 'wu_3_2833750.png', 'wu_3_3333376.png', 'wu_5_310927.png', 'wu_5_1906877.png', 'wu_6_3045259.png', 'wu_6_154126.png', 'wu_7_1365339.png', 'wu_7_2760604.png', 'wu_7_32273.png', 'wu_7_417696.png', 'wu_7_2402891.png', 'wu_7_1329217.png', 'wu_7_1184659.png', 'wu_0_3038293.png', 'wu_0_3121781.png', 'wu_0_1421121.png', 'wu_1_2788498.png', 'wu_1_2733000.png', 'wu_2_182324.png', 'wu_2_3385533.png', 'wu_2_2708701.png', 'wu_3_128450.png', 'wu_3_16101.png', 'wu_3_3160025.png', 'wu_3_1945977.png', 'wu_5_2109460.png', 'wu_6_237061.png', 'wu_6_85788.png', 'wu_7_3013933.png', 'wu_7_1035976.png', 'wu_7_32153.png', 'wu_7_64438.png', 'wu_8_1000022.png', 'wu_8_2211264.png', 'wu_8_56312.png']
    img_list = list(set(q_list +h_list))
    for imgname in img_list:
        for info in txt_info:
            infoList = info.split('\t')
            imgName = infoList[0][:-1]
            if imgname in infoList:
                try:
                    shutil.move('D:/train_data\wu14CC\erzhihua\make_nu/nu_RGBA/'+imgName, 'D:/train_data\wu14CC\erzhihua\make_nu\er\er/'+imgName)
                except:
                    print(imgName)
                # print(infoList[0], imgname); quit()
                # re_list.append(infoList[2])




    # h_list = ['wu_1_2363762.png', 'wu_3_20171.png', 'wu_3_2545302.png', 'wu_7_1902953.png', 'wu_7_1754351.png', 'wu_8_3336856.png', 'wu_8_1562623.png', 'wu_8_2054769.png', 'wu_9_1711358.png', 'wu_9_2211265.png', 'wu_3_2545302.png', 'wu_7_1902953.png', 'wu_8_3107895.png', 'wu_8_2687875.png', 'wu_8_1648737.png', 'wu_8_2101630.png', 'wu_8_2906875.png', 'wu_9_2320734.png', 'wu_9_2320734.png', 'wu_8_2160389.png', 'wu_8_1902954.png', 'wu_8_1180635.png', 'wu_8_2054769.png', 'wu_8_1816987.png', 'wu_1_2614868.png', 'wu_6_1676148.png', 'wu_7_2336321.png', 'wu_8_1707452.png', 'wu_8_2520918.png', 'wu_8_2371593.png', 'wu_9_1711358.png', 'wu_9_2168235.png', 'wu_9_1723090.png', 'wu_9_2101631.png', 'wu_9_1711358.png', 'wu_9_1180636.png', 'wu_9_1816988.png', 'wu_1_3399444.png', 'wu_3_2534850.png', 'wu_3_2545302.png', 'wu_6_1707450.png', 'wu_7_1385160.png', 'wu_8_2101630.png', 'wu_8_68387.png', 'wu_8_2687875.png', 'wu_8_2371593.png', 'wu_9_2520919.png', 'wu_9_1899052.png', 'wu_9_1711358.png', 'wu_1_1503935.png', 'wu_1_1503935.png', 'wu_3_20171.png', 'wu_7_1902953.png', 'wu_8_2774560.png', 'wu_9_1813080.png', 'wu_9_2211265.png', 'wu_9_1899052.png', 'wu_9_2211265.png', 'wu_9_2211265.png', 'wu_3_2534850.png', 'wu_7_1754351.png', 'wu_7_1754351.png', 'wu_7_2434131.png', 'wu_8_1156597.png', 'wu_8_2449819.png', 'wu_8_3080067.png', 'wu_8_1515714.png', 'wu_8_1180635.png', 'wu_8_1816987.png', 'wu_8_3013934.png', 'wu_6_88363.png', 'wu_7_1777866.png', 'wu_9_433778.png', 'wu_9_68388.png', 'wu_3_1699625.png', 'wu_9_3257168.png', 'wu_9_1156598.png', 'wu_9_2265928.png', 'wu_9_414775.png', 'wu_9_433778.png', 'wu_9_1707453.png', 'wu_9_2211265.png', 'wu_0_128447.png', 'wu_1_3166715.png', 'wu_1_2363762.png', 'wu_3_1699625.png', 'wu_8_402718.png', 'wu_8_2039127.png']
    # q_list = ['wu_2_1648731.png', 'wu_5_2722583.png', 'wu_8_72507.png', 'wu_1_2097701.png', 'wu_6_2573156.png', 'wu_6_1734798.png', 'wu_7_237062.png', 'wu_7_1317140.png', 'wu_2_274783.png', 'wu_2_1361317.png', 'wu_5_196839.png', 'wu_5_1875631.png', 'wu_7_2238616.png', 'wu_8_2426318.png', 'wu_1_331020.png', 'wu_2_3121783.png', 'wu_8_158159.png', 'wu_8_410753.png', 'wu_0_158151.png', 'wu_0_1789601.png', 'wu_0_2882478.png', 'wu_1_2269824.png', 'wu_1_1353276.png', 'wu_1_2238610.png', 'wu_1_1196725.png', 'wu_1_434845.png', 'wu_1_1397255.png', 'wu_2_1236956.png', 'wu_2_2527881.png', 'wu_2_16100.png', 'wu_2_3069635.png', 'wu_3_1617437.png', 'wu_3_2281583.png', 'wu_3_2461476.png', 'wu_3_194359.png', 'wu_3_56307.png', 'wu_3_2833750.png', 'wu_3_3333376.png', 'wu_5_310927.png', 'wu_5_1906877.png', 'wu_6_3045259.png', 'wu_6_154126.png', 'wu_7_1365339.png', 'wu_7_2760604.png', 'wu_7_32273.png', 'wu_7_417696.png', 'wu_7_2402891.png', 'wu_7_1329217.png', 'wu_7_1184659.png', 'wu_0_3038293.png', 'wu_0_3121781.png', 'wu_0_1421121.png', 'wu_1_2788498.png', 'wu_1_2733000.png', 'wu_2_182324.png', 'wu_2_3385533.png', 'wu_2_2708701.png', 'wu_3_128450.png', 'wu_3_16101.png', 'wu_3_3160025.png', 'wu_3_1945977.png', 'wu_5_2109460.png', 'wu_6_237061.png', 'wu_6_85788.png', 'wu_7_3013933.png', 'wu_7_1035976.png', 'wu_7_32153.png', 'wu_7_64438.png', 'wu_8_1000022.png', 'wu_8_2211264.png', 'wu_8_56312.png']

if __name__ == "__main__":
    img_list = img_List()
    # find_erimg()


    # nu1_lsit = [os.path.join('D:/data/MNIST/raw/resize/no_biankuang/1/', na) for na in os.listdir('D:/data/MNIST/raw/resize/no_biankuang/1/')]
    # xuanzhuan_fh(1500,nu1_lsit)
    # cv2.imshow('ts',img)
    # cv2.waitKey(0)
    # zhengshu_pj(50000,img_list)
    # zhengshu_pj_RGBA(30000,img_list)

    hx_lsit = [os.path.join('D:/train_data/wu14CC/erzhihua/original/-50/', na) for na in os.listdir('D:/train_data/wu14CC/erzhihua/original/-50/')]
    # fh_list = [os.path.join('D:/train_data/wu14CC/erzhihua/original/fh/', na) for na in os.listdir('D:/train_data/wu14CC/erzhihua/original/fh/')]

    fengshu_pj(10000 , img_list,hx_lsit)
    # jiafengshu_pj(img_list,hx_lsit)
    # xuanzhuan_fh(10000 ,fh_list)
    # print(len(img_list),len(hx_lsit));quit()
    # pool = Pool(24)   # 24线程
    # pool.map(xuanzhuan_fh, fh_list)  # 注意map用法，是multiprocessing.dummy.Pool的方法
    # pool.close()
    # pool.join()

    # one_list = [os.path.join('D:/train_data/wu14CC/erzhihua/original/1/', na) for na in os.listdir('D:/train_data/wu14CC/erzhihua/original/1/')]
    # for i in range(1000):
    #     one_path = random.choice(one_list)
    #     la = one_path.split('_')[2]
    #     imgzs = cv2.imread(one_path, 0)
    #     cat_img = xuanzhuan_nu(imgzs)
    #
    #     cv2.imwrite(
    #         'D:/train_data/wu14CC/erzhihua/make_nu/ro/make1/wu_{}_{}.png'.format(la, random.randint(1, 999999)),
    #         cv2.resize(qiegebiankuangfs(cat_img), dsize=(52, 32)))

        # dange_zhengshu_pj(4, img_list)
    # img, la = dange_zhengshu_pj(2,img_list)
    # qiegebiankuang(img)




    # 测试图片resize
    # for name in os.listdir('D:/water/'):
    #     if 'jpg' in name:
    #         img = cv2.imread( 'D:\water/'+name )
    #         img = cv2.resize(img,dsize=(52,32))
    #         cv2.imwrite('D:\water/test/'+name ,img)


    # # # # 整理分数
    # path = 'D:/train_data/wu14CC/erzhihua/make_nu/fenshu_nu2/'
    # pather = 'D:/train_data/wu14CC/erzhihua/make_nu/fenshu_er/'
    # imgList = os.listdir(path)
    # for name in imgList:
    #     try:
    #         fz = name.split("-")[0].split("{")[1]
    #         fm = name.split("-")[1].split("}")[0]
    #         # print(fz,fm);quit()
    #         if fz[0] == '0' or fm[0] == '0':
    #             shutil.move(path+name ,pather+name)
    #             print(name)
    #     except:
    #         print(path+name)

    # dian_list = [os.path.join('D:/train_data/wu14CC/erzhihua/original/00028/', na) for na in os.listdir('D:/train_data/wu14CC/erzhihua/original/00028/')]
    # xiaoshu_pj(30000,img_list,dian_list)
    # fs_list = [os.path.join('D:/train_data/wu14CC/erzhihua/original/-30/', na) for na in os.listdir('D:/train_data/wu14CC/erzhihua/original/-30/')]
    # # fushu_xiaoshu_pj(20000, img_list,fs_list,dian_list)
    # fushu_pj(10000, img_list,fs_list)


    # # 整理负号
    # imglist = os.listdir('D:/train_data/wu14CC/erzhihua/original/1/')
    # for name  in imglist:
    #     img = cv2.imread('D:/train_data/wu14CC/erzhihua/original/1/' +name,0)
    #     h,w = img.shape
    #     center = (w , w)
    #     M = cv2.getRotationMatrix2D(center, 90, 1.0)
    #     img90 = cv2.warpAffine(img, M, (h, 2*w+1))
    #     img = img90[ w+1:2*w+1,0:h]
    #
    #     # cv2.imshow('t',img)
    #     # cv2.waitKey(0)
    #     sh = img.shape
    #     print(sh)
    #     if sh[1] > 49:
    #         cv2.imwrite('D:/train_data/wu14CC/erzhihua/original/51/'+name , img)
    #         # shutil.copy('D:/train_data/wu14CC/erzhihua/original/1/' +name ,'D:/train_data/wu14CC/erzhihua/original/50/'+name)
    #         print(name)

# 移动图片
    # imglist = os.listdir('D:/train_data/wu14CC/erzhihua/make_nu/xiaoshu_nu/')
    #
    # for name in imglist:
    #     la = name.split("_")[1]
    #     if len(la) == 5:
    #         shutil.move('D:/train_data/wu14CC/erzhihua/make_nu/xiaoshu_nu/' +name ,'D:/train_data/wu14CC/erzhihua/make_nu/xiaoshu4_nu/'+name)


    # print(len(img_list))