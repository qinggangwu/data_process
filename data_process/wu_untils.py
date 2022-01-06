import os
import cv2
import random
import shutil
import time
import requests
import urllib.request
import pymysql
import numpy as np
from xml.dom.minidom import parse
from PIL import Image
from multiprocessing.dummy import Pool
import re

# 一些常用文件处理方法

# # 文件不存在，创建
# if not os.path.exists(path):
#     os.makedirs(path)

# 读取路径的文件夹、目录、根目录
# for root, dirs, files in os.walk(path):





# 读取xml内容
def readXML(xname):
    info_list = []
    domTree = parse(xname)
    rootNode = domTree.documentElement
    # 所有顾客
    customers = rootNode.getElementsByTagName("object")

    for customer in customers:
        if not customer.hasAttribute("name"):
            name = customer.getElementsByTagName("name")[0].childNodes[0].data
            # print("name:", name.childNodes[0].data)
            box = customer.getElementsByTagName("bndbox")[0]
            xmin = box.getElementsByTagName("xmin")[0].childNodes[0].data
            # print(xmin.nodeName, ":", xmin.childNodes[0].data)
            ymin = box.getElementsByTagName("ymin")[0].childNodes[0].data
            # print(ymin.nodeName, ":", ymin.childNodes[0].data)
            xmax = box.getElementsByTagName("xmax")[0].childNodes[0].data
            # print(xmax.nodeName, ":", xmax.childNodes[0].data)
            ymax = box.getElementsByTagName("ymax")[0].childNodes[0].data
            # print(ymax.nodeName, ":", ymax.childNodes[0].data)

            info_list.append([name,xmin,ymin,xmax,ymax])
    return info_list

# 切割xml文件标签图片
def qg_xml_img(xml_path,img_path,img_out_path,n):
    xml_list = os.listdir(xml_path)
    n = n
    num = 0
    for name in xml_list:
        print(name)
        # name = '006757.xml'
        img = cv2.imread(img_path+name.replace('xml','jpg'))
        infobox = readXML(xml_path+name)
        for i in infobox:
            im_name = i[0]
            out_img = img[int(i[2]):int(i[4]) , int(i[1]):int(i[3])]
            out_img_name = '/wu_'+im_name+'_'+name[:-4]+'_'+'0'*(5-len(str(n)))+str(n)+'.jpg'
            n+=1
            img_out_path0 = os.path.join(img_out_path,im_name)
            try:
                if not os.path.exists(img_out_path0):
                    os.mkdir(img_out_path0)
                cv2.imencode('.jpg', out_img)[1].tofile(img_out_path0+out_img_name)   # 保存文件名里面有中文
            except:
                pass
            print('正在切割:  {}'.format(im_name))
            num+=1
    print(num)

# 查看torch各版本
def wutest_version():
    import torch
    print(torch.__version__)  # torch 版本
    print(torch.version.cuda)  # cuda版本
    print(torch.backends.cudnn.version())  # cudnn 版本
    # print(torch.version.cudnn)
    print(torch.cuda.is_available())  # cuda是否可以用
    print(torch.cuda.device_count())  # cuda 可用的数量

    print(torch.cuda.get_device_name(0))  # 显卡型号
    print(torch.cuda.current_device())  # 显卡的编号

# Image切去图片边缘
def get_size(path):
    im = Image.open(path)
    iml = im.load()
    width,heigth = im.size
    x_max, x_min, y_max, y_min = 0, 128, 0, 128
    for i in range(width):
        for j in range(heigth):
            if iml[i, j][0] < 10 and y_min > j:
                y_min = j
            if iml[i, j][0] < 10 and y_max < j:
                y_max = j
            if iml[i, j][0] < 10 and x_min > i:
                x_min = i
            if iml[i, j][0] < 10 and x_max < i:
                x_max = i
    return (x_min-3,y_min-3 , x_max+3,y_max+3)

# cv2 去掉二值化白色边缘
def qiegebiankuang(img):
    # path= ''
    # img = cv2.imread(path,0)   #读取灰度图
    h,w = img.shape
    xi,yi,xa,ya = w,h,0,0
    for i in range(h):
        for j in range(w):
            if img[i][j] != 255:
                ya = i
                if i < yi:
                    yi = i
    for i in range(w):
        for j in range(h):
            if img[j][i] != 255:
                xa = i
                if i < xi :
                    xi = i

    imgcat = img[yi : ya ,xi :xa]
    return imgcat

