# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :006基金数量种类统计.py
    @Time      :2024/11/15-10:05
    @Author    :Lenovo
'''

import pandas as pd
import numpy as np
from collections import Counter


def main(file):
    df = pd.read_excel(file)
    df_foud = df.groupby(by='基金数量').size().reset_index(name='出现次数')
    # print(df_foud)
    df_foud.to_excel(r'./result/基金数量统计111.xlsx', index=None)

    all_kinds = []
    for kinds in df['基金类型']:
        if kinds is not np.nan:
            all_kinds.extend(kinds.split(','))
    # print(all_kinds)
    kind_freq = Counter(all_kinds).most_common()
    df_counts = pd.DataFrame(data=kind_freq, columns=['基金类型' ,'次数'])
    # print(df_counts)
    df_counts.to_csv(r'./result/基金类型统计111.csv', index=None)





if __name__ == "__main__":
    file = r'./result/职教脱敏_分词处理.xlsx'
    main(file)
