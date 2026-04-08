# -*- coding:utf-8 -*-
'''
    @Project   :案例4：招聘网站数据分析 
    @FileName  :4、各地工作年限与薪资关系分析.py
    @Time      :2024/11/20-23:47
    @Author    :Lenovo
'''


import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_excel(r'./result/招聘数据清洗薪资.xlsx')

    df = df.dropna(subset=['salary_min', 'salary_max', 'salary_mean'])

    years_experience = df['workyear']
    # df[['workyear', 'salary_mean']] = df[['workyear', 'salary_mean']].groupby(df['word_city'])
    years_experience_vs_salary = df.pivot_table(values='salary_mean', index='workyear', columns='word_city')
    print(years_experience_vs_salary)

    years_experience_vs_salary.plot(kind='line', marker='o')



    plt.rcParams['font.family'] = ['KaiTi']
    plt.figure(figsize=(6, 4), dpi=300)
    plt.plot(df['workyear'], df['word_city'], label='上海', marker='s')
    plt.plot(df['workyear'], df['word_city'], label='北京', marker='*')

    plt.xlabel('workyear')
    plt.ylabel('salary_mean')
    plt.title('各地工作年限与薪资关系分析')
    # 刻度变成12个！！！！！

    plt.xticks(list(map(lambda m: str(m) + '年' for m in df['workyear'])))
    plt.legend()

    plt.show()