
from matplotlib import pyplot as plt

def pol_txt(path,txt_name):
    info = open(path+txt_name)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    test_loss = []
    accuray = []
    for line in info.readlines():
        if 'Test loss' in line:
            basi_list = line.split(':')
            try:
                test_loss.append(float(basi_list[1][1:7]))
                accuray.append(float(basi_list[2][1:7]))
            except:
                pass
            # print(line,basi_list[1][1:7],basi_list[2][1:7])
    print('best accuray: {} '.format(max(accuray)), 'best Test loss: {} '.format(min(test_loss)),'mean Test loss: {}'.format(round(sum(test_loss)/len(test_loss), 4)))
    x = [i for i in range(len(accuray))]
    print(test_loss)
    print(accuray)
    name = txt_name.split('.')[0]
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Epoch ')
    ax1.set_ylabel('test loss', color=color)
    ax1.plot(x, test_loss, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # 创建共用x轴的第二个y轴
    color = 'tab:blue'
    ax2.set_ylabel('accuray', color=color)
    ax2.plot(x,accuray, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('训练时间'+name)
    plt.show()


def plt_unet(path,txt_name):
    info = open(path + txt_name)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    train_loss = []
    for line in info.readlines():
        if 'epoch' in line:
            basi_list = line.split(':')
            train_loss.append(float(basi_list[1]))

            # print(basi_list[1])
    print('best train loss: {} '.format(min(train_loss)))
    x = [i for i in range(len(train_loss))]
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Epoch ')
    ax1.set_ylabel('test loss', color='red')
    ax1.plot(x, train_loss, color='red')


    plt.title('训练时间' + txt_name)
    plt.show()


if __name__ == '__main__':
    path = '..\CRNN_Chinese_Characters_Rec-stable\output\OWN\crnn/txt/'
    path_unet = '../u_net_liver-master/log/'

    txt_name = '2021.txt'


    # plt_unet(path_unet,txt_name)
    pol_txt(path,txt_name)
# print(len('0123456789,.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-'))