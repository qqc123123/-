# -*- coding:utf-8 -*-
'''
    @Project   :案例4：招聘网站数据分析 
    @FileName  :5、统计公司类型分布情况.py
    @Time      :2024/11/20-23:51
    @Author    :Lenovo
'''


import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_excel(r'./result/招聘数据清洗.xlsx')
    company_types = df['companytype_text'].value_counts()
    company_types.to_excel(r'./result/公司类型分布.xlsx')

    # 输出并存储复合饼图
    # company_types.plot(kind='pie', autopct='%1.1f%%')


    plt.rcParams['font.family'] = ['KaiTi']
    explode = [0.1, 0, 0, 0, 0, 0, 0, 0.2, 0, 0]

    plt.pie(company_types['companytype_text'],
            autopct='%.2f%%',  # 设置百分比
            pctdistance=1.2,  # 设置数字位置
            explode=explode,  # 设置各部分离圆心的距离
            wedgeprops={'width': 0.4, 'linewidth': 1, 'edgecolor': 'y'}  # 环形饼状图
            )
    plt.title('公司类型分布')
    plt.savefig(r'./result/公司类型分布.png', dpi=600)  # 存储图形务必放在show（）之前
    plt.show()