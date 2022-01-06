import os
import shutil
from xml.dom.minidom import parse

def move_img(jsonpath, moveimg_path,img_path):
    file_list = os.listdir(jsonpath)
    for name in file_list:
        imgname = name.replace('.json','.jpg')
        imgre_path =os.path.join(img_path,imgname)
        print('正在复制： {}'.format(imgname))
        shutil.copy(imgre_path,moveimg_path )

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

def  save_txt(info,sava_path):
    f = open(sava_path,'w',encoding = 'utf-8')
    txt_info = []
    for i in info:
        fo = [i[1],i[2],i[3],i[2],i[3],i[4],i[1],i[4],i[0]]
        # fo = [i[1],i[2],i[3],i[4],i[0]]

        fo =''.join(str([int(x) for x in fo[:-1]])[1:-1].split()) + ','+i[0] +'\n'
        # print(fo, type(fo))
        # fo = str([eval(x) for x in fo])[1:-1] + '\n'

        txt_info.append(fo)
    f.writelines(txt_info)
    f.close()

def make_train_val_txt(txt_path,img_path):
    # fw = open(r'D:\py\pytorch\DBNet-wu\datasets\wutrain.txt','w')
    # ft = open(r'D:\py\pytorch\DBNet-wu\datasets\wutest.txt','w')
    fw = open(r'E:/Pytorch/PaddleOCR-release-2.2/train_data/chdet_train.txt','w',encoding = 'utf-8')
    ft = open(r'E:/Pytorch/PaddleOCR-release-2.2/train_data/chdet_test.txt','w',encoding = 'utf-8')
    # txt_list =  os.listdir(txt_path)
    txt_list = open(txt_path ,'r',encoding= 'utf-8').readlines()
    info = []
    test_info = []
    for name0 in txt_list:
        name = name0.split()[0]
        img_name = name.replace('txt','png')
        imgpa = os.path.join(img_path,img_name)
        txtpa = os.path.join(txt_path,name)
        fo = imgpa+'\t'+txtpa+'\n'
        fo = 'D:/train_data/handwriting_rec/orimg/'+ name0

        if len(name)<= 10:
            if int(name[:6]) %11 ==0 :
                test_info.append(fo)
            else:
                info.append(name0)
        else:
            name2 = name.split('_')
            if int(name2[1][:6]) %5 ==0 :
                test_info.append(fo)
            else:
                info.append(name0)

    fw.writelines(info)
    ft.writelines(test_info)
    fw.close()
    ft.close()

def make_txt(xml_path ,txt_path):
    xml_list = os.listdir(xml_path)
    for name in xml_list:
        txt_name = name.replace('xml','txt')
        xml_name = os.path.join(xml_path,name)
        try:
            info = readXML(xml_name)
        except:
            print(xml_name)
        txtsave_path = os.path.join(txt_path,txt_name)
        save_txt(info,txtsave_path)
    print('xml转化txt完成')


def move_xml_img(txt_path,or_img, save_img):
    file_list = os.listdir(txt_path)
    for filename in file_list:
        imgname = filename.replace('txt','jpg')
        imgpath = os.path.join(save_img,imgname)
        if not os.path.exists(imgpath):
            shutil.copy(os.path.join(or_img,imgname),imgpath)
            print("正在移动图片： {}".format(imgname))



if __name__== '__main__':
    jsonpath = 'D:\Backup\桌面\data\json9.27/'
    moveimg_path = 'D:/train_data\yemian_fenxi\img/'
    img_path = 'D:\data\orgimage\Chinese_orgiamge\ycl/'
    xml_path = 'D:/train_data/handwriting_rec/xml1210_2/'

    txt_all_label = 'E:/Pytorch/PaddleOCR-release-2.2/train_data/train_ch_det_label.txt'
    txt_path = 'D:/train_data/handwriting_rec/txt1210/'
    js2txt_path = 'D:/train_data/rec/txt/'
    or_img = 'D:/data/orgimage/Chinese_orgiamge/wclall/'
    save_path = 'D:/train_data/handwriting_rec/orimg/'

    # make_txt(xml_path,txt_path)   #  xml转化成txt文档
    # move_img(jsonpath,moveimg_path,img_path)
    make_train_val_txt(txt_all_label,img_path)   #通过txt文件夹完成训练和测试文档，文件名可以被5整除的的作为val
    # move_xml_img(txt_path,or_img,save_path)