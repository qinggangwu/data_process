

import requests
import time
import pandas as pd
import json
import random
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request


def main():
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI CAZ-AL10 Build/HUAWEICAZ-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36 JsSdk/2 NewsArticle/7.0.1 NetType/wifi',
        'X-Requested-With': 'com.ss.android.article.news'
    }
    url = "https://is-lq.snssdk.com/search/?keyword=物业"
    url = "https://www.toutiao.com/a6947324083591823909/?traffic_source=&in_ogs=&utm_source=&source=search_tab&utm_medium=wap_search&original_source=&in_tfs=&channel=&enter_keyword=%E7%89%A9%E4%B8%9A&wid=1637997562803"
    req = requests.get(url=url, headers=head,verify=False)
    text = req.text

    soup = BeautifulSoup(text, 'lxml')
    print(soup)
    print(soup.select('title'))
    print(soup.select('#text'))
    # print(req.json())


def requests_move():
    url = 'https://movie.douban.com/chart'
    # 豆瓣排行榜

    herders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Referer': 'https://movie.douban.com/', 'Connection': 'keep-alive'}
    # 请求头信息

    req = urllib.request.Request(url, headers=herders)
    # 设置请求头
    response = urllib.request.urlopen(req)
    # response 是返回响应的数据
    htmlText = response.read()
    # 读取响应数据

    # 把字符串解析为html文档
    html = BeautifulSoup(htmlText, 'lxml')

    result = html.select(".pl2")
    # imgresult = html.select('.item')
    img_url = html.select('.nbg')[0].contents[1].attrs['src']  # 获取每个电影的封面
    # ss = img_url.select('img')[0]
    print(img_url);quit()

    # file = open('data.txt', 'a', encoding='utf-8')
    # 打开一个文本文件

    # 遍历几个
    for item in result:
        str = ''
        # 声明一个空的字符串
        str += item.select('a')[0].get_text().replace(' ', '').replace("\n", "")
        # 获取标题文字.替换掉空格.替换掉换行
        str += '('
        # 给评分加个左括号
        str += item.select('.rating_nums')[0].get_text()
        # 获取评分
        str += ')\n'
        # 给评分加个右括号
        print(str)
        print(item.select('.pl')[1].get_text())
        # 在控制台输出内容
        # file.write(str)
        # 写入文件

    # file.close()
    # 关闭文件

if __name__ == "__main__":
    requests_move()