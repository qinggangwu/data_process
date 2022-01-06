

# txt_info = open('E:/Pytorch/PaddleOCR-release-2.2/train_data/info.txt')
# sum = 0
# q = 0
# for info in txt_info.readlines():
#     info = info.split('，')
#     if info[0][-3:] == 'png':
#         sum+=1
#         lable = info[0].split("_")[1]
#         reza = info[1][4:][:-1]
#         # print(lable, lable.lower(), reza, reza.lower())
#
#         if lable.lower() == reza.lower() :
#             print(lable,reza)
#             q+=1
#
#
#
#
# print(1- q/sum,sum,q)
#     # print(info)


# !/usr/bin/env python
# -*- coding:utf-8 -*-



import sys
from test  import Ui_ocr
from PyQt5.QtWidgets import *


class OCR(QMainWindow,Ui_ocr):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img_path = None
        self.txt_path = None
        self.flag = False

        self.setupUi(self)
        self.show()

        # 绑定信号与槽函数
        self.sel_imgfile.clicked.connect(self.select_img)
        self.sel_txtfile.clicked.connect(self.select_txt)
        self.run.clicked.connect(self.start)
        self.over.clicked.connect(self.end)

    def select_img(self):
        self.img_path = QFileDialog.getExistingDirectory(self, 'open file', '/')
        self.img_lineEdit.setText(self.img_path)

    def select_txt(self):
        self.txt_path = QFileDialog.getExistingDirectory(self, 'open file', '/')
        self.txt_lineEdit.setText(self.txt_path)

    def start(self):
        self.flag = True
        print(self.flag)

    def end(self):
        self.flag = False
        print(self.flag)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCR()
    window.show()
    sys.exit(app.exec_())


# import sys
# from PyQt5 import QtWidgets
#
# app = QtWidgets.QApplication(sys.argv)
# widget = QtWidgets.QWidget()
# widget.resize(360, 360)
# widget.setWindowTitle("ocr识别")
# widget.show()
# sys.exit(app.exec())