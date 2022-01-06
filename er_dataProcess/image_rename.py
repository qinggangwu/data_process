import os
import shutil
import random



def re_name(path):   #去掉文件夹加路径里面的空格

    filename = os.listdir(path)

    n = 0
    for i in filename:
        # print(i)
        imgpath = path+i
        image_or_mane = imgpath
        # image_remane = ''.join(i.split(" "))
        image_remane = 'wu_'+ '0'*(5-len(str(n)))+str(n) +'.png'
        n +=1
        image_remane0 = path + image_remane
        # try:
        #     # if os.path.exists(image_remane0):
        #     #     shutil.move(image_or_mane, image_remane0+'_')
        #     # else:
        #     shutil.move(image_or_mane, image_remane0)
        # except:
        #     pass
        print("正在保存{}".format(image_remane))


def remo_file(n, inpath,outpath):
    filename = os.listdir(inpath)
    for name in filename:
        src = os.path.join(inpath, name)   #拼接 文件路径
        # outpath0 = os.path.join(outpath, '{}_num'.format(len(name)))

        # print(src,dst)
        try:
            if len(name) < n and (float(name) % 1 ==0 ):
                outpath0 = os.path.join(outpath, '{}_num'.format(len(name)))
                dst = os.path.join(outpath0, name)
                if not os.path.exists(outpath0):
                    os.makedirs(outpath0)

                shutil.move(src, dst)
            else:
                outpath0 = os.path.join(outpath, '{}_nn_num'.format(len(name)))
                dst = os.path.join(outpath0, name)
                if not os.path.exists(outpath0):
                    os.makedirs(outpath0)
                shutil.move(src, dst)


        except:
            pass

if __name__ == '__main__':
    path = 'E:/BaiduNetdiskDownload/segment_orgiamge/img/'     # 传入需要修改文件名称的路径
    # re_name(path)
    # remo_file(10,path,path)

    # filename = os.listdir(path)
    # list_name = []
    # imglen = len(filename)
    # for i in range(int(imglen *0.1)):
    #     num = random.randint(1,imglen)
    #     list_name.append(filename[num])
    # for name in list_name:
    #     imgpath = path + name
    #     shutil.copyfile(imgpath, path + 'sss/' + name)


    # filename = os.listdir(path)
    # #
    # list_name = []
    # del_list =[]
    # for i in filename:
    # #     print(i)
    #     imgpath = path + i
    #     s = "_".join(i.split("_")[1:3])
    #     if s not in list_name:
    #         list_name.append(s)
    #     else:
    #         del_list.append(i)
    #         shutil.move(imgpath, path +'ss/'+ i)
    # print(del_list)
    # print(len(del_list))


        # image_or_mane = imgpath
        # if i[-1] == '_':
        #     image_remane = i[:-1]
        # else:
        #     continue
    img_name = os.listdir(path)
    n = 0
    for i in img_name:
        image_or_mane = path +i
        image_remane = 'wu_'+ '0'*(4-len(str(n)))+str(n) +'.png'
        n +=1
        image_remane0 = path + image_remane
        try:
            # if os.path.exists(image_remane0):
            #     shutil.move(image_or_mane, image_remane0+'_')
            # else:
            shutil.move(image_or_mane, image_remane0)
        except:
            pass
        print("正在保存{}".format(image_remane))




    # imagename = os.listdir(imgpath)
    # for j in imagename[:3]:

        # image_or_mane = imgpath + '/'+j
        # image_remane = ''.join(j.split(" "))
        # image_remane = imgpath + '/'+image_remane
    # print(image_or_mane,image_remane)
        # shutil.move(image_or_mane, image_remane)


        # os.rename(image_or_mane,image_remane)



        # print(image_or_mane, image_remane)