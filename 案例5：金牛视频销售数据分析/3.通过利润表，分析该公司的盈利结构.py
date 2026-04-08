# -*- coding:utf-8 -*-
'''
    @Project   :商务数据分析 
    @FileName  :3.通过利润表，分析该公司的盈利结构.py
    @Time      :2024/12/12-10:30
    @Author    :Lenovo
'''


import matplotlib.pyplot as plt
import pandas as pd


def main(file):
    df = pd.read_excel(file, sheet_name=1, usecols=['项目', '本年合计'])
    df.set_index('项目', inplace=True)

    yy_sr = df.loc['一、营业收入', '本年合计']

    yy_cb = df.loc['   减：营业成本', '本年合计']  # df.iloc[1, 0]
    sf = df.loc['       税金及附加', '本年合计'] + df.loc['   减：所得税费用', '本年合计']
    xs_fy = df.loc['       销售费用', '本年合计']
    gl_fy = df.loc['       管理费用', '本年合计']
    cw_fy = df.loc['       财务费用', '本年合计']
    jlr = df.loc['四、净利润（净亏损以“-”号填列）', '本年合计']

    parts = [yy_cb, sf, xs_fy, gl_fy, cw_fy, jlr]
    names = ['营业成本', '税费', '销售费用', '管理费用', '财务费用', '净利润']
    percent = []
    for part in parts:
        p = round(float(part) / float(yy_sr), 4)
        percent.append(p)
    print(percent)

    # 绘图
    plt.rcParams['font.family'] = ['STKaiti']
    plt.pie(percent,  # 也能不用
            autopct='%.2f%%',
            pctdistance=0.8,
            wedgeprops={'width': 0.4, 'linewidth': 1, 'edgecolor': 'w'},
            labels=names
            )
    plt.text(0, 0, '盈利结构', ha='center', va='center', fontsize=20, color='green')
    plt.text(0, -0.25, '--2021年底', ha='left', va='bottom', fontsize=13, color='orange')

    plt.title('公司盈利结构', fontsize=30, color='#404040', fontstyle='italic', fontweight='bold')

    plt.savefig('result/公司盈利结构.png')
    # plt.show()


if __name__ == "__main__":
    file = r'./data/cwal.xlsx'
    main(file)
