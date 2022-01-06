import torch
print(torch.__version__)               # torch 版本
print(torch.version.cuda)              # cuda版本
print(torch.backends.cudnn.version())  # cudnn 版本
# print(torch.version.cudnn)
print(torch.cuda.is_available())       # cuda是否可以用
print(torch.cuda.device_count())       # cuda 可用的数量

print(torch.cuda.get_device_name(0))   # 显卡型号
print(torch.cuda.current_device())     # 显卡的编号

