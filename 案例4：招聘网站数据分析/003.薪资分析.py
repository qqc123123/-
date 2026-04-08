# -*- coding:utf-8 -*-
'''
    @Project   :案例4：招聘网站数据分析 
    @FileName  :003.薪资分析.py
    @Time      :2024/11/29-10:48
    @Author    :Lenovo
'''
import pandas as pd
import re
import numpy as np


def contains_specific_strings(input_string):
    patterns = ['万/月', '千/月', '万/年']
    for pattern in patterns:
        if pattern in input_string:
            return True
    return False


def get_salary_data(row):
    sala_str = row['providesalary_text']
    if contains_specific_strings(sala_str):
        salary_rets = re.findall('([\d\.]*?)-([\d\.]*?)(万/月|千/月|万/年)', sala_str)

        if salary_rets[0][2] == '万/月':
            a = 10000
        elif salary_rets[0][2] == '千/月':
            a = 1000
        else:
            a = 10000 / 12
        row['salary_min'] = int(float(salary_rets[0][0]) * a)
        row['salary_max'] = int(float(salary_rets[0][1]) * a)
        row['salary_mean'] = (row['salary_min'] + row['salary_max']) / 2
    elif '元/天' in sala_str:
        patten = '(\d+\.\d+|\d+)(?=元/天)'
        numbers = re.findall(patten, sala_str)
        row['salary_min'] = row['salary_max'] = row['salary_mean'] = int(float(numbers[0])) * 30
    else:
        row['salary_min'] = row['salary_max'] = row['salary_mean'] = np.nan

    return row


def main(file):
    print('正在打开数据...')
    df = pd.read_excel(file)
    # 01求最高、最低、平均工资
    print('正在求最高、最低、平均工资')
    df = df.apply(get_salary_data, axis=1)
    # print(df[['salary_max', 'salary_min', 'salary_mean']])
    df.to_excel(r'./result/招聘数据清洗薪资.xlsx', index=False)

    # 02薪资数据离散化
    print('正在将薪资数据离散化...')
    category = [0, 5000, 10000, 20000, 30000, 40000, 50000, 1000000]
    labels = ['0-5 千/月', '0.5-1 万/月', '1-2 万/月', '2-3 万/月', '3-4 万/月', '4-5 万/月', '5万 / 月以上']
    df['salary_sep'] = pd.cut(df['salary_mean'], category, right=True, labels=labels)

    #03统计各城市薪资分布情况
    work_cities = ['广州', '上海', '北京', '深圳', '全数据']
    for city in work_cities:
        print(f'正在统计{city}市的薪资分布..', end='')
        if city != '全数据':
            df_temp = df[df['workarea_text'].str.contains(city)]  #还可以用“work_city”列来筛选
            df_sala_stat = df_temp['salary_sep'].value_counts().reset_index()
            df_sala_stat.to_csv(f'./result/薪资分布统计结果_{city}.csv', index=False)
            print(end='')
        else:
            df_temp = df[df['workarea_text'].str.contains(city)]  #还可以用“work_city”列来筛选
            df_sala_stat = df_temp['salary_sep'].value_counts().reset_index()
            df_sala_stat.to_csv(f'./result/薪资分布统计结果_{city}.csv', index=False)
            print(end='')


    #04统计各城市平均工资
    df_g = df.groupby(by='word_city', as_index=False)['salary_mean'].mean().round(2)
    df_g.to_csv(r'./result/各城市平均薪资.csv', index=False)







if __name__ == "__main__":
    file = r'./result/招聘数据清洗.xlsx'
    main(file)

