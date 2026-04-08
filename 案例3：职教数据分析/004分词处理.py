# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :004分词处理.py
    @Time      :2024/11/8-11:03
    @Author    :Lenovo
'''
import numpy as np
import pandas as pd
import jieba.posseg as jp

def cut_string(input_string, stop_words):
    if isinstance(input_string, (int, float)) or input_string.strip()=='':
        return np.nan
    cut_words = []
    words_seg = jp.cut(input_string)
    for word, flag in words_seg:
        if word not in stop_words and len(word)>1 and flag in ['n', 'ns', 'nt', 'nw', 'nr', 'nz', 'f', 's', 'x']: #名词、地名、机构团体....
            cut_words.append(word)

    return ','.join(cut_words)


def main(file, stop_file):
    #01读取停用词表
    with open(stop_file, 'r', encoding='utf-8') as fp:
        stop_words = fp.read().split()
    #02读取文件，分词
    df = pd.read_excel(file)
    df['主副标题'] = df['主标题'] + df['副标题']

    df['摘要_分词'] = df['摘要'].apply(cut_string, args=(stop_words, ))
    df['主副标题_分词'] = df['主副标题'].apply(cut_string, args=(stop_words,))

    df.to_excel(r'./result/职教脱敏_分词处理.xlsx')


if __name__ == "__main__":
    stop_file = r'./data/stopwords.txt'
    file = r'./result/职教脱敏_补充后.xlsx'
    main(file, stop_file)