# 制作train 和 text  txt文件
def train_test_txt(path,train_path,test_path):
    """"
    path 图片所在目录
    train_path 生成train.txt 目录
    test_path 生成test.txt 目录
    ex：
    train_test_txt(path='D:/train_data/wu14CC/erzhihua/make_nu/tow_nu/',train_path ='train.txt',test_path='test.txt')


    """
    test_txt = open(test_path, 'w',encoding='utf-8')
    train_txt = open(train_path, 'w',encoding='utf-8')
    # test_txt.truncate(0)       #清空txt文档所有内容
    # train_txt.truncate(0)
    test = []
    train = []

    num = len(os.listdir(path))
    print("图片总数量为 ： {}".format(num))
    n_test = int(num * 0.15)   # 控制测试文本长度，
    random_num = [random.randint(1, num - 1) for j in range(n_test)]
    random_num = list(set(random_num))

    totla_data = []
    # path  为图片所在的目录
    for i,name in enumerate(os.listdir(path)):
        # if name[-3:] in ['jpg','png']:
        la = name.split("_")[1]
        if name.split("_")[0] == 'wu':
            if la == '27':
                la = '<'
            elif la == '29':
                la = '>'
        s = name + '\t'+la + '\n'

        if i in random_num:
            test.append(s)
        else:
            train.append(s)


    # totla_data.append()

    # for i in range(num):
    #     s = totla_data[i]
    #     if i in random_num:
    #         test.append(s)
    #         # test_txt.writelines(s)
    #     else:
    #         train.append(s)
    #         # train_txt.writelines(s)

    test_txt.writelines(test)
    train_txt.writelines(train)
    test_txt.close()
    train_txt.close()


# 获取文件夹图片的方差和均值
def make_mean_std():
    # img_h, img_w = 32, 32
    img_h, img_w = 32, 48  # 根据自己数据集适当调整，影响不大
    means, stdevs = [], []
    img_list = []

    imgs_path = 'E:/BaiduNetdiskDownload/wu14CC/Integer/'
    imgs_path_list = os.listdir(imgs_path)

    len_ = len(imgs_path_list)
    i = 0
    for item in imgs_path_list:
        img = cv2.imread(os.path.join(imgs_path, item))
        img = cv2.resize(img, (img_w, img_h))
        img = img[:, :, :, np.newaxis]
        img_list.append(img)
        i += 1
        if i % 100 == 0:
            print(i, '/', len_)

    imgs = np.concatenate(img_list, axis=3)
    imgs = imgs.astype(np.float32) / 255.

    for i in range(3):
        pixels = imgs[:, :, i, :].ravel()  # 拉成一行
        means.append(np.mean(pixels))
        stdevs.append(np.std(pixels))

    # BGR --> RGB ， CV读取的需要转换，PIL读取的不用转换
    means.reverse()
    stdevs.reverse()
    print("normMean = {}".format(means))
    print("normStd = {}".format(stdevs))


