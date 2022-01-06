import numpy as np
import torch

import math
np.set_printoptions(suppress=True)

def softmax(x, axis=1):
    # 计算每行的最大值
    row_max = x.max(axis=axis)

    # 每行元素都需要减去对应的最大值，否则求exp(x)会溢出，导致inf情况
    row_max = row_max.reshape(-1, 1)
    x = x - row_max

    # 计算e的指数次幂
    x_exp = np.exp(x)
    x_sum = np.sum(x_exp, axis=axis, keepdims=True)
    s = x_exp / x_sum
    return s


def fun(str_num):
    before_e = float(str_num.split('e')[0])
    sign = str_num.split('e')[1][:1]
    after_e = int(str_num.split('e')[1][1:])
    # if after_e >20 :
    #     return 0
    if sign == '+':
        float_num = before_e * math.pow(10, after_e)
    elif sign == '-':
        float_num = before_e * math.pow(10, -after_e)
    else:
        float_num = None
        print('error: unknown sign')
    return float_num


if __name__ == "__main__":

    info = open('E:/vcporject/openMat/img.txt').readlines()
    info = [lines.split() for lines in info]
    info_arrye = np.array(info, dtype=str)
    for i,lineinfo in enumerate(info_arrye):
        for j ,ss in enumerate(info_arrye[i]):
            if ss == '-nan':
                info_arrye[i][j] = 0
            else:
                try:
                    info_arrye[i][j] = fun(ss)
                except:
                    info_arrye[i][j] = float(ss)
    info_arrye = np.array(info_arrye, dtype=float)
    info_arrye = np.expand_dims(info_arrye, axis=0)
    x_tensor = torch.tensor(info_arrye, requires_grad=True)
    soft_tensor = torch.nn.functional.softmax(x_tensor, dim=1 )
    array_tensor = soft_tensor.detach().numpy()



    array_tensor = array_tensor.squeeze()



    print('end');quit()
    # info_fc = softmax(info_arrye,axis=1)
    #
