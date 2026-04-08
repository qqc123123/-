# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :008基金与被引关联分析.py
    @Time      :2024/11/15-10:51
    @Author    :Lenovo
'''

import pandas as pd
import numpy as np


def get_only_type(txt):
    only_type = ''
    if txt is np.nan:
        only_type = '无项目'
    elif '国家自然科学基金' in txt:
        only_type = '国家自然科学基金项目'
    elif '国家社会科学基金' in txt:
        only_type = '国家社会科学基金项目'
    elif '教育部' in txt:
        only_type = '教育部项目'
    elif '省级' in txt:
        only_type = '省级项目'
    else:
        only_type = '其他项目'

    return only_type

def main(file):
    df = pd.read_excel(file)
    df['基金最高级别'] = df['基金类型'].map(get_only_type)

    df_g = df.groupby(by='基金最高级别', as_index=True).agg({'基金最高级别':'count', '被引':'sum'})
    df_g.rename(columns={'基金最高级别':'总数量', '被引':'总被引数'}, inplace=True)
    df_g['平均被引次数'] = (df_g['总被引数'] / df_g['总数量']).round(2)

    df_g.to_excel(r'./result/基金类型与平均被引用关联111.xlsx')

if __name__ == "__main__":
    file = r'./result/职教脱敏_分词处理.xlsx'
    main(file)
