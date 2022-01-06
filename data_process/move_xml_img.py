import os
import shutil
import numpy as np
import cv2
import random
import re
from PIL import Image
import matplotlib.pyplot as plt


# 移动xml文件，生成对应的专属图片文件
def move_img():
    xml_list  = os.listdir(r'D:\data\orgimage\Chinese_orgiamge\xml/')
    for name in xml_list:
        img_name0 = name.replace('xml','jpg')
        img_name = os.path.join(r'D:\data\orgimage\Chinese_orgiamge\img/',img_name0)
        # print(name)
        if not os.path.exists(os.path.join(r'D:\data\orgimage\Chinese_orgiamge\img/',img_name0)):
            shutil.copy(os.path.join(r'D:\data\orgimage\Chinese_orgiamge\ycl/',img_name0),img_name)
            print('正在移动图片： {}'.format(name.replace('xml','jpg')))


def move_img_json():
    xml_list  = os.listdir(r'D:/data/orgimage/segment_orgiamge/train_img/json/')
    for name in xml_list:
        img_name0 = name.replace('json','jpg')
        img_name = os.path.join(r'D:\data\orgimage\segment_orgiamge\train_img/',img_name0)
        # print(name)
        if not os.path.exists(img_name):
            try:
                shutil.copy(os.path.join(r'D:\data\orgimage\Chinese_orgiamge\ycl/',img_name0),img_name)
                print('正在移动图片： {}'.format(name.replace('xml','jpg')))
            except:
                print('图片文件夹不正确')




def make_fh_txt():
    finfo  = open('E:/Pytorch/PaddleOCR-release-2.2/ppocr/utils/chiese_dict.txt',encoding= 'utf-8').readlines()
    fw = open('E:/Pytorch/PaddleOCR-release-2.2/ppocr/utils/chiesefh_dict.txt','w',encoding= 'utf-8')
    a = []
    for i in finfo:
        i = i[:-1]
        try:
            if  ord(i) <13300:
                print(i,ord(i))
                a.append(i + '\n')
        except:
            pass

    fw.writelines(a)
    fw.close()

# 读取npy文件里面的图片
def load_npy():
    img_info = np.load('D:/data/中文手写数据/字符样本数据/mpy/test_images.npy')
    lab_info = np.load('D:/data/中文手写数据/字符样本数据/mpy/test_labels.npy')
    for i in range(len(img_info)):
        img_name = 'D:/data/wutest/wu_{}_{}.jpg'.format(lab_info[i],random.randint(1,999999))
        cv2.imwrite(img_name,img_info[i])
    # print(img_info[1] , lab_info[1])

# 查看图片名称和文件夹加分类是否正确
def look_rename():
    a = []
    file_path = os.listdir('D:/data/CASIA/train')
    for name in file_path:
       img_path = os.path.join('D:/data/CASIA/train/' , name)
       img_list = os.listdir(img_path)
       for img_name in img_list:
           lable = img_name.split('_')[1]
           # print(a ,lable) ;quit()
           if name !=lable:
               a.append(name)
               print(a)
               break
    print(a)

def move_yuliang_img():
    file_name = os.listdir('D:/train_data/wu14CC/yn/')
    file_bg = os.listdir('E:/Pytorch/PaddleOCR-release-2.2/StyleText/output_data/images/bg/')
    for name in file_bg[::2]:
        label = name[:-8].split("_")[-3:]
        bz = '_'.join(label)
        for img_name in file_name:
            if bz in img_name:
                shutil.copy('D:/train_data/wu14CC/yn/'+img_name,'D:/train_data/wu14CC/yuniao/'+img_name)
                print('正在移动：{}'.format(img_name))

def make_yuniao_txt():

    # print(bz)
    file_name = os.listdir('D:/train_data/wu14CC/yuniao/')
    info = []
    for name in file_name:
        label = name.split("_")[1]
        ss = name + '\t' + label
        info.append(ss + "\n")

    fw = open('E:/Pytorch/PaddleOCR-release-2.2/StyleText/examples/ylinfo.txt', 'w', encoding='utf-8')
    fw.writelines(info)
    fw.close()

