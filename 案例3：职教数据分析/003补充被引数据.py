# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :003补充被引数据.py
    @Time      :2024/11/8-10:40
    @Author    :Lenovo
'''

import pandas as pd


def main(file1, file2):
    #读取文件1
    df1 = pd.read_excel(file1, usecols=['Title-题名', 'Author-作者', '被引'])
    df1['主标题'] = df1['Title-题名'].map(lambda s: s.strip().split('——')[0].strip())
    # print(df1['主标题'].head(10))
    #读取文件2
    df2 = pd.read_excel(file2)
    df2['主标题'] = df2['主标题'].map(lambda s: s.strip())

    #合并数据
    df = pd.merge(df2, df1, how='left', left_on='主标题', right_on='主标题')
    df.drop(columns=['Title-题名', 'Author-作者'], inplace=True)

    df.to_excel(r'./result/职教脱敏_补充后.xlsx')

if __name__ == "__main__":
    file1 = r'./data/被引数据表.xlsx'
    file2 = r'./result/职教脱敏_关键词合并.xlsx'
    main(file1, file2)
