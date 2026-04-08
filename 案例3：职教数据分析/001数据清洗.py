# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :001数据清洗.py
    @Time      :2024/11/7-10:07
    @Author    :Lenovo
'''
import re

import numpy as np
import pandas as pd

def clean_col(s):
    if s.strip() == '无' or s.strip() == '无对应文章' or s.strip() == '未找到对应文章':
        return np.nan
    clean_s = re.sub(r'[；\-;,，：:、/ ]+', ',', s)  # 正则....
    return clean_s


def get_primary_unit(input_string):
    if '不详' in input_string:
        return np.nan
    match = re.search(r'^(.+?)(?:大学|学院|学校|研究所|研究院)', input_string)
    if match:
        return match.group(0)
    else:
        # input_string.spirt()[0]  #
        return np.nan


def extract_project_code(txt):
    projects = re.findall('[a-zA-Z0-9\[\]\-/_]+', txt)
    projects = [item for item in projects if not item.isalpha() and item not in ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'] and len(item) > 2]
    if projects:
        return ','.join(projects)
    else:
        return np.nan


def contains_substring(txt):
    sub_strings = ['省', '北京市', '天津市', '上海市', '重庆市', '自治区', '建设兵团']
    for sub_str in sub_strings:
        if sub_str in txt:
            return True

    return False


def get_fund_type(text):  # 获取基金类型
    items = []
    if text is np.nan or '无' in text or text.strip() == '未找到对应文章':
        return np.nan
    for txt in text.split('；'):
        if '国家社科' in txt or '国家社会科学' in txt:
            items.append('国家社会科学基金')
        elif '国家自科' in txt or '国家自然科学' in txt:
            items.append('国家自然科学基金')
        elif '教育部' in txt:
            items.append('教育部')
        elif contains_substring(txt):
            items.append('省级')
        else:
            items.append('其他')

    if items:
        return ','.join(items)
    else:
        return np.nan


def main(file):
    df = pd.read_excel(file)
    #01重复值的处理
    df.drop_duplicates(keep='first', inplace=True)
    #02处理空值
    # empty_rows = df[['主标题', '副标题', '作者', '杂志名称']].isna().all(axis=1)  #查看那4列全为空的行索引
    # print(df[empty_rows])
    df.dropna(subset=['主标题', '副标题', '作者', '杂志名称'], how='all', inplace=True)
    #03列清洗
    df['作者'] = df['作者'].map(clean_col)
    df['关键词'] = df['关键词'].map(clean_col)
    df['作者单位'] = df['作者单位'].map(clean_col)

    df['一作单位'] = df['一作单位'].map(get_primary_unit)
    df['一作姓名'] = df['一作姓名'].map(lambda name: name.strip())
    df['杂志名称'] = df['杂志名称'].map(lambda mc: mc.strip().replace('《', '').replace('》', ''))

    #04提取基金中的项目编号和数量，并获取基金类型
    df['基金'] = df['基金'].map(lambda txt:np.nan if txt is np.nan else txt.replace('；主持人', ',主持人'))
    df['基金号'] = df['基金'].map(extract_project_code)
    df['基金数量'] = df['基金号'].map(lambda proj: 0 if proj is np.nan else len(proj.split(',')))
    df['基金类型'] = df['基金'].map(get_fund_type)
    # print(df['基金类型'].to_list())
    df.to_excel(r'./result/职教脱敏_清洗后.xlsx', index=False)





if __name__ == "__main__":
    file = r'./data/职教脱敏.xlsx'
    main(file)

