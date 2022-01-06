import numpy as np
import base64
import json
import os
import os.path as osp
import cv2
import imgviz
from labelme.logger import logger
from labelme import utils
import PIL.Image
import matplotlib.pyplot as plt
import argparse


def read_josn(path):
    with open(path) as f:
        json_info = json.load(f)
        info = json_info["shapes"][0]
    return (info['label'],info['points'])

def __is_point_in_polygon(pointTp, verts):
    """
    - PNPoly算法:判断点是否在不规则区域内（在边界线上也算）
    """
    # is_contains_edge=True
    x, y = pointTp[0], pointTp[1]
    try:
        x, y = float(x), float(y)
    except:
        return False
    vertx = [xyvert[0] for xyvert in verts]
    verty = [xyvert[1] for xyvert in verts]

    # N个点中，横坐标和纵坐标的最大值和最小值，判断目标坐标点是否在这个外包四边形之内
    if not verts or not min(vertx) <= x <= max(vertx) or not min(verty) <= y <= max(verty):
        return False

    # 上一步通过后，核心算法部分
    nvert = len(verts)
    is_in = False
    for i in range(nvert):
        j = nvert - 1 if i == 0 else i - 1
        if __is_in_line((x, y), verts[j], verts[i]):
            return True
        if ((verty[i] > y) != (verty[j] > y)) and (
                x < (vertx[j] - vertx[i]) * (y - verty[i]) / (verty[j] - verty[i]) + vertx[i]):
            is_in = not is_in

    return is_in

def mark_image(img_path,info):

    label = info[0]
    des = info[1]
    img = cv2.imread(img_path)
    imgmark = np.zeros(img.shape, dtype=np.uint8)
    imgmark = cv2.cvtColor(imgmark, cv2.COLOR_BGR2GRAY)
    # print(imgmark)
    h,w = imgmark.shape
    for i in range(h):
        for j in range(w):
            if __is_point_in_polygon((i,j),des):
                # pass
                imgmark[i,j] = 255

    cv2.imshow('mark',imgmark)
    cv2.waitKey(0)
    # print(imgmark.shape)



def change_one_json(json_file, output_file):
    # logger.warning('This script is aimed to demonstrate how to convert the '
    #                'JSON file to a single image dataset.')
    # logger.warning("It won't handle multiple JSON files to generate a "
    #                "real-use dataset.")
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('json_file')
    # parser.add_argument('-o', '--out', default=None)
    # args = parser.parse_args()

    # json_file = args.json_file

    if output_file is None:
        out_dir = osp.basename(json_file).replace('.', '_')
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = output_file.replace(".jpg", '')
    # if not osp.exists(out_dir):
    #     os.mkdir(out_dir)

    if os.path.exists(out_dir+'_label.png'):
        return

    data = json.load(open('D:\Backup\桌面\data\json9.27/' + json_file))
    imageData = data.get('imageData')

    if not imageData:
        imagePath0 = os.path.join(os.path.dirname(json_file), data['imagePath'])
        imagePath = 'D:/train_data/yemian_fenxi/img/' +imagePath0.split('\\')[-1]
        with open(imagePath, 'rb') as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode('utf-8')
    img = utils.img_b64_to_arr(imageData)

    label_name_to_value = {'_background_': 0, 'book': 255, 'stair':0, 'corrider':2, 'gate':0,'rubblish':3}
    # label_name_to_value = {'_background_': (0,0,0), 'book': (255,0,0) }
    for shape in sorted(data['shapes'], key=lambda x: x['label']):
        label_name = shape['label']
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl, _ = utils.shapes_to_label(
        img.shape, data['shapes'], label_name_to_value
    )

    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name

    lbl_viz = imgviz.label2rgb(
        label=lbl, img=imgviz.asgray(img), label_names=label_names, loc='rb'
    )

    # PIL.Image.fromarray(img).save(osp.join(out_dir, 'img.png'))
    # utils.lblsave(osp.join(out_dir, 'label.png'), lbl)
    # PIL.Image.fromarray(img).save(out_dir.replace('gt', 'img') + '_img.png')
    # utils.lblsave(out_dir + '_label.png', lbl)
    lbl =lbl.tolist()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # a =lbl[i][j]
            # print(a)
            if lbl[i][j] == 0:
                lbl[i][j] = (0, 0 ,0)
            else:
                lbl[i][j] = (0, 0, 255)

    cv2.imwrite(out_dir + '_label.png', np.array(lbl))
    # PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))

    # with open(out_dir.replace('gt', 'label_names') + '_label_names.txt', 'w',encoding='utf-8') as f:
    #     print(len(label_names))
    #     for lbl_name in label_names:
    #         # print(type(lbl_name),lbl_name)
    #         try:
    #             f.write(lbl_name + '\n')
    #         except:
    #             pass

    logger.info('Saved to: {}'.format(out_dir))

if __name__ == "__main__":
    import shutil
    json_list = os.listdir('D:\Backup\桌面\data\json9.27/')
    print('总josn数量为:  ',len(json_list))
    # create_list = ['transpic/gtpic/', 'transpic/img/', 'transpic/label_names/']
    # for item in create_list:
    #     if os.path.exists(item):
    #         shutil.rmtree(item)
    #     os.makedirs(item)
    for json_file in json_list:
        if json_file.endswith(".json"):
            output_file = 'D:/train_data/yemian_fenxi/mark2/' + json_file.replace('json', 'jpg')
            print(json_file, output_file)
            change_one_json(json_file, output_file)
