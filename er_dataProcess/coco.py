import coco_text
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
from PIL import Image
import pylab
import math
import traceback
import os
import html

pylab.rcParams['figure.figsize'] = (10.0, 8.0)

dataDir = 'E:\dataset\COCO'
dataType = 'train2014'

ct = coco_text.COCO_Text('../cocotext.v2.json')
ct.info()
imgIds = ct.getImgIds(imgIds=ct.train, catIds=[('legibility', 'legible')])
# return
# img = ct.loadImgs(imgIds[np.random.randint(0,len(imgIds))])[0]
# print("???",'%s/%s/%s'%(dataDir,dataType,img['file_name']))
# I = io.imread('%s/%s/%s'%(dataDir,dataType,img['file_name']))
# print(I.shape)
# print ('/%s/%s'%(dataType,img['file_name']))
# plt.figure()
f = open("./COCO-TEXT/gt_train.txt", "w", encoding="utf-8")

print("???", len(imgIds))
# os._exit(233)
cnt = 0
for idx in range(0, len(imgIds)):
    img = ct.loadImgs(imgIds[idx])[0]
    I = io.imread('%s/%s/%s' % (dataDir, dataType, img['file_name']))
    # plt.imshow(I)
    # plt.show()
    # os._exit("233")
    if idx % 100 == 0:
        print(idx, "/", len(imgIds))
    # print('%s/%s/%s'%(dataDir,dataType,img['file_name']),"___",I.shape,len(I.shape))
    annIds = ct.getAnnIds(imgIds=img['id'])
    anns = ct.loadAnns(annIds)
    # print("ANNS=",anns)
    # ct.showAnns(anns)
    for GT in anns:
        if "utf8_string" not in GT or GT["language"] != "english":
            continue
        # print("GT=",GT)
        # os._exit(233)
        label = GT["utf8_string"]
        label = label.strip()
        if label == "" or label == " ":
            continue
        label = html.unescape(label)
        bb = GT["bbox"]
        x = math.floor(bb[0])
        y = math.floor(bb[1])
        dx = math.ceil(bb[2])
        dy = math.ceil(bb[3])
        xx = x + dx
        yy = y + dy
        # print(xx,yy)
        if xx >= I.shape[1]:
            xx = I.shape[1] - 1
        if yy >= I.shape[0]:
            yy = I.shape[0] - 1
        if len(I.shape) == 2:
            croppedimg = I[y:yy, x:xx]
        else:
            croppedimg = I[y:yy, x:xx, :]
        # print(label)
        cnt += 1
        url = './COCO-TEXT/train/' + str(cnt) + ".jpg"
        gt_url = "./train/" + str(cnt) + ".jpg"
        try:
            io.imsave(url, croppedimg)
            f.write(url + " " + label + "\n")
        except Exception as ex:
            cnt -= 1
            # traceback.print_exc()
            print(ex)
        # plt.imshow(croppedimg)
        # plt.show()

f.close()