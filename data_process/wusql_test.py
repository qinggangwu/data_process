# 引入pymysql包
import pymysql
import datetime
import random
import time


def write_sql():
    # 连接数据库并打开library数据库
    # print('开始建立连接')
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='test')
    print("数据库连接成功")
    # 获取游标对象
    cur = conn.cursor()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(dt[11:16]);quit()
    info = ['13:20','000020']
    info[0] = dt.replace(dt[11:16] , info[0])


    # for i in range(15):
    #     stat = time.time()
        # sql = '''insert into gp_info (time,gp,zf,xz,zl,zs,xl,xs) values ('%s','%s','%s','%s','%s','%s','%s','%s')''' % (
        # info[0], info[1], str(random.randint(1000,999999)), str(random.randint(1000,999999)),str(random.randint(1000,999999)), str(random.randint(1000,999999)), str(random.randint(1000,999999)), str(random.randint(1000,999999)))
        # print(sql)

        # into = "insert into gp_info (time,gp,zf,xz,zl,zs,xl,xs) values "
        # values = [(info[0], info[1], str(random.randint(1000,999999)), str(random.randint(1000,999999)),
        #            str(random.randint(1000,999999)), str(random.randint(1000,999999)), str(random.randint(1000,999999)), str(random.randint(1000,999999))) for i in range(15)]
        # print(str(values)[1:-1],type(eval(str(values)[1:-1])));quit()
    intotest = """ insert into gp_info (time,gpnum,zf,xj,zl,xl,zs,lb) values  ('2021-12-01 10:23:54', '000151', '0.65', '7.79', '6605', '36', '0.00', '1.29'), ('2021-12-01 10:23:54', '000153', '-2.15', '12.29', '50985', '22', '-0.23', '1.27'), ('2021-12-01 10:23:54', '000155', '-1.04', '29.49', '217763', '500', '-0.06', '1.37'), ('2021-12-01 10:23:54', '000156', '0.68', '7.37', '14316', '21', '0.14', '1.07'), ('2021-12-01 10:23:54', '000157', '1.29', '7.07', '216535', '15', '0.14', '2.20'), ('2021-12-01 10:23:54', '000158', '2.23', '7.33', '275304', '119', '0.55', '2.98'), ('2021-12-01 10:23:54', '000159', '-0.32', '6.27', '23858', '5', '0.16', '0.97'), ('2021-12-01 10:23:54', '000166', '1.19', '5.11', '315798', '639', '-0.19', '1.87'), ('2021-12-01 10:23:54', '000301', '2.79', '24.35', '315619', '18', '-0.68', '3.68'), ('2021-12-01 10:23:54', '000333', '0.18', '67.90', '67700', '151', '0.07', '1.55'), ('2021-12-01 10:23:54', '000338', '4.86', '16.18', '103.2w', '488', '0.37', '7.79'), ('2021-12-01 10:23:54', '000400', '0.52', '27.13', '233179', '123', '-0.25', '1.48'), ('2021-12-01 10:23:54', '000401', '-', '-', '0', '0', '-', '0.00'), ('2021-12-01 10:23:54', '000402', '1.09', '5.57', '45297', '1', '0.00', '1.60'), ('2021-12-01 10:23:54', '000403', '-0.69', '30.32', '8663', '6', '0.23', '1.53'), ('2021-12-01 10:23:54', '000404', '1.17', '4.34', '31227', '19', '0.46', '1.29'), ('2021-12-01 10:23:54', '000407', '0.72', '4.18', '20844', '20', '0.24', '1.00'), ('2021-12-01 10:23:54', '000408', '-2.04', '26.94', '45955', '1', '-0.21', '1.16'), ('2021-12-01 10:23:54', '000409', '0.38', '5.24', '20820', '2', '0.19', '1.83'), ('2021-12-01 10:23:54', '000410', '2.09', '4.88', '42484', '100', '-0.40', '2.78'), ('2021-12-01 10:23:54', '000411', '-0.46', '12.96', '4633', '20', '-0.07', '0.90'), ('2021-12-01 10:23:54', '000413', '-0.46', '2.17', '123312', '119', '0.00', '0.76'), ('2021-12-01 10:23:54', '000415', '0.65', '3.10', '709251', '19', '0.32', '7.88'), ('2021-12-01 10:23:54', '000416', '0.00', '4.16', '39925', '51', '-0.23', '1.28'), ('2021-12-01 10:23:54', '000417', '0.97', '4.18', '10404', '254', '0.00', '1.32'), ('2021-12-01 10:23:54', '000419', '0.47', '4.25', '5295', '51', '-0.22', '1.00'), ('2021-12-01 10:23:54', '000420', '-0.49', '6.14', '343795', '12', '-0.64', '1.14'), ('2021-12-01 10:23:54', '000421', '0.66', '4.60', '9071', '6', '0.00', '1.83'), ('2021-12-01 10:23:54', '000422', '0.00', '24.36', '426135', '10', '-0.68', '2.43'), ('2021-12-01 10:23:54', '000423', '0.86', '41.27', '16466', '67', '0.46', '0.80')"""
    intotest1 = """insert into gp_info (time,gpnum,zf,xj,zl,xl,zs,lb) values  ('2021-12-01 10:20:50', '000151', '0.39', '7.77', '6430', '259', '-0.12', '1.33'), ('2021-12-01 10:20:50', '000153', '-2.07', '12.30', '49604', '15', '-0.15', '1.31'), ('2021-12-01 10:20:50', '000155', '-1.14', '29.46', '214130', '65', '0.20', '1.43'), ('2021-12-01 10:20:50', '000156', '0.68', '7.37', '14055', '16', '0.14', '1.11'), ('2021-12-01 10:20:50', '000157', '1.15', '7.06', '201196', '24', '0.28', '2.16'), ('2021-12-01 10:20:50', '000158', '1.95', '7.31', '255050', '31', '0.69', '2.92'), ('2021-12-01 10:20:50', '000159', '-0.48', '6.26', '23535', '6', '0.16', '1.01'), ('2021-12-01 10:20:50', '000166', '1.19', '5.11', '307993', '78', '-0.19', '1.93'), ('2021-12-01 10:20:50', '000301', '3.04', '24.41', '310504', '38', '-0.48', '3.84'), ('2021-12-01 10:20:50', '000333', '0.28', '67.97', '65810', '65', '-0.03', '1.60'), ('2021-12-01 10:20:50', '000338', '5.57', '16.29', '964462', '1266', '1.18', '7.71'), ('2021-12-01 10:20:50', '000400', '0.52', '27.13', '225573', '43', '-0.10', '1.51'), ('2021-12-01 10:20:50', '000401', '-', '-', '0', '0', '-', '0.00'), ('2021-12-01 10:20:50', '000402', '1.27', '5.58', '44646', '5', '0.36', '1.67'), ('2021-12-01 10:20:50', '000403', '-0.92', '30.25', '8535', '3', '0.07', '1.59'), ('2021-12-01 10:20:50', '000404', '0.93', '4.33', '30381', '24', '0.00', '1.32'), ('2021-12-01 10:20:50', '000407', '0.96', '4.19', '20154', '190', '0.48', '1.02'), ('2021-12-01 10:20:50', '000408', '-1.89', '26.98', '45260', '2', '0.19', '1.21'), ('2021-12-01 10:20:50', '000409', '0.19', '5.23', '20171', '15', '0.00', '1.87'), ('2021-12-01 10:20:50', '000410', '2.30', '4.89', '41734', '30', '-0.19', '2.89'), ('2021-12-01 10:20:50', '000411', '-0.46', '12.96', '4536', '8', '0.00', '0.94'), ('2021-12-01 10:20:50', '000413', '-0.92', '2.16', '117191', '50', '0.00', '0.77'), ('2021-12-01 10:20:50', '000415', '0.32', '3.09', '695080', '99', '0.98', '8.18'), ('2021-12-01 10:20:50', '000416', '0.00', '4.16', '38991', '5', '0.00', '1.32'), ('2021-12-01 10:20:50', '000417', '0.97', '4.18', '9526', '9', '0.00', '1.28'), ('2021-12-01 10:20:50', '000419', '0.47', '4.25', '5223', '50', '0.00', '1.05'), ('2021-12-01 10:20:50', '000420', '0.00', '6.17', '329308', '123', '-0.47', '1.16'), ('2021-12-01 10:20:50', '000421', '0.88', '4.61', '8587', '2', '0.22', '1.83'), ('2021-12-01 10:20:50', '000422', '0.37', '24.45', '414631', '283', '-1.12', '2.50'), ('2021-12-01 10:20:50', '000423', '0.39', '41.08', '15632', '2', '0.27', '0.80') """
    intotest2 = """insert into gp_info (time,gpnum,zf,xj,zl,xl,zs,lb) values  ('2021-12-01 10:18:25', '000151', '0.52', '7.78', '5642', '5', '0.00', '1.21'), ('2021-12-01 10:18:25', '000153', '-1.91', '12.32', '48344', '29', '0.74', '1.33'), ('2021-12-01 10:18:25', '000155', '-0.81', '29.56', '208826', '1', '1.44', '1.45'), ('2021-12-01 10:18:25', '000156', '0.55', '7.36', '13792', '8', '0.14', '1.13'), ('2021-12-01 10:18:25', '000157', '1.29', '7.07', '190301', '193', '0.43', '2.13'), ('2021-12-01 10:18:25', '000158', '1.67', '7.29', '247124', '285', '0.41', '2.94'), ('2021-12-01 10:18:25', '000159', '-0.64', '6.25', '22460', '11', '0.16', '1.00'), ('2021-12-01 10:18:25', '000166', '1.39', '5.12', '293747', '53', '0.20', '1.92'), ('2021-12-01 10:18:25', '000301', '3.33', '24.48', '307901', '36', '0.37', '3.96'), ('2021-12-01 10:18:25', '000333', '0.12', '67.86', '63970', '39', '-0.33', '1.62'), ('2021-12-01 10:18:25', '000338', '4.47', '16.12', '887837', '216', '0.81', '7.38'), ('2021-12-01 10:18:25', '000400', '0.56', '27.14', '214582', '73', '0.93', '1.50'), ('2021-12-01 10:18:25', '000401', '-', '-', '0', '0', '-', '0.00'), ('2021-12-01 10:18:25', '000402', '0.91', '5.56', '40860', '1', '-0.17', '1.59'), ('2021-12-01 10:18:25', '000403', '-0.88', '30.26', '8354', '26', '-0.09', '1.62'), ('2021-12-01 10:18:25', '000404', '0.93', '4.33', '28871', '5', '0.00', '1.31'), ('2021-12-01 10:18:25', '000407', '0.48', '4.17', '16643', '9', '0.00', '0.88'), ('2021-12-01 10:18:25', '000408', '-1.82', '27.00', '44570', '4', '0.33', '1.24'), ('2021-12-01 10:18:25', '000409', '0.38', '5.24', '19777', '20', '0.19', '1.91'), ('2021-12-01 10:18:25', '000410', '2.30', '4.89', '41489', '20', '-0.19', '2.99'), ('2021-12-01 10:18:25', '000411', '-0.38', '12.97', '4511', '2', '0.31', '0.97'), ('2021-12-01 10:18:25', '000413', '-0.46', '2.17', '112366', '61', '0.46', '0.77'), ('2021-12-01 10:18:25', '000415', '0.00', '3.08', '686388', '663', '0.33', '8.40'), ('2021-12-01 10:18:25', '000416', '0.24', '4.17', '37267', '3', '0.72', '1.31'), ('2021-12-01 10:18:25', '000417', '0.97', '4.18', '8620', '106', '0.24', '1.20'), ('2021-12-01 10:18:25', '000419', '0.71', '4.26', '4542', '6', '0.24', '0.95'), ('2021-12-01 10:18:25', '000420', '0.16', '6.18', '316026', '24', '-0.31', '1.16'), ('2021-12-01 10:18:25', '000421', '0.44', '4.59', '7245', '1', '0.00', '1.61'), ('2021-12-01 10:18:25', '000422', '0.82', '24.56', '393208', '152', '-0.76', '2.47'), ('2021-12-01 10:18:25', '000423', '0.29', '41.04', '15116', '14', '0.05', '0.81') """
    for inss in [intotest,intotest1,intotest2]:
        cur.execute(inss)
        conn.commit()

            # cur.execute(sql)
            # conn.commit()
        # print("所用时间", time.time() - stat)

    # 关闭游标对象
    cur.close()
    # 关闭数据库连接
    conn.close()


if __name__ == '__main__':
    write_sql()
    # print([[x for x in range(1,100)] [i:i+3] for i in range(0,100,3)])