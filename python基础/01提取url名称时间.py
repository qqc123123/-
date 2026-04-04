# -*- coding:utf-8 -*-
'''
    @Project   :2024春 
    @FileName  :01提取url名称时间.py
    @Time      :2024/6/17-15:31
    @Author    :Administrator--野牛首领
'''

import re

def extraction_data(html_file):
    # step1:读取页面内容
    with open(html_file, 'r', encoding='utf-8') as fr:
        url = fr.read()

    # step2:利用正则表达解析报告url(需要拼接学院网址)、标题、时间
    obj = re.compile(
        r'<a href=\'(?P<link>.*?)\' target=\'_blank\' title=\'(?P<title>.*?)\'>.*?<span class=\'Article_PublishDate\'>(?P<time>.*?)</span> ',
        re.S
    )
    data = obj.finditer(url)

    with open(r'./result/数据提取结果.csv', 'w', encoding='utf-8') as fw:
        fw.write('链接地址, 标题, 时间\n')

        for item in data:
            link = 'https://gy.nwnu.edu.cn/' + item.group('link')# 拼接学院网址
            title = item.group('title')
            time = item.group('time')
            fw.write(f'{link}, {title}, {time}\n')


if __name__ == "__main__":
    html_file = r'./otherfiles/test_web.html'
    extraction_data(html_file)

