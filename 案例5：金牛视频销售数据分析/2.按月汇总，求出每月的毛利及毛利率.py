# -*- coding:utf-8 -*-
'''
    @Project   :案例5：金牛视频销售数据分析 
    @FileName  :2.按月汇总，求出每月的毛利及毛利率.py
    @Time      :2024/12/11-20:25
    @Author    :Lenovo
'''


import pandas as pd
import matplotlib.pyplot as plt


def main(file):
    df = pd.read_excel(file, sheet_name=1).iloc[0:2, 1:13]

    data1 = df.loc[0] - df.loc[1]
    df_data1 = pd.DataFrame(data=data1)
    print(df_data1)

    data2 = df_data1[0] / df.loc[0]
    df_data2 = pd.DataFrame(data=data2)
    df_data2[0] = round(df_data2[0] * 100, 2)
    print(df_data2)

    months = range(1, 13)
    heights1 = df_data1[0]  # 毛利
    heights2 = df_data2[0]  # 率

    # 绘图
    plt.rcParams['font.family'] = ['STKaiti']

    # 创建一个图形和两个y轴
    fig, ax1 = plt.subplots(figsize=(13, 7), dpi=80)
    plt.ylim(18.0, 24.0)  # 注意*&（*……*&……*……*（&*：双轴要特别设置范围时，需要注意顺序）

    ax2 = ax1.twinx()

    line = ax1.plot(months, heights2, label='毛利率', color='red', marker='o')
    bar = ax2.bar(months, heights1, label='毛利', color='#90EE90', alpha=0.6)

    ax1.set_xlabel('月份', fontdict={'size': 16})
    ax1.set_ylabel('销售毛利率(%)', fontdict={'size': 16})
    ax2.set_ylabel('销售毛利(元)', fontdict={'size': 16})

    plt.title('销售毛利、毛利率')

    ax1.legend(loc=2)  # 分别显示出来
    ax2.legend(loc=1)

    for i in months:
        ax1.text(x=i, y=heights2[i - 1] + 0.08, s=str(round(heights2[i - 1], 1)), ha='left', fontsize=12, )

    plt.savefig(f'result/销售毛利、毛利率.png')
    # plt.show()


if __name__ == "__main__":
    file = r'./data/cwal.xlsx'
    main(file)
















    df = pd.read_excel(file)
    df = pd.read_excel(file, sheet_name='利润表')

    df['月份'] = pd.to_datetime(df['销售日期']).dt.month
    monthly_profit = df.groupby('月份')['销售收入', '成本'].sum().reset_index()
    monthly_profit['毛利'] = monthly_profit['销售收入'] - monthly_profit['成本']
    monthly_profit['毛利率'] = monthly_profit['毛利'] / monthly_profit['销售收入']
    monthly_profit.set_index('月份', inplace=True)
    print(monthly_profit)