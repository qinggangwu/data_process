import math
import os
import time
import xlrd
import cv2
import onnxruntime
import numpy as np
from xlutils.copy import copy
from scipy import misc
import imageio
import skimage.io as io
from multiprocessing import Pool


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

def decode(t, length, raw=False):
    alphabet = "0123456789w.:-"
    char_list = []
    for i in range(length):
        if t[i] != 0 and (not (i > 0 and t[i - 1] == t[i])):
            char_list.append(alphabet[t[i] - 1])
    return ''.join(char_list)

def shibei(img_list):
    session = onnxruntime.InferenceSession("gp.onnx")
    input_name = getattr(session.get_inputs()[0], 'name')
    s = []
    for img in img_list:
        img = resize_norm_img(img, [3, 32, 100])
        preds = session.run([], {input_name: img[np.newaxis, :]})
        preds = np.unravel_index(np.argmax(preds[0][0], axis=1), preds[0][0].shape)[1]   # 获取每个预测位置上的最大值索引
        sim_pred = decode(preds, 25, raw=False)
        s.append(sim_pred)
    return s

def read_img800(img):    # (800,1280,3)
    img_list = []
    img_list.append(img[28:45, 1078:1130])
    img_list.append(img[470: 486, 5:53])
    return img_list

def write_excel(path,info_list):
    book = xlrd.open_workbook(path)  # 打开一个工作表
    sheet1 = book.sheet_by_index(0)  # 通过索引获取表
    ncol = sheet1.ncols  # 表的列数
    gp = [i for i in sheet1.col_values(1) if len(i) >0]
    nrow = len(gp)
    gp = gp[1:]

    book2 = copy(book)
    sheet0 = book2.get_sheet(0)
    sheet0.write(0,ncol,time.strftime('%m-%d', time.localtime()))
    ind = []

    for i in range(len(gp)):
        for j in range(0 , len(info_list) ,2):
            if gp[i] == info_list[j]:
                sheet0.write(i+1,ncol, info_list[j+1])
                ind.append(j)
                ind.append(j+1)
    ind = sorted(ind,reverse= True)
    for x in ind:
        info_list.pop(x)
    if info_list != None:
        info_dict = dict(zip([info_list[i] for i in range(0, len(info_list), 2)],[info_list[i] for i in range(1, len(info_list), 2)]))
        info_dict = sorted(info_dict.items(), key=lambda d: d[0])
        n = 0
        for key in info_dict:
            sheet0.write(nrow + n, 1, key[0])
            sheet0.write(nrow + n, ncol, key[1])
            n+=1
    try:
        book2.save(path)
    except:
        print('请关闭股票表格后重新运行')

def resize_image(file_name):
    try:
        img = cv2.imread(file_name)
        img_list = read_img800(img)
    except:
        print(file_name)
    return img_list



def main():
    start0 =time.time()
    img_path = 'C:/Users/Administrator/Downloads/tpAgu/'      # 股票图片的目录，后面记得加个 /
    txt_path = 'D:/data/project/test.xls'                     # 粗存结果的表格，尽量不用中文。
    img_list = []
    img_paths = [os.path.join(img_path, pa)   for  pa in os.listdir(img_path)]
    pool = Pool(6)
    s = pool.map(resize_image, img_paths)
    for reimg in s:
        img_list +=reimg
    pool.close()
    pool.join()
    print('读取图片时间',time.time() - start0)
    start1 = time.time()
    re = shibei(img_list)
    write_excel(txt_path, re)
    print('识别和写入时间', time.time() - start1)

if __name__=="__main__":
    start = time.time()
    main()
    print('程序总消耗时间',time.time() -start)

