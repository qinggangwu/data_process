import os,random
from PIL import Image
import shutil

#  等号数，修改标签
def num_rename(path_in ,path_out):
    for root, dirs, files in os.walk(path_in):
        for name in files:
            remane0 = ''
            im_path = root + '/'+ name
            list = name.split('_')
            list[1] = '='+list[1]          #  等号数，修改标签
            remane = '_'.join(list)

            remane0 = "".join(remane.split(" "))  #消除标签空格
            # for i in remane:
            #     if i == ' ':
            #         pass
            #     else:
            #         remane0 +=i
            out_path  = path_out +remane0
            # print(out_path)
            im = Image.open(im_path)
            im.save(out_path)
    print('名称修改完成')


# 完成总txt文件
def witer_txt(im_path,txt_path):

    ftxt = open(txt_path, 'a',encoding='utf-8')
    ftxt.truncate(0)
    # try:

    # # 文件名称有空格，消除空格
    # img_name_list = os.listdir(im_path)
    # for na in img_name_list:
    #     na0 = ''.join(na.split(' '))
    #     shutil.move(im_path+na,im_path+na0)
    files = os.listdir(im_path)
    # for root, dirs, files in os.walk(im_path):
    for name in files[1:]:
        # name0 = root + '/' + name

        lable = name.split("_")
        # print(name,name0 , lable)

        s = name + '\t'+lable[1]
        # print(s )
        ftxt.writelines(s + '\n')
    ftxt.close()

def lable_change(path):
    # path = 'E:/BaiduNetdiskDownload/wu14CC/整理好数据/totladata.txt'

    f = open(path)

    lin = f.readlines()
    write_list = []
    for l in lin:
        ll = l[:-1].split(' ')
        k = ll.pop(1)
        # print(k)

        s = ''

        for i in range(len(k)):
            num = ord(k[i])
            # print(num)
            if num == 61:
                s += ' 11'
            elif num == 46:
                s += ' 12'
            elif num ==44:
                s += ' 13'
            elif num == 45:
                s += ' 66'
            elif 64< num <91:
                s += ' '+str(num-51)
            elif 96 < num < 123:
                s += ' '+str(num - 57)
            # else:
            #     s += ' {}'.format(int(k[i]) + 1)

            elif 47<num<58:
                s += ' {}'.format(int(k[i]) + 1)

            else:
                s +=''

        s0 = ll[0] + s
        write_list.append(s0 + '\n')
    f.close()

    write_txt = open(path, 'w')
    # write_txt.truncate(0)
    write_txt.writelines(write_list)
    write_txt.close()

# 制作train 和 text  txt文件
def train_test_txt(tatlo_path,train_path,test_path):
    totla_txt = open(tatlo_path, 'r',encoding='utf-8')
    test_txt = open(test_path, 'a',encoding='utf-8')
    train_txt = open(train_path, 'a',encoding='utf-8')
    test_txt.truncate(0)       #清空txt文档所有内容
    train_txt.truncate(0)
    random_num = []

    totla_data = totla_txt.readlines()
    n_test = int(len(totla_data)*0.15 )
    for i in range(n_test):
        n = random.randint(1,len(totla_data)-1)
        random_num.append(n)

    random_num = list(set(random_num))

    for i in range(len(totla_data)):
        s = totla_data[i]
        if i in random_num:
            test_txt.writelines(s)
        else:
            train_txt.writelines(s)
    test_txt.close()
    train_txt.close()



if __name__ =="__main__":
    # img_path = 'D:/train_data/wu14CC/Chinese_data/'


    img_path = 'E:/Pytorch/ss/cat_img/'

    path_out = 'E:/BaiduNetdiskDownload/wu14CC/Integer/'
    # num_rename(path,path_out)
    totlatxt_path = 'E:/Pytorch/PaddleOCR-release-2.2/train_data/totladata.txt'
    traintxt_path = 'E:/Pytorch/PaddleOCR-release-2.2/train_data/nutrain.txt'
    testtxt_path = 'E:/Pytorch/PaddleOCR-release-2.2/train_data/nutest.txt'

    witer_txt(img_path,totlatxt_path)
    # lable_change(totlatxt_path)
    train_test_txt(totlatxt_path, traintxt_path, testtxt_path)

    # print(len("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"))

