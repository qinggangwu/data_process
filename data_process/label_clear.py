import re
import os
import cv2
import shutil
from PIL import Image


def claer_la(label):
    label = label.split("_")[1]
    # ret = re.match("([^-]*){(\d+)",label)
    ret = label.split('{')
    res = label.split('}')
    er = []
    # print(ret)

    if '()' in ret[1] or '+' in ret[1] :
        return True
    elif len(res) >=2 :
        for i in ['+', '-', '*', '/']:
            if i in ret[0] or i in res[1]:          # 分数前后有计算的都剔除
                return True
    else:
        print(label)



    char_spl = re.findall('[\u4e00-\u9fa5]', label)      # 查找所有的中文字符
    char_english = re.findall(r'[A-Za-z]', label)        # 查找所有的英文字符
    char_num = re.findall(r'[0-9]',label)                # 查找所有的数字
    # print(char_num)

    # if len(char_spl)!=0 or len(char_english) != 0 or len(char_num) > 5:
    if len(char_spl)!=0 or len(char_english) != 0 :
        return True
        # print(char_spl)
    return False

def move_img(img_path, move_path):
    # file_list = os.listdir(img_path)[:15]
    file_list = ['E:/BaiduNetdiskDownload/wu14CC/qiegefs/clear2wu']
    if not os.path.exists(move_path):
        os.makedirs(move_path)

    for file in file_list:

        file = os.path.join(img_path, file)
        print(file)
        img_list = os.listdir(file)
        for img_name in img_list[1:]:
            img_name0 = os.path.join(file, img_name)

            if len(img_name.split("_")) < 3:
                shutil.move(img_name0, os.path.join(move_path, img_name))
                print('正在移动： {}'.format(img_name))
            else:
                fp = open(img_name0, 'rb')
                img = Image.open(fp)
                fp.close()
                w, h = img.size

                if w > 1.6 * h:
                    shutil.move(img_name0, os.path.join(move_path, img_name))
                    print('正在移动： {}'.format(img_name))
                elif claer_la(img_name):
                    shutil.move(img_name0, os.path.join(move_path, img_name))

                    print('正在移动： {}'.format(img_name))


def remove_img(file_path):
    a = os.listdir(file_path)

    if not os.path.exists(os.path.join(file_path, 'remove')):
        os.makedirs(os.path.join(file_path, 'remove'))
    name_ll = []
    img_name = []

    for aa in os.listdir(os.path.join(file_path, 'remove')):
        ss = "".join(aa.split("_")[1:3])
        name_ll.append(ss)

    for path in a:
        img_list = os.listdir(os.path.join(file_path,path))

        for name in img_list:
            flag = True
            name0 = "".join(name.split("_")[1:3])
            if name0 not in name_ll:
                shutil.move(os.path.join(file_path,path,name),os.path.join(file_path,'remove',name))
                name_ll.append(name0)
                img_name.append(name)
            else:
                fp = open(os.path.join(file_path,path,name), 'rb')
                img1 = Image.open(fp)
                fp.close()
                w1, h1 = img1.size
                # img1 = Image.open(os.path.join(file_path,path,name))
                for oldname in img_name:
                    if "".join(oldname.split("_")[1:3] ) == name0:
                        fp = open(os.path.join(file_path,'remove',oldname), 'rb')
                        img2 = Image.open(fp)
                        fp.close()
                        w2, h2 = img2.size
                        if w1==w2 or h1 ==h2:
                            flag = False
                if flag:
                    shutil.move(os.path.join(file_path,path, name), os.path.join(file_path, 'remove', name))
                    img_name.append(name)



def move_img2file(img_path,img2path):
    img_name = os.listdir(img_path)
    for name in img_name:
        na = name.split("_")[1]
        if not os.path.exists(os.path.join(img2path,na)):
            os.makedirs(os.path.join(img2path,na))
        shutil.move(os.path.join(img_path,name),os.path.join(img2path,na,name))

if __name__ == "__main__":
    img_path = 'E:/BaiduNetdiskDownload/wu14CC/qiegefs/'
    move_path = 'E:/BaiduNetdiskDownload/wu14CC/qiegefs/clear2wu/ss'
    # move_img(img_path, move_path)
    # label = 'wu_({35-15})_1397835_153.jpg'
    # print(claer_la(label))
    remove_img('E:\BaiduNetdiskDownload\wu14CC\qiegefs\wuclear')
    # move_img2file('E:\BaiduNetdiskDownload\wu14CC\qiegefs\ss','E:\BaiduNetdiskDownload\wu14CC\qiegefs\wuclear')

