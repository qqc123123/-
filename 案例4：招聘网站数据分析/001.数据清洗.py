# -*- coding:utf-8 -*-
'''
    @Project   :案例4：招聘网站数据分析 
    @FileName  :001.数据清洗.py
    @Time      :2024/11/29-10:07
    @Author    :Lenovo
'''


import pandas as pd
import re


def deal_place(workarea_text):
    city = re.findall(r'[\u4e00-\u9fff]+', workarea_text)[0]
    return city


def main(file):
    df = pd.read_excel(file)
    print('正在打开数据....')
    # old_len = len(df)

    #01重复值
    print('正在删除重复数据。。。。')
    df.sort_values(by=['company_name', 'job_name', 'issuedate'], ascending=[True, True, False], inplace=True)
    df.drop_duplicates(subset=['company_name', 'job_name'], keep='first', inplace=True)

    #02空值处理
    df.dropna(how='any', inplace=True)
    print('正在删除空值...')
    # new_len = len(df)
    # print(old_len, new_len)  #与清洗数据无关，输出前后长度，只为观察

    #03规范地区并清洗
    df['word_city'] = df['workarea_text'].map(deal_place)

    #04.存储清洗后的数据
    df.to_excel(r'./result/招聘数据清洗.xlsx')





if __name__ == "__main__":
    file = r'./data/招聘数据.xlsx'
    main(file)
