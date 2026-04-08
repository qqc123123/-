# -*- coding:utf-8 -*-
'''
    @Project   :课程文件 
    @FileName  :数据清洗01.py
    @Time      :2024/10/23-21:46
    @Author    :Lenovo
'''


import pandas as pd
import numpy as np
import re


def clean_string(string):
    if string is np.nan or str(string).strip() == '':
        return np.nan
    elif type(string) is int:
        return string
    else:
        return re.sub(r'[^0-9A-Za-z\u4E00-\u9fa5+]', '', string)


if __name__ == "__main__":

    df = pd.read_excel(r'./任务03.xlsx', sheet_name='资产负债表')
    df = df.drop_duplicates(keep='first')

    df['期间'] = list(map(lambda x: clean_string(x), df['期间']))
    df['销售费用'] = list(map(lambda x: float(clean_string(x)), df['销售费用']))
    df['财务费用'] = list(map(lambda x: clean_string(x), df['财务费用']))

    df = df.set_index('期间')
    df = df.apply(pd.to_numeric)

    df = df.dropna(axis=1, how='all')
    df['营业收入'] = df['营业收入'].fillna(20000)
    df['管理费用'] = df['管理费用'].fillna(3000)

    df = df.fillna(df.mean())
    df = df.round(2)
    print(df)

    df1 = pd.read_excel(r'./任务03.xlsx', sheet_name='利润表')

    df1['年月'] = df1['年'].astype(str) + '-' + df1['月'].astype(str)
    df1.set_index('年月', inplace=True)
    df1.drop(['年', '月'], axis=1, inplace=True)
    df1 = df1 / 10000

    df1['营业净利率'] = df1['净利润'] / df1['营业收入']
    df1['业绩评价'] = df1['营业净利率'].apply(lambda x: '达标' if x > 0.18 else '不达标')


    df1['是否发放奖金'] = df1['业绩评价'].apply(lambda x: True if x == '达标' else False)

    p = 0.08
    df1['奖金额'] = df1['是否发放奖金'].apply(lambda x: x * p if x else 0)

    # df1.columns = [col + '(万)' for col in df1.columns]
    # df1 = df1.rename(columns={'营业净利率(万)':'营业净利率(%)', '业绩评价(万)':'业绩评价', '是否发放奖金(万)':'是否发放奖金'})
    df1.rename(columns={'营业收入': '营业收入(万)', '营业成本': '营业成本(万)', '净利润': '净利润(万)', '营业净利率': '营业净利率(%)', '奖金额': '奖金额(万)'}, inplace=True)

    df1['营业净利率(%)']=(df1['营业净利率(%)']*100).round(4).astype(str) + '%'
    # df1['营业净利率(%)'] = df1['营业净利率(%)'].astype(str) + '%'
    print(df1)

    df2 = pd.read_excel(r'./任务03.xlsx', sheet_name='财务指标')

    df2.dropna(how='all', inplace=True)
    df2['年份'] = df2['年份'].astype('str')
    df2.set_index('年份', inplace=True)
    df2['权益乘数'] = df2['权益乘数'].fillna(df2['权益乘数'].median())

    p1 = 0.01
    df2['营业净利率'] = df2['营业净利率'].apply(lambda x, y: x - y, args=(p1,))  # 此问题有更简单的方法

    p2 = 0.02
    df2['资产周转率'] = df2['资产周转率'].apply(lambda x, y: x + y, args=(p2,))

    df2['净资产收益率'] = df2.apply(lambda row: round(row.prod(), 4), axis=1)

    df2 = df2.round(4)
    print(df2)

    with pd.ExcelWriter(r'./清洗好的数据.xlsx', engine='openpyxl', mode='w') as fw:
        df.to_excel(fw, sheet_name='资产负债表')
        df1.to_excel(fw, sheet_name='利润表')
        df2.to_excel(fw, sheet_name='财务指标')

    #另一种写法，对大数据更适用！！！
    # dfs = [df, df1, df2]
    # sheet_names = ['资产负债表', '利润表', '财务指标']
    # with pd.ExcelWriter(r'C:\Users\Lenovo\Desktop\清理好的任务03_副本.xlsx') as writer:
    #     for df, sheet_name in zip(dfs, sheet_names):
    #         df.to_excel(writer, sheet_name=sheet_name)