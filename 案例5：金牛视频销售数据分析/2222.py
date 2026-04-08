# -*- coding:utf-8 -*-
'''
    @Project   :案例5：金牛视频销售数据分析 
    @FileName  :2222.py
    @Time      :2024/12/11-20:58
    @Author    :Lenovo
'''

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt

    # 读取Excel文件
    file_path = r'./data/cwal.xlsx'
    df0 = pd.read_excel(file_path, sheet_name='销售明细表')
    df1 = pd.read_excel(file_path, sheet_name='利润表')
    # 任务1：统计销售收入前15的品牌
    top_sales = df0['收入合计'].sort_values(ascending=False).head(15)
    top_salesBrand = df0['商品名称'][df0['收入合计'] >= top_sales.min()]
    top_sales_df = pd.DataFrame({'品牌': top_salesBrand, '销售收入（万元）': top_salesBrand * 10000})  # 假设收入合计单位是元，转换为万元

    # 任务2：按月汇总，求出每月的毛利及毛利率
    monthly_data = df0.groupby('月份')['收入合计', '成本合计'].agg('sum')
    monthly_data['毛利'] = monthly_data['收入合计'] - monthly_data['成本合计']
    monthly_data['毛利率'] = (monthly_data['毛利'] / monthly_data['收入合计']) * 100

    # 任务3：分析该公司的盈利结构

    # df_transposed = df1.transpose()
    # df_transposed.to_excel(r'./result/利润表转置数据.xlsx')
    df3 = pd.read_excel(r'./result/利润表转置数据.xlsx')
    profit_structure = {
        '营业成本': df3['   减：营业成本'].sum(),
        '销售费用': df3['       销售费用'].sum(),
        '管理费用': df3['       管理费用'].sum(),
        '财务费用': df3['       财务费用'].sum(),
        '税费': df3['       税金及附加'].sum(),
        '净利润': df3['四、净利润（净亏损以“-”号填列）'].sum()
    }
    profit_df = pd.DataFrame(profit_structure, index=['百分比(%)']).T

    # 输出结果
    # print(df3)
    # print("销售收入前15的品牌：")
    # print(top_sales_df)
    # print("\n按月汇总的毛利及毛利率：")
    # print(monthly_data)
    # print("\n盈利结构：")
    # print(profit_df)

    # 可视化
    plt.figure(figsize=(10, 6))

    # 任务1的可视化
    plt.subplot(2, 2, 1)
    plt.bar(top_sales_df['品牌'], top_sales_df['销售收入（万元）'], color='blue')
    plt.title('热销商品Top-15')
    plt.ylabel('销售收入（万元）')

    # 任务2的可视化
    plt.subplot(2, 2, 2)
    plt.plot(monthly_data.index, monthly_data['毛利率'], 'ro-', label='毛利率')
    plt.bar(monthly_data.index, monthly_data['毛利'], alpha=0.3, label='毛利')
    plt.title('销售毛利、毛利率')
    plt.ylabel('销售毛利率(%) / 销售毛利(元)')
    plt.legend()

    # # 任务3的可视化
    # plt.subplot(2, 2, 4)
    # plt.pie(profit_df['百分比(%)'], labels=profit_df.index, autopct='%1.1f%%%')
    # plt.title('盈利结构—2021年底')

    plt.tight_layout()
    plt.show()
