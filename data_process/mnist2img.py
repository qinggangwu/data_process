import os
from skimage import io
import torchvision.datasets.mnist as mnist
import cv2
import numpy



def convert_to_img(train=True):
    root = "D:/data/MNIST/raw/"

    train_set = (
        mnist.read_image_file(os.path.join(root, 'train-images-idx3-ubyte')),
        mnist.read_label_file(os.path.join(root, 'train-labels-idx1-ubyte'))
    )

    test_set = (
        mnist.read_image_file(os.path.join(root, 't10k-images-idx3-ubyte')),
        mnist.read_label_file(os.path.join(root, 't10k-labels-idx1-ubyte'))
    )

    print("train set:", train_set[0].size())
    print("test set:", test_set[0].size())

    if (train):
        f = open(root + 'train.txt', 'w')
        data_path = root + '/train/'
        if (not os.path.exists(data_path)):
            os.makedirs(data_path)
        for i, (img, label) in enumerate(zip(train_set[0], train_set[1])):

            int_label = str(label).replace('tensor(', '')
            int_label = int_label.replace(')', '')
            data_path_sa = os.path.join(data_path , str(int_label))
            if (not os.path.exists(data_path_sa)):
                os.makedirs(data_path_sa)

            img_path = os.path.join(data_path_sa ,'train_{}_{}.jpg'.format(int_label,i))
            io.imsave(img_path, img.numpy())
            f.write(img_path + ' ' + str(int_label) + '\n')
        f.close()
    else:
        f = open(root + 'test.txt', 'w')
        data_path = root + '/test/'
        if (not os.path.exists(data_path)):
            os.makedirs(data_path)
        for i, (img, label) in enumerate(zip(test_set[0], test_set[1])):

            int_label = str(label).replace('tensor(', '')
            int_label = int_label.replace(')', '')
            data_path_sa = os.path.join(data_path, str(int_label))
            if (not os.path.exists(data_path_sa)):
                os.makedirs(data_path_sa)

            img_path = os.path.join(data_path_sa, 'test_{}_{}.jpg'.format(int_label, i))
            io.imsave(img_path, img.numpy())

            f.write(img_path + ' ' + str(int_label) + '\n')
        f.close()

def qiegebiankuang(img):
    h,w = img.shape
    xi,yi,xa,ya = w,h,0,0
    for i in range(h):
        for j in range(w):
            if img[i][j] != 255 :
                ya = i
                if i < yi:
                    yi = i
    for i in range(w):
        for j in range(h):
            if img[j][i] != 255 :
                xa = i
                if i < xi :
                    xi = i
    # print(xi,yi,xa,ya)
    # return img[yi: ya, xi:xa]
    # return cv2.resize(img[(yi) : (ya+2) ,(xi) :(xa +2)] ,dsize=None,fx=2.0,fy=2.0)

    if yi >1 and xi > 1:
        imgcat = img[(yi-2) : (ya+2) ,(xi-2) :(xa +2)]
    elif xi >1:
        imgcat = img[(yi): (ya + 2), (xi - 2):(xa + 2)]
    elif yi >1:
        imgcat = img[(yi-2 ): (ya + 2), xi:(xa + 2)]
    else:
        imgcat = img[yi: (ya + 2), xi:(xa + 2)]

    imgcat = cv2.resize(imgcat,dsize=None,fx=2.0,fy=2.0)

    return imgcat

def img_resize(img_name):

    save_path = 'D:/data/MNIST/raw/resize/no_biankuang/'
    img = cv2.imread(img_name)
    height, width, temp = img.shape
    img2 = img.copy()

    for i in range(height):
        for j in range(width):
            img2[i, j] = (255 - img[i, j][0], 255 - img[i, j][1], 255 - img[i, j][2])

    img_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img_mean = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 15, 13)

    img_mean = qiegebiankuang(img_mean)

    # img_save = cv2.resize(img_mean,dsize=(104,64))

    # img_save = cv2.resize(img2,dsize=(104,64))

    name = img_name.split("raw")[-1][6:]
    cv2.imwrite(save_path+name,img_mean)


    # cv2.imshow('test',img_save)
    #
    # cv2.waitKey(0)
    # return img2

    # print(img.shape)



if __name__ == "__main__":
    path = 'D:/data/MNIST/raw/resize/no_biankuang/1/'

    for name in os.listdir(path):
        ne = "wu" +name[5:]
        img = cv2.resize(cv2.imread(path+name) ,dsize=(104,64))
        cv2.imwrite('D:/data/MNIST/raw/resize/no_biankuang/re/'+ne,img)
        # img_resize(path+name)
    # convert_to_img(True)
    # convert_to_img(False)