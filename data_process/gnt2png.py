import os
import numpy as np
import struct
from PIL import Image
import pickle
# data文件夹存放转换后的.png文件



def read_from_gnt_dir(gnt_dir='D:data/中文手写数据/字符样本数据/Gnt1.0TrainPart1/'):
    def one_file(f):
        header_size = 10
        while True:
            header = np.fromfile(f, dtype='uint8', count=header_size)
            if not header.size: break
            sample_size = header[0] + (header[1] << 8) + (header[2] << 16) + (header[3] << 24)
            tagcode = header[5] + (header[4] << 8)
            width = header[6] + (header[7] << 8)
            height = header[8] + (header[9] << 8)
            if header_size + width * height != sample_size:
                break
            image = np.fromfile(f, dtype='uint8', count=width * height).reshape((height, width))
            yield image, tagcode

    for file_name in os.listdir(gnt_dir):
        if file_name.endswith('.gnt'):
            file_path = os.path.join(gnt_dir, file_name)
            with open(file_path, 'rb') as f:
                for image, tagcode in one_file(f):
                    yield image, tagcode


def read_train(data_dir,train_data_dir, i):
    train_counter = 500000 *i
    for image, tagcode in read_from_gnt_dir(gnt_dir=train_data_dir):
        tagcode_unicode = struct.pack('>H', tagcode).decode('gb2312', 'ignore')
        im = Image.fromarray(image)
        # 路径为data文件夹下的子文件夹，train为存放训练集.png的文件夹
        # dir_name = data_dir + 'traina/' + '%0.5d' % char_dict[tagcode_unicode]
        lens = len(tagcode_unicode)

        # print(dir_name,len(str(tagcode_unicode[:lens-1])))
        # else:
        #     dir_name = data_dir + 'train_num/' + '%0.5d' % char_dict[tagcode_unicode]


        try:
            if lens > 1:
                dir_name = data_dir + 'train/' + str(tagcode_unicode[:lens - 1])
                filename = dir_name + '/wu_' + str(tagcode_unicode[:lens - 1]) + '_' + str(train_counter) + '.png'
            elif lens == 1:
                dir_name = data_dir + 'train/' + str(tagcode_unicode[0])
                filename = dir_name + '/wu_' + str(tagcode_unicode[0]) + '_' + str(train_counter) + '.png'
            else:
                dir_name = data_dir + 'train_num/' + '%0.5d' % char_dict[tagcode_unicode]
                filename = dir_name + '/' + 'wu_' + str(char_dict[tagcode_unicode]) + '_' + str(train_counter) + '.png'
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            print(filename)
            im.convert('RGB').save(filename)
        except:
            dir_name = data_dir + 'train_num/' + '%0.5d' % char_dict[tagcode_unicode]
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            print(dir_name + '/' + 'wu_' + str(char_dict[tagcode_unicode]) + '_' + str(train_counter) + '.png')
            im.convert('RGB').save(dir_name + '/' + 'wu_' + str(char_dict[tagcode_unicode]) + '_' + str(train_counter) + '.png')
        # print("train_counter=", train_counter)
        train_counter += 1
    print('Train transformation finished ...')


def read_test(data_dir,test_data_dir):
    test_counter = 0
    for image, tagcode in read_from_gnt_dir(gnt_dir=test_data_dir):
        tagcode_unicode = struct.pack('>H', tagcode).decode('gb2312', 'ignore')
        im = Image.fromarray(image)
        # 路径为data文件夹下的子文件夹，test为存放测试集.png的文件夹
        dir_name = data_dir + 'test/' + '%0.5d' % char_dict[tagcode_unicode]
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        im.convert('RGB').save(dir_name + '/' +'wu_'+str(tagcode_unicode)+'_'+ str(test_counter) + '.png')
        print("test_counter=", test_counter)
        test_counter += 1
    print('Test transformation finished ...')



if __name__ =="__main__":
    data_dir = 'D:/data/CASIA/'
    # 路径为存放数据集解压后的.gnt文件
    train_data_dir = 'D:data/中文手写数据/字符样本数据/'
    # train_data_dir0_1 = 'D:data/中文手写数据/字符样本数据/Gnt1.0TrainPart1/'
    # train_data_dir0_2 = 'D:data/中文手写数据/字符样本数据/Gnt1.0TrainPart2/'
    # train_data_dir0_3 = 'D:data/中文手写数据/字符样本数据/Gnt1.0TrainPart3/'
    # train_data_dir1_1 = 'D:data/中文手写数据/字符样本数据/Gnt1.1TrainPart1/'
    # train_data_dir1_2 = 'D:data/中文手写数据/字符样本数据/Gnt1.1TrainPart2/'
    # train_data_dir2_1 = 'D:data/中文手写数据/字符样本数据/Gnt1.2TrainPart1/'
    # train_data_dir2_2 = 'D:data/中文手写数据/字符样本数据/Gnt1.2TrainPart2/'

    test_data_dir = 'D:data/中文手写数据/字符样本数据/Gnt1.0Test/'

    char_set = set()
    for _, tagcode in read_from_gnt_dir(gnt_dir='D:data/中文手写数据/字符样本数据/Gnt1.2TrainPart1/'):
        tagcode_unicode = struct.pack('>H', tagcode).decode('gb2312', 'ignore')
        char_set.add(tagcode_unicode)
    char_list = list(char_set)
    char_dict = dict(zip(sorted(char_list), range(len(char_list))))
    print(len(char_dict))
    print("char_dict=", char_dict)

    f = open('char_dict', 'wb')
    pickle.dump(char_dict, f)
    f.close()

    # read_test(data_dir, test_data_dir)

    file_list =os.listdir(train_data_dir)
    i = 5
    for name in file_list:
        if ('TrainPart' in name)  and  ('zip' not in name):

            train_data_dir0 = os.path.join(train_data_dir ,name)
            # print(train_data_dir0)
            read_train(data_dir,train_data_dir0,i)
            i+=1


    # read_train(data_dir,train_data_dir0_2)
    # read_train(data_dir,train_data_dir0_3)
    # read_train(data_dir,train_data_dir1_1)
    # read_train(data_dir,train_data_dir1_2)
    # read_train(data_dir,train_data_dir2_1)
    # read_train(data_dir,train_data_dir2_2)
