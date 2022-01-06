# -*- coding: utf-8 -*-

from xml.dom.minidom import parse
import cv2
import os


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
                # print(img_out_path0+out_img_name)
                # cv2.imwrite(img_out_path0+out_img_name , out_img)
                cv2.imencode('.jpg', out_img)[1].tofile(img_out_path0+out_img_name)   # 保存文件名里面有中文
            except:
                pass
            print('正在切割:  {}'.format(im_name))
            num+=1
    print(num)


if __name__ == '__main__':
    xml_path = 'D:/data/orgimage/Chinese_orgiamge/xml2/'
    img_path = 'D:/data/orgimage/Chinese_orgiamge/img/'
    img_out_path = 'D:/train_data/wu14CC/Chinese_data2/'

    # n = 50000           #50000  3337
    n = 27602          #  27601
    num = 0
    qg_xml_img(xml_path, img_path,img_out_path, n)


