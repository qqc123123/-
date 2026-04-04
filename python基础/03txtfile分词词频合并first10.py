# -*- coding:utf-8 -*-
'''
    @Project   :2024春 
    @FileName  :03txtfile分词词频合并first10.py
    @Time      :2024/6/18-8:05
    @Author    :Administrator--野牛首领
'''

import os
import time

import jieba.posseg as jp
from collections import Counter


def cut_freq(file, content):   # 对content文本分词、统计词频、存储
    # 读取停用词表
    with open(r'./otherfiles/stopwords.txt', 'r', encoding='utf-8') as fr1:
        stopwords = set(fr1.read().splitlines())

    # 根据词性筛选出需要的词，排除停用词和单字词
    words = []
    for word, flag in jp.cut(content):
        if (flag in ('n', 'nr', 'ns', 'nt', 'nw', 'nz', 'vn') and len(word) > 1 and word not in stopwords):
            words.append(word)

    # 统计词频、存储到同名的.csv文件当中
    word_freq = Counter(words)

    with open(file.replace('.txt', '.csv'), 'w', encoding='utf-8') as fw1:
        fw1.write('word,freq')
        for word, freq in word_freq.items():
            fw1.write(f'{word},{freq}\n')


def visit_everyfile(path):
    # 遍历每一个文件，合并前10个内容，每一个文件调用函数分词、统计词频、存储
    failed_files = []
    first10_content = ''
    file_list = [f for f in os.listdir(path) if f.endswith('.txt')]

    for i, file in enumerate(file_list, start=1):
        print(f'正在处理第{i}/{len(file_list)}个文件{file}...')

        try:
            file_path = os.path.join(path, file)
            with open(file_path, 'r', encoding='utf-8') as fr2:
                content = fr2.read()
                if i < 10:
                    first10_content += content
                cut_freq(file_path, content)
        except Exception as e:
            failed_files.append(file)
            print('发生错误，错误信息已经记录！')
            with open(r'./result/文本文件处理失败记录.txt', 'w', encoding='utf-8') as fw2:
                for file in failed_files:
                    fw2.write(f'文件：  {file}  报错\n, 错误是： {e} \n')

    #　将前10个txt文件的内容写入first10.txt文件当中
    with open(r'./result/first10.txt', 'w', encoding='utf-8') as fw3:
        fw3.write(first10_content)


if __name__ == "__main__":
    path = r'./txtfiles'
    visit_everyfile(path)

"""


"""

