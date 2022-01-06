# coding=utf-8
# 导入相应的python包
import argparse
from skimage import io
import matplotlib.pyplot as plt
from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage.segmentation import mark_boundaries



# 超像素分析
# 设置并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# 读取图片并将其转化为浮点型
image = img_as_float(io.imread(args["image"]))

# 循环设置不同的超像素组
for numSegments in (100, 200, 300):
	# 应用slic算法并获取分割结果
	segments = slic(image, n_segments = numSegments, sigma = 5)

	# 绘制结果
	fig = plt.figure("Superpixels -- %d segments" % (numSegments))
	ax = fig.add_subplot(1, 1, 1)
	ax.imshow(mark_boundaries(image, segments))
	plt.axis("off")

# 显示结果
plt.show()