def make_info_txt():
    s = []
    fr = open('E:\Pytorch\PaddleOCR-release-2.2\StyleText\examples\corpus/info.txt','r',encoding= 'utf-8').readlines()
    for i in fr:
        res = re.findall(u"[\u4e00-\u9fa5]", i)
        # print(res,len(res))
        if len(i)< 6 and len(i)-1 == len(res):
            s.append(i)
            # print(i,len(i) ,len(res))
    fw = open('E:\Pytorch\PaddleOCR-release-2.2\StyleText\examples/info.txt','w')
    fw.writelines(s)
    fw.close()

def remove_img(path ='D:/train_data/wu14CC/Chinese_make_data/images/wu_train/'):

    img_list = os.listdir(path)
    for name in img_list:
        fp = open(path + name, 'rb')
        img = Image.open(fp)
        fp.close()

        # img = Image.open()

        w,h = img.size
        if w > h*4.5:
            os.remove(path + name)
            print('正在删除 ：{}'.format(name))
# import random
def get_img(path):
    file_list = os.listdir(path)
    img_name = random.choice(file_list)
    # fp = open(path + img_name, 'rb')
    # img = Image.open(fp)
    # fp.close()
    img = Image.open(path + img_name)
    lable = img_name.split("_")[1]
    return  img,lable

def image_compose(imag, imag_1,i):
    h , w = 32,32
    # src = os.path.join(os.path.abspath(IMAGE_SAVE_PATH), img)
    to_image = Image.new('RGB', (i * w, h))  # 创建一个新图
    # 把两张图片按顺序粘贴到对应位置上
    # rom_image = imag.resize((h, w), Image.ANTIALIAS)
    rom_image_1 = imag_1.resize((h, w), Image.ANTIALIAS)
    to_image.paste(imag, (0, 0))
    to_image.paste(rom_image_1, (w*(i-1), 0))

    return to_image


def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = img.getpixel((2,2))
    for h in range(H):
        for l in range(L):
            dot = (l,h)
            color_1 = img.getpixel(dot)
            # print(color_1 , color_0)
            if color_1[0] > 250 or color_1[1] > 250 or color_1[2] > 250 or l==0 or h==0:
            # if color_1 == color_0 or l==0 or h==0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot,(0,0,0,0))
            # else:
            #     print(img.getpixel(dot))
    return img


# 修改标签，分为4类，nu数字，en英语单词，fs分数，ch中文
def rename_img(path = 'D:/train_data/wu14CC/ss/sss/'):
    img_list = os.listdir(path)
    for name in img_list:
        nn = name.split("_")
        resch = re.findall(u"[\u4e00-\u9fa5]", name)
        rescn = re.findall(r'[a-zA-Z,]', nn[1])
        resnu = re.findall(r'[0-9A-DEFXV.xv×√]',nn[1])

        if len(resnu) == len(nn[1]):
            nn[0] = 'nu'
            if len(nn[1]) == 1:
                if nn[1] in "xX":
                    nn[1] = '×'
                elif nn[1] in "vV":
                    nn[1] = '√'
        # elif len(rescn)== len(nn[1]) and rescn[0] not in 'ABCDEFTFXV':
        elif len(rescn)== len(nn[1]) :
            nn[0] = 'en'
        elif "{" in nn[1] or "}"in nn[1]:
            nn[0] = 'fs'
        else:
            nn[0] = 'ch'
        nwename = '_'.join(nn)
        # print(name,nwename)

        os.rename(path+name,path+nwename)




if __name__ == '__main__':
    # rename_img(path= 'D:/train_data/wu14CC/Chinese_data/')
    move_img_json()
    # move_img()
    # make_fh_txt()
    # load_npy()
    # look_rename()
    # print(ord('伶'))
    #
    # remove_img()  # 删除长宽比不合适的图片
    # move_yuliang_img()   # 移动语料背景图片
    # make_yuniao_txt()    # 生成语料背景txt文件
    # make_info_txt()    # 生成语料txt文件









