import json
import os
import shutil

def read_json():
    info = open('D:/data/sample_catastici/via_catastici_annotated.json','r')
    info_list = json.load(info)
    info_list = info_list['_via_img_metadata']['9747f790-b7cd-42b8-a608-bdabe86c52b4-000094.jpg873173']

    # print(info_list)
    info_list = info_list['regions']

    for i in info_list:
        info = i['shape_attributes']
        # print(info)
        ss = (i['region_attributes']['lines'], info['all_points_x'] + info['all_points_y'])
        print(ss)

    # for name in info_list:
    #     print(name, info_list[name])
    #     print(type(info_list[name]))
    # for name0 in info_list['_via_img_metadata']:
    #     info = info_list['_via_img_metadata'][name0]
    #     for i in info['9747f790-b7cd-42b8-a608-bdabe86c52b4-000094.jpg873173']:
    #         print(i)
    # print(info_list)


def mov_det_img():
    infoList = open('E:/Pytorch/PaddleOCR-release-2.2/output/det_db/predicts_db.txt').readlines()
    for info in infoList:
        img_path = info.split('\t')[0]
        m = len(eval(info.split('\t')[1]))


        if m<2:
            new_path = img_path.replace('wcl', str(1))
        elif m < 6 :
            new_path = img_path.replace('wcl',str(5))
        elif m > 20:
            new_path = img_path.replace('wcl', str(20))
        elif m > 15:
            new_path = img_path.replace('wcl', str(15))
        else:
            new_path = img_path.replace('wcl', str(m))

        path = new_path[:36]
        if not os.path.exists(path):
            # print(new_path , path)
            os.makedirs(path)

        try:
            shutil.move(img_path,new_path)
        except:
            print(img_path)







if __name__ =='__main__':
    # read_json()
    # mov_det_img()

    path = 'E:/er_data/'
    img_lsit = os.listdir(path)
    for name in img_lsit:
        if os.path.exists('E:/reksall/'+name):
            shutil.move('E:/reksall/' + name, 'E:/reksall_er/' + name)
            print(name)
