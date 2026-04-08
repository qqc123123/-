# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :002关键词合并与删除.py
    @Time      :2024/11/7-11:45
    @Author    :Lenovo
'''
import numpy as np
import pandas as pd


def create_dict(merge_keywords_file):
    change_dict = dict()
    with open(merge_keywords_file, 'r', encoding='utf-8') as fp:
        for line in fp:
            kv = line.strip().split('，')
            if len(kv) == 2:
                k = kv[0].strip()
                v = kv[1].strip()
            else:
                k = kv[0].strip()
                v = np.nan
            change_dict[k] = v

    return change_dict


def merge_keywords(key_wordstr, change_dict):
    if key_wordstr is np.nan or '未找到对应文章' in key_wordstr:
        return ''
    remain_keywords = []
    for kw in key_wordstr.split(','):
        if kw not in change_dict.keys():
            remain_keywords.append(kw)
            continue
        else:
            if change_dict[kw] is not np.nan:
                remain_keywords.append(change_dict[kw])
            else:
                continue

    return ','.join(remain_keywords)


def main(file, merge_keywords_file):
    change_dict = create_dict(merge_keywords_file)  #生成字典
    df = pd.read_excel(file)
    df['合并关键词'] = df['关键词'].apply(merge_keywords, args=(change_dict, ))
    df.to_excel(r'./result/职教脱敏_关键词合并.xlsx', index=False)

if __name__ == "__main__":
    file = r'./result/职教脱敏_清洗后.xlsx'
    merge_keywords_file = r'./data/关键词合并表.txt'
    main(file, merge_keywords_file)
