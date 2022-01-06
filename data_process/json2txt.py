import json
import os
import collections




def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, int) and not isinstance(el, float):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def js2txt(json_path, txt_savepath):
    jsom_list = os.listdir(json_path)
    for js in jsom_list[:5]:
        path = json_path +js
        # print(path)
        data = json.load(open(path),encoding = 'utf-8')
        imageData = data.get('shapes')[0]
        if imageData:
            box_info = imageData['points']
            box_info = flatten(box_info)

            box_info = [str(round(i,2)) for i in box_info]
            # print(box_info)
            box_info = ','.join(box_info)
            label = imageData['label']

        txt_path =txt_savepath+ js.replace('json','txt')
        info = box_info +','+label
        # print(type(info))
        fw = open(txt_path,'w')
        fw.writelines(info)
        fw.close()


def json2txt(json_path, txt_savepath):
    jsom_list = os.listdir(json_path)
    for js in jsom_list:
        path = json_path +js
        # print(path)
        data = json.load(open(path),encoding = 'utf-8')
        img_h = data['imageHeight']
        img_w = data['imageWidth']
        point1,point2,point3,point4 = data.get('shapes')[0]['points'],data.get('shapes')[1]['points'],data.get('shapes')[2]['points'],data.get('shapes')[3]['points']
        print(point1,point2,point3,point4)

        x1 = point1[0][0]/img_w
        y1 = point1[0][1]/img_h
        x2 = point2[0][0]/img_w
        y2 = point2[0][1]/img_h
        x3 = point3[0][0]/img_w
        y3 = point3[0][1]/img_h
        x4 = point4[0][0]/img_w
        y4 = point4[0][1]/img_h

        info = str(4) +'\n' +str(x1) +'\t' +str(y1) +'\t'+str(x2) +'\t' +str(y2) +'\t'+str(x3) +'\t' +str(y3) +'\t'+str(x4) +'\t' +str(y4)
        print(info)
        # if imageData:
        #     box_info = imageData['points']
        #     # box_info = flatten(box_info)
        #
        #     box_info = [str(round(i,2)) for i in box_info]
        #     # print(box_info)
        #     box_info = ','.join(box_info)
        #     label = imageData['label']
        #
        txt_path =txt_savepath+ js.replace('json','txt')
        # info = box_info +','+label
        # print(type(info))
        fw = open(txt_path,'w')
        fw.writelines(info)
        fw.close()





if __name__ == "__main__":
    json_path = 'D:\py\pytorch\SimpleCVReproduction-master\simple_keypoint\heatmap\data\json/'
    txt_savepath = 'D:\py\pytorch\SimpleCVReproduction-master\simple_keypoint\heatmap\data\labels/'
    json2txt(json_path,txt_savepath)
