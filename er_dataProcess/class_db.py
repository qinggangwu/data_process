import pymysql
import time
import requests
import os
import urllib.request

class db():
    # 构造函数
    def __init__(self, hostnum=0):
        hosts = [['192.168.0.123', 'db_001', 'db_001', 'db_001']]
        # hosts = [['127.0.0.1', 'root', '123123', 'test']]

        self.conn = pymysql.connect(host=hosts[hostnum][0], user=hosts[hostnum][1], password=hosts[hostnum][2], port=3306, database=hosts[hostnum][3], charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query(self, sql, data=None):
        self.cursor.execute(sql, data)
        self.conn.commit()

    def selectOne(self, sql):
        re = self.select(sql)
        if len(re) == 0: return {}
        return re[0]

    def select(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def insert(self, table, data_dict, return_insert_id=0):
        self.query("insert into " + table + "(" + ",".join(data_dict) + ") values(" + ("%s,"*len(data_dict)).rstrip(',') + ")", tuple(data_dict.values()))
        if return_insert_id: return self.cursor.lastrowid

    # 析构函数
    def __del__(self):
        self.cursor.close()
        self.conn.close()



def download_img(save_paht,image_name,image_url):
    try:
        if not os.path.exists(save_paht):
            os.makedirs(save_paht)  # 如果没有这个path则直接创建
        filename = '{}{}'.format(save_paht, image_name)
        urllib.request.urlretrieve(image_url, filename=filename)  # 利用urllib.request.urltrieve方法下载图片
        print('正在保存图片：', image_name)
    except IOError as e:
        print(1, e)

    except Exception as e:
        print(2, e)



def selecto(index):
    db1 = db()
    re = db1.select('select id,image,ocr_info from a_kousuan_pigai  Where id > {} order by id asc limit 10000' .format(1300000+index))

    # re = db1.select('select id,image,ocr_info from a_kousuan_pigai limit {},{}'.format(index-1,n))

    return re

def selectofs(i):
    db1 = db()
    re = db1.select('select id,image,ocr_info from a_kousuan_pigai where frac_count>6 limit {},{}'.format(1000*(i-1),1000*i))
    # re = db1.select('select id,image,ocr_info from a_kousuan_pigai where frac_count>6 limit {},{}'.format(10*(i-1),10*i))

    # re = db1.select('select id,image,ocr_info from a_kousuan_pigai limit {},{}'.format(index-1,n))

    return re



if __name__ == '__main__':
    db1 = db()
    # re = db1.select('select * from pre_m_check_homework limit 10')

    # re = db1.select('select id,image,ocr_info  from a_kousuan_pigai where frac_count>6 limit 0,1000')
    re = db1.select('select id,image  from a_kousuan_pigai where frac_count>6 limit 10000,5000')
    # print(re[:10])
#     # http://user.1010pic.com/
#     print(re)



    # 下载图片
    for info in re:
        image_name = str(info['id']) + '.jpg'
        url = 'http://192.168.0.123/image/decode?url=' + info['image']
        file_path = 'E:/BaiduNetdiskDownload/fs_orgiamge/'
        # print(url)

        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)  # 如果没有这个path则直接创建
            filename = '{}{}'.format(file_path, image_name)
            urllib.request.urlretrieve(url, filename=filename)   #利用urllib.request.urltrieve方法下载图片
            print('正在保存图片：', image_name)
        except IOError as e:
            print(1, e)
        except Exception as e:
            print(2, e)



