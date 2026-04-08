# -*- coding:utf-8 -*-
'''
    @Project   :案例5：金牛视频销售数据分析 
    @FileName  :1.统计销售收入前15的品牌.py
    @Time      :2024/12/11-20:14
    @Author    :Lenovo
'''


import pandas as pd
import matplotlib.pyplot as plt


def main(file):
    #筛选
    df = pd.read_excel(file, sheet_name=0, usecols=['商品名称', '收入合计'])
    df_count = df.groupby(by='商品名称').sum().reset_index()

    df_count.sort_values(by='收入合计', inplace=True, ascending=False)
    df_count.reset_index(drop=True, inplace=True)
    df_count = df_count.loc[0: 14, :]
    df_count['收入合计(万元)'] = round((df_count['收入合计'] / 10000), 1)

    #可视化
    plt.rcParams['font.family'] = ['STKaiti']
    plt.figure(figsize=(8, 6), dpi=600)

    s = range(len(df_count['商品名称']))
    heights = list(df_count['收入合计(万元)'])

    plt.bar(x=s, height=heights, color='blue')
    plt.xticks(ticks=range(len(df_count['商品名称'])), labels=list(df_count['商品名称']),
               fontsize=6, rotation=30, fontweight='bold')

    plt.title('热销商品Top-15')
    plt.xlabel('商品名称')
    plt.ylabel('销售收入(万元)')

    for i in s:
        plt.text(x=i, y=heights[i], s=str(heights[i]), ha='center', va='bottom')

    plt.legend()

    plt.savefig(r'result/热销商品top-15.png')
    # plt.show()


if __name__ == "__main__":
    file = r'./data/cwal.xlsx'
    main(file)








# df = pd.read_excel(file, sheet_name='销售明细表')
    #
    # plt.rcParams['font.sans-serif'] = ['KaiTi']  # 显示中文
    #
    # top_brands = df.groupby('商品名称')['收入合计'].sum().nlargest(15).reset_index()
    # top_brands.columns = ['商品名称', '收入合计']
    # top_brands.plot(kind='bar', x='商品名称', y='收入合计', legend=False, figsize=(12, 10))
    #
    # plt.bar(top_brands['商品名称'], top_brands['收入合计'])
    # plt.xlabel('')
    # plt.ylabel('销售收入(万元)')
    # plt.title('热销商品top-15 ')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.savefig(r'./result/热销商品top-15.png')
    # plt.show()