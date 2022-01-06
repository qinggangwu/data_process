import cv2
import numpy as np
import random,os




# rows,cols,channels = img.shape  #rows，cols最后一定要是前景图片的，后面遍历图片需要用到


#转换hsv
# hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# for i in hsv:
#     for j in i:
#         print(j)
#
# lower_blue=np.array([0,0,0])
# upper_blue=np.array([0,0,110])
# mask = cv2.inRange(hsv, lower_blue, upper_blue)
# cv2.imshow('Mask', mask)
# cv2.waitKey(0)
#
# erode=cv2.erode(mask,None,iterations=1)
# cv2.imshow('erode',erode)
# dilate=cv2.dilate(erode,None,iterations=1)
# cv2.imshow('dilate',dilate)

def mix_bp(image,image_bp):
    X = random.randint(20, 70)
    x = 0
    y = 10
    rows, cols, channels = image.shape
    rows0, cols0, channels0 = image_bp.shape
    centerX = random.randint(1,cols0-40)  # 在新背景图片中的位置
    centerY = random.randint(1,rows0-40)
    pianyi = random.randint(20,40)
    # print(centerX,centerY,pianyi)

    image_bp = image_bp[centerY:centerY+pianyi, centerX:centerX+pianyi]
    image_bp = cv2.resize(image_bp,dsize=(cols,rows),dst=None)


    for i in range(rows):
        for j in range(cols):
            if np.sum(image[i,j])==0:   #0代表黑色的点
                image_bp[i,j]=[X+random.randint(x,y),X,X+random.randint(x,y)]#此处替换颜色，为BGR通道

    return image_bp



def main():
    img_Path = 'E:/BaiduNetdiskDownload/wu14CC/images_re/wu_V/'
    # img_name = random.choice(os.listdir(img_Path))
    im_save_path = 'E:/BaiduNetdiskDownload/wu14CC/images_re/made_image/wu_V_made/'

    bp_path = 'E:/BaiduNetdiskDownload/wu14CC/image_bp/'
    # bp_name = random.choice(os.listdir(bp_path))


    #随机读取图片
    for img_name in os.listdir(img_Path):
        bp_name = random.choice(os.listdir(bp_path))
        img=cv2.imread(img_Path+img_name)
        img_back =cv2.imread(bp_path+bp_name)
        img=cv2.resize(img,None,fx=0.6,fy=0.6)
        img_made = mix_bp(img,img_back)
        cv2.imwrite(im_save_path+img_name, img_made)
        print('正在保存图片：{}'.format(img_name))


# for i in range(2000):
if __name__ == '__main__':
    main()


# cv2.imshow('res',a)
# cv2.waitKey(0)