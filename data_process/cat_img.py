# import cv2
#
#
#
# img = cv2.imread('./pic/20210821142513.png')
# # img = cv2.imread('./pic/1629521418(1).jpg')
#
# # x0,y0 = 10,0
# #
# # w0,h0 = 92,36.5
# # print(img.shape)
# # h,w ,_ = img.shape
# # img = cv2.resize(img,(110,int(110/w *h)))
# # H,w,_ = img.shape
# # for i in range(int((H-y0) /h0 )+1):
# #     cv2.rectangle(img, ( x0,  int(y0)), (x0 + w0,  int(y0 + h0)), (253, 253, 0), 1)
# #     y0 += h0
# # cv2.rectangle(img, ( x0,  int(y0)), (x0 + w0,  int(y0 + h0)), (253, 253, 0), 1)
#
#
#
# h,w,_ = img.shape
# x0,y0 = 40,66
# w0 ,h0 = 60,920
# wt,ht = 0,22
# for i in range(int(h0/ht)+1):
#     cv2.rectangle(img, (x0, int(y0)), (x0 + w0, int(y0 + ht)), (253, 253, 0), 1)
#     cat_img = img[int(y0) :int(y0 + ht), x0: (x0 + w0)]  # 裁剪坐标为[y0:y1, x0:x1]
#     path = './pic/re/wu_{}.png'.format(i)
#     cv2.imwrite(path,cat_img)
#     y0 = int(y0 + ht)
#
#
#
# # cv2.waitKey(0)
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from PIL import Image, ImageDraw


# def bianyuan():
#     import cv2
#     import numpy as np
#
#     vc = cv2.VideoCapture(0)
#
#     while True:
#         ret, img = vc.read()
#
#         start = time.time()
#         source = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#         # sobel_x:发现垂直边缘
#         sobel_x = cv2.Sobel(source, cv2.CV_64F, 1, 0)
#         # sobel_y:发现水平边缘
#         sobel_y = cv2.Sobel(source, cv2.CV_64F, 0, 1)
#
#         sobel_x = np.uint8(np.absolute(sobel_x))
#         sobel_y = np.uint8(np.absolute(sobel_y))
#         np.set_printoptions(threshold=np.inf)
#         sobelCombined = cv2.bitwise_or(sobel_x, sobel_y)  # 按位或
#
#         # sum = sobel_x + sobel_y
#
#         # cv2.imshow('sobel_combined', sobelCombined)
#         sobelCombined = cv2.cvtColor(sobelCombined, cv2.COLOR_GRAY2BGR)
#         sobelCombined = cv2.bitwise_and(sobelCombined, img)  # 按位或
#         print(time.time() - start, '2')
#         cv2.imshow('aaa', sobelCombined)
#         cv2.waitKey(1)




def find_chessboard(img, size=(2,2), corner=4):
    import numpy as np
    import cv2

    # original_image = cv2.imread("1.png")
    image = img.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)

    # Find contours in the image
    cnts = cv2.findContours(canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Obtain area for each contour
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in cnts]

    # Find maximum contour and crop for ROI section
    if len(contour_sizes) > 0:
        largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        ROI = img[y:y + h, x:x + w]
        cv2.imshow("ROI", ROI)

    # cv2.imshow("canny", canny)
    # cv2.imshow("detected", image)
    # cv2.waitKey(0)

    cv2.imwrite('test.jpg',ROI)
    cv2.imwrite('test2.jpg',canny)

class Rotate(object):

    def __init__(self, image: Image.Image, coordinate):
        self.image = image.convert('RGB')
        self.coordinate = coordinate
        self.xy = [tuple(self.coordinate[k]) for k in ['left_top', 'right_top', 'right_bottom', 'left_bottom']]
        self._mask = None
        self.image.putalpha(self.mask)

    @property
    def mask(self):
        if not self._mask:
            mask = Image.new('L', self.image.size, 0)
            draw = ImageDraw.Draw(mask, 'L')
            draw.polygon(self.xy, fill=255)
            self._mask = mask
        return self._mask

    def run(self):
        image = self.rotation_angle()
        box = image.getbbox()
        return image.crop(box)

    def rotation_angle(self):
        x1, y1 = self.xy[0]
        x2, y2 = self.xy[1]
        angle = self.angle([x1, y1, x2, y2], [0, 0, 10, 0]) * -1
        return self.image.rotate(angle, expand=True)

    def angle(self, v1, v2):
        dx1 = v1[2] - v1[0]
        dy1 = v1[3] - v1[1]
        dx2 = v2[2] - v2[0]
        dy2 = v2[3] - v2[1]
        angle1 = math.atan2(dy1, dx1)
        angle1 = int(angle1 * 180 / math.pi)
        angle2 = math.atan2(dy2, dx2)
        angle2 = int(angle2 * 180 / math.pi)
        if angle1 * angle2 >= 0:
            included_angle = abs(angle1 - angle2)
        else:
            included_angle = abs(angle1) + abs(angle2)
            if included_angle > 180:
                included_angle = 360 - included_angle
        return included_angle


if __name__ == '__main__':
    path = 'E:/WeChat Files/wu331376411/WeChat Files/wu331376411/FileStorage/File/2021-09/789/时代 七上数学/时代数学2021七上 (1).jpg'

    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    find_chessboard(image)
  #   coordinate = {'left_top': [179, 151], 'right_top': [975, 155], 'right_bottom': [177, 1300], 'left_bottom': [978, 1300]}
  #   rotate = Rotate(image, coordinate)
  #   rotate.run().convert('RGB').save('./1.jpg')
  # # 318,