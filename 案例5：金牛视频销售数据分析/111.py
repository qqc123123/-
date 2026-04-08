# -*- coding:utf-8 -*-
'''
    @Project   :案例5：金牛视频销售数据分析 
    @FileName  :111.py
    @Time      :2024/12/11-20:35
    @Author    :Lenovo
'''

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt

    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 显示中文
    # 读取Excel文件
    file_path = r'./data/cwal.xlsx'
    sales_df = pd.read_excel(file_path, sheet_name='销售明细表')
    profit_df = pd.read_excel(file_path, sheet_name='利润表')

    # 任务1：统计销售收入前15的品牌


    # 任务2：按月汇总，求出每月的毛利及毛利率
    monthly_profit = sales_df.groupby(sales_df['月份'].dt.to_period('M')).agg({'毛利': 'sum', '销售收入': 'sum'})
    monthly_profit['毛利率'] = monthly_profit['毛利'] / monthly_profit['销售收入']
    monthly_profit.plot(kind='bar', x=monthly_profit.index, y=['毛利', '毛利率'], legend=True, figsize=(10, 6))
    plt.title('Monthly Gross Profit and Gross Margin')
    plt.xlabel('Month')
    plt.ylabel('Gross Profit / Gross Margin')
    plt.tight_layout()
    plt.savefig('monthly_profit.png')  # 保存图片，确保与PPT中的图片一致
    plt.show()

    # 任务3：通过利润表，分析该公司的盈利结构
    profit_components = profit_df.set_index('项目')['金额'].plot(kind='bar', figsize=(10, 6))
    plt.title('Profit Structure Analysis')
    plt.xlabel('Profit Component')
    plt.ylabel('Amount')
    plt.tight_layout()
    plt.savefig('profit_structure.png')  # 保存图片，确保与PPT中的图片一致
    plt.show()
