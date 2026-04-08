# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :007高被引数据统计.py
    @Time      :2024/11/15-10:22
    @Author    :Lenovo
'''

import pandas as pd

def main(file):
    df = pd.read_excel(file)
    df.sort_values(by='被引', ascending=False, inplace=True)

    #01高被引全作者
    df1 = df.groupby(by='作者', as_index=False)['被引'].sum()
    df1.sort_values(by='被引', inplace=True, ascending=False)
    df1.to_excel(r'./result/高被引作者榜（全作者）.xlsx', index=False)

    #02高被引作者(1作)
    df2 = df.groupby(by='一作姓名', as_index=False)['被引'].sum()
    df2.sort_values(by='被引', inplace=True, ascending=False)
    df2.to_excel(r'./result/高被引作者榜（一作）.xlsx', index=False)

    #03高被引论文榜单

    # df2 = df.groupby(by='主标题', as_index=False)['被引'].sum()
    # df2.sort_values(by='被引', inplace=True, ascending=False)
    # df2.to_excel(r'./result/高被引论文榜111.xlsx', index=False)

    df3 = df[df['被引']>0][['主标题', '被引']]
    df3.to_excel(r'./result/高被引论文榜111.xlsx', index=False)

    # 03高被引期刊榜

    df4 = df.groupby(by='杂志名称', as_index=False)['被引'].sum()
    df4.sort_values(by='被引', inplace=True, ascending=False)
    df4.to_excel(r'./result/高被引期刊榜111.xlsx', index=False)


if __name__ == "__main__":
    file = r'./result/职教脱敏_分词处理.xlsx'
    main(file)
