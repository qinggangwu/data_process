from PIL import Image
import os
import random
imgname = 0



def pingjie(imgs):
    # print('------------pingjie-------------')
    target = Image.new('RGB', (size[0] * len(imgs), size[1]))  # 拼接前需要写拼接完成后的图片大小 1200*600
    for i in range(len(imgs)):
        a = size[0] * i  # 图片距离左边的大小
        b = 0  # 图片距离上边的大小
        c = size[0] * (i + 1)  # 图片距离左边的大小 + 图片自身宽度
        d = size[0]  # 图片距离上边的大小 + 图片自身高度
        target.paste(imgs[i], (a, b, a + imgs[i].width, b + imgs[i].height))
        global imgname
        # print('拼接图片的路径为：', path1 + str(imgname) + '.jpg')
        imgname += 1
    name = ''
    for i in index:
        name += str(i)

    name_re ='hsf_{}_{}.png'.format(name,random.randint(0,99999))
    target.save(path1 + name_re)



for i in range(100):
    path1 = 'E:/BaiduNetdiskDownload/wu14CC/images_re/wu_ran_n/'  # 拼接后图片的存放目录
    # index = 'hsf_0_00000'  # 图片的名字
    # for i in range(1):  # 有两行，所以需要循环两次
    im_path = []
    images = []
    index = [random.randint(1,9),random.randint(0,9),random.randint(0,9),random.randint(0,9)]
    for i in index:
        path = 'E:/BaiduNetdiskDownload/wu14CC/images_re/wu_{}/'.format(i)
        for root, dirs, files in os.walk(path):
            L= files[random.randint(0, len(files))]
        im_path.append(path+L)

    IM = Image.open(im_path[0])
    size = IM.size  # 以随机图片的第一张width为尺寸
    for i in range(len(im_path)):
        images.append(Image.open(im_path[i]).resize(size))
    pingjie(images)

# if __name__ == '__main__':
#     for i in range(100):
#         index()






















# def pingjie(imgs):
#     # print('------------pingjie-------------')
#     target = Image.new('RGB', (size[0] * 4, size[1] * 1))  # 拼接前需要写拼接完成后的图片大小 1200*600
#     for i in range(len(imgs)):
#         a = size[0] * i  # 图片距离左边的大小
#         b = 0  # 图片距离上边的大小
#         c = size[0] * (i + 1)  # 图片距离左边的大小 + 图片自身宽度
#         d = size[0]  # 图片距离上边的大小 + 图片自身高度
#         # target.paste(imgs[i], (a, b, c, d))
#         target.paste(imgs[i], (a, b, a + imgs[i].width, b + imgs[i].height))
#
#         global imgname
#         print('拼接图片的路径为：', path1 + str(imgname) + '.jpg')
#         target.save(path1 + str(imgname) + '.jpg')
#         imgname += 1
#
#
# def pj():
#     # print('------------pj-------------')
#     # 取1,3是因为每行拼接完整都是最后那个，第一行是0，1命名，第二行是2,3命名，所以取后面那个值
#     imglist = [1, 3]
#     img = []
#     for i in imglist:
#         print('完整行的拼接路径为：' + path1 + str(i) + '.jpg')
#         img.append(Image.open(path1 + str(i) + '.jpg'))
#     target = Image.new('RGB', (size[0] * 2, size[1] ))  # 拼接前需要写拼接完成后的图片大小 1200*1200
#     for i in range(len(img)):
#         a = 0  # 图片距离左边的大小
#         b = size[0] * i  # 图片距离上边的大小
#         c = size[0] * 2  # 图片距离左边的大小 + 图片自身宽度
#         d = size[0] * (i + 1)  # 图片距离上边的大小 + 图片自身高度
#         target.paste(img[i], (a, b, a + img[i].width, b + img[i].height))
#         global imgname
#         target.save(path1 + 'pingjie' + '.jpg')
#
#
# if __name__ == '__main__':
#     # size = 600  # 图片的宽高都为600像素
#     # path = 'G:/img/img1/'  # 存放要拼接图片的目录
#     path = 'E:/BaiduNetdiskDownload/wu14CC/images_re/wu_1/'
#     path1 = 'E:/BaiduNetdiskDownload/wu14CC/images_re/wu_ran_num/'  # 拼接后图片的存放目录
#     # index = 'hsf_0_00000'  # 图片的名字
#     for i in range(1):  # 有两行，所以需要循环两次
#         images = []  # 每一次拼接只能一行一行拼接，不能在第一行拼接完后再在其基础上拼接第二行的图片，矩阵不允许这样操作
#         for j in range(2):  # 每行有两张图片，所以也要循环两次
#             for root, dirs, files in os.walk(path):
#                 L= [files[random.randint(0, len(files))], files[random.randint(0, len(files))]]
#                 for index in L:
#
#                     print(path + str(index))
#                     IM = Image.open(path + str(L[0]))
#                     size = IM.size  # 以随机图片的第一张width为尺寸
#                     images.append(Image.open(path + str(index)))
#             # index += 1
#         print('第 {} 行拼接完成'.format(i))
#         pingjie(images)
#     pj()