# 建立数据库对象
class db():
    # 构造函数
    def __init__(self, hostnum=0):
        hosts = [['192.168.0.123', 'db_001', 'db_001', 'db_001']]
        # hosts = [['127.0.0.1', 'root', '123123', 'test']]

        self.conn = pymysql.connect(host=hosts[hostnum][0], user=hosts[hostnum][1], password=hosts[hostnum][2], port=3306, database=hosts[hostnum][3], charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query(self, sql, data=None):
        self.cursor.execute(sql, data)
        self.conn.commit()

    def selectOne(self, sql):
        re = self.select(sql)
        if len(re) == 0: return {}
        return re[0]

    def select(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def insert(self, table, data_dict, return_insert_id=0):
        self.query("insert into " + table + "(" + ",".join(data_dict) + ") values(" + ("%s,"*len(data_dict)).rstrip(',') + ")", tuple(data_dict.values()))
        if return_insert_id: return self.cursor.lastrowid

    # 析构函数
    def __del__(self):
        self.cursor.close()
        self.conn.close()

# 下载图片
def dowload_img(i):
    db1 = db()
    # re = db1.select('select * from pre_m_check_homework  where subject_id =3  limit 1000,9000')       # 134381   21100
    # re = db1.select('select * from pre_m_check_homework l')       # 134381   21100
    # re = db1.select('select * from pre_m_check_homework where id < 900000')       # 134381   21100
    # re = db1.select('select id,img,baidu_ocr_result from a_single_page_ocr limit {},{}'.format(500*i,500*(i+1)))       # 134381   21100
    re = db1.select('SELECT o.id,o.width,o.height,p.pleft,p.ptop,p.pwidth,p.pheight,o.img,p.ocr_text FROM a_single_page_timupos as p  left join  a_single_page_ocr as o on p.bookid=o.bookid and p.typeid=o.typeid and p.page=o.page  where o.id=4444')       # 134381   21100
    print(re) ;quit()
    # re = db1.select('select id,image,ocr_info from pre_m_check_homework  Where id > {} order by id asc limit 10000' .format(5000))
    # print(re)
    n = 34537

    # m = 0  #切割图片数量
    file_path = 'D:/data/orgimage/qieti_orgiamge/'
    txt_path = 'D:/data/orgimage/qieti_orgiamge_txt/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    for i in re:
        imgurl=i['img']
        # for j in imgurl:
            # img_url ='http://user.1010pic.com/' +j
        img_url ='http://thumb.1010pic.com/' +imgurl     # 切割 pic url

        print(img_url)
        # m += 1
            # i0 = str(n)
        # imgname = str(i['id']) +'_'+'0'*(6-len(str(m))) +str(m) +'.jpg'
        imgname = str(i['id']) +'.jpg'
        print(imgname)
        # download_img(file_path,imgname,img_url)

        # txtname = imgname.replace('jpg','txt')
        # fw = open(txt_path + txtname , 'w',encoding= 'utf-8')
        # js = json.dumps(eval(i['baidu_ocr_result']),ensure_ascii= False)
        # fw.writelines(js)
        # fw.close()


# 图像瞄框
def huakuang():
    fr = open('E:\Pytorch\PaddleOCR-release-2.2\output/predicts_db450.txt')
    info_list = fr.readlines()
    for info in info_list[:30]:
        img_path = info.split()[0]
        info_points = eval(info[51:])
        img = cv2.imread(img_path)
        img = img.copy()
        for point in info_points:
            pts = np.array(point['points'], np.int32)  # 数据类型必须为 int32
            # print(len(pts))     # 长度为4
            pts = pts.reshape((-1, 1, 2))

            cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

        # cv2.imshow('test',img)
        # cv2.waitKey(0)

        # path = os.path.join('D:\data\paddlere_img', img_path[-10:])
        # cv2.imwrite(path,img)


# 移动图片
def move_image():
    # img_path = 'D:/train_data/wu14CC/erzhihua/make_nu/fenshu_nu/'
    re_path = 'D:/train_data/wu14CC/erzhihua/make_nu/all/'
    path = 'D:/train_data/wu14CC/erzhihua/make_nu/'
    for root, dirs, files in os.walk(path):
        print(root)
        print(dirs)
        # print(files)

        for dir in dirs:
            if dir != 'all':
                img_path = os.path.join(root ,dir)

                for name in os.listdir(img_path):
                    shutil.copy(os.path.join(img_path,name) ,re_path +name)
                    # print(os.path.join(img_path,name) ,re_path +name)
            else:
                img_path = ''
            print(img_path)


# 获取path下所有的图片 返回列表
def get_image_paths(path):
    return [os.path.join(path,name) for name in os.listdir(path) ]

# 多进程处理图片
# save_dir = 'E:/reksall2/'
# dir = 'E:/ks_test/'
global count
count=0

def duo_resize_image(filename):   #图片risize
    global count

    # full_file_name = os.path.join(dir, filename)
    # 保存的新路径
    # new_full_file_name = os.path.join(save_dir, filename.split('\\')[-1])
    # print("文件全路径：",full_file_name)
    # image = np.array(Image.open((filename)))  # 打开图片，转换为ndarray
    image = cv2.imread(filename)

    # 添加高斯噪声，方差0.002
    # image = util.random_noise(image, mode='gaussian', var=0.002)
    # print(full_file_name,new_full_file_name)

    # print(image.shape)
    if image.shape[1] > 5*image.shape[0]:
        # print(filename)
        image_resized = cv2.resize(image, dsize= (160,32))   # dsize=(w,h)
        cv2.imwrite(filename, image_resized)
        count = count + 1
    if count %3000 ==0:
        print('存储resize之后的图像，第 {} 张，存储成功！'.format(count))

# 多线程处理图片
def move_img():
    path = 'D:/train_data/wu14CC/erzhihua/all/'   # 文件夹路径
    path = 'E:/all/'   # 文件夹路径

    # print(os.path.splitext('20210929145640.jpg'))

    images =[os.path.join(path,name) for name in os.listdir(path) if os.path.splitext(name)[-1] in ['.jpg','.png']]     #   获取图片的路径列表   已经有缺省参数

    pool = Pool(24)   # 24线程
    pool.map(duo_resize_image, images)  # 注意map用法，是multiprocessing.dummy.Pool的方法
    pool.close()
    pool.join()

# 移动标签不正确的图片
def move_er_img():

    path = 'E:/all/'
    remove_path = 'E:/er/8/'
    imglist = os.listdir(path)
    for name in imglist:
        if 'png' not in name:
            continue
        else:
            re = name.split("_")
            try:
                if 'nu' in re[0] and '8' in re[1][1:-1]:
                    shutil.move(path +name ,remove_path +name)
            except:
                print(name)

            # os.remove(remove_path+name)
            # print('正在删除图片 ： {}'.format(name))


def list_test(a:list, b:list):
    c = []
    if len(a) ==0 or len(b) == 0:
        return a + b
    for i in range(len(a+b)):
        if len(a) ==0 or len(b)==0:
            break
        if a[0] <= b[0]:
            c.append(a.pop(0))
        else:
            c.append(b.pop(0))
    if len(a) == 0:
        return c + b
    else:
        return c + a

def rename():
    path = 'D:/train_data/wu14CC/Chinese/Chinese_1210/wu_en/'
    img_lsit = os.listdir(path)
    for name in img_lsit:
        new_name = name.split('_')
        new_name[0] = 'en'
        new_names = '_'.join(new_name)

        os.rename(path+name,path+new_names)
        # if ' ' in name:
        #     print(name)

# 修改标签，分为4类，nu数字，en英语单词，fs分数，ch中文
def move_dir():
    path = 'D:/train_data/wu14CC/Chinese/Chinese_1210/'

    img_list = os.listdir(path)
    for name in img_list:
        # nn = name.split("_")
        resch = re.findall(u"[\u4e00-\u9fa5]", name)
        # rescn = re.findall(r'[a-zA-Z,]', nn[1])
        # resnu = re.findall(r'[0-9A-DEFXV.xv×√]',nn[1])
        resen = re.findall(r'[a-zA-Z, ]', name)
        resnu = re.findall(r'[0-9A-FXV.xv×√]',name)

        # print(resch,rescn,resnu)
        try:

            if  0 != len(resch):
                shutil.move(path +name, path +'wu_ch')
            elif '{' in name or '}'in name:
                shutil.move(path +name, path +'wu_fs')
            elif len(name) == len(resnu):
                shutil.move(path +name, path +'wu_nu')
            elif len(name) == len(resen):
                shutil.move(path +name, path +'wu_en')
        except:
            print(name)

# 移动xml文件对应的图片
def move_xmlimg():
    xml_path = 'D:/train_data/handwriting_rec/xmlall/'
    img_orpath = 'D:/data/orgimage/Chinese_orgiamge/wclall/'
    img_savepath = 'D:/train_data/handwriting_rec/imgall/'

    xml_list = os.listdir(xml_path)
    for name in xml_list:
        imgname = name.replace("xml",'jpg')
        shutil.copy(img_orpath +imgname ,img_savepath +imgname)

if __name__ == '__main__':

    # huakuang()
    # move_image()
    # s =time.time()
    # train_test_txt(path='E:/ks_test/',
    #                train_path='E:/Pytorch/PaddleOCR-release-2.2/train_data/re2kstrain.txt',
    #                test_path='E:/Pytorch/PaddleOCR-release-2.2/train_data/re2kstest.txt')
    # print(time.time() -s)

    # move_dir()
    rename()
    # move_er_img()


    # a = [1,3,5,20,30]
    # b = [8,9,10,20]
    # # b = []
    # # print(list_test(a,b))
    # for index, i in enumerate(a):
    #     print(index,i)

    # img_list = [os.path.join(,name) for name in os.listdir('D:/data/') if os.path.splitext(name)[-1] == '.jpg']
    # print(len(img_list))

    # encode = open('D:/data/Synthetic Chinese String Dataset/char_std_5990.txt',encoding= 'utf-8').readlines()
    #
    # infolist = open('C:/Users/MyPC/Downloads/wordninja_words.txt',encoding= 'utf-8').readlines()
    # xiaoxues = open('C:/Users/MyPC/Downloads/english-wordlists-master/小学英语大纲词汇.txt',encoding= 'utf-8').readlines()
    # newtxt = open('D:/data/newWord.txt','w',encoding= 'utf-8')

    # info_list = [ os.path.join('Synthetic_Chinese_String_Dataset',lin) for lin in  infolist]
    #
    # for word in xiaoxues:
    #     if word not in infolist:
    #         infolist.insert(0,word)
    #         print(word)
    # for index,info in enumerate(infolist):
    #     infolist = info.split()
    #     imgname = infolist[0]
    #     label_list = [encode[int(index)][:-1] for index in [infolist[i] for i in range(1, len(infolist))]]
    #     label = ''.join(label_list)
    #     la = imgname + '\t'+ label +'\n'
    #     info_list.append(la)
    #
    # newtxt.writelines(infolist)
    # newtxt.close()
