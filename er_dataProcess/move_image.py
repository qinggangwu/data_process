from PIL import Image
import os


def move_img(in_path, out_path):
    n = 0   #设置索引值
    filename = os.listdir(in_path)
    print(len(filename))
    for name in filename:
        ims = Image.open(in_path + name)
        namelist = name.split("_")
        # namelist[1] = "V"
        namelist[2] = '0' * (4 - len(str(n))) + str(n) + '.png'
        n +=1
        name = "_".join(namelist)

        ims.save(out_path+name)
        print('正在移动图片{}'.format(name))





if __name__ == '__main__':

    in_path ='E:/BaiduNetdiskDownload/wu14CC/整理好数据/ABCDXV/V/'
    out_path = 'E:/BaiduNetdiskDownload/wu14CC/整理好数据/ABCDXV/ss/V/'

    # filename = os.listdir('E:\BaiduNetdiskDownload\wu14CC\images_re\wu_V_new/')
    # print(filename)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    move_img(in_path,out_path)
