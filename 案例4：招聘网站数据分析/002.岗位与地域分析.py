# -*- coding:utf-8 -*-
'''
    @Project   :案例4：招聘网站数据分析 
    @FileName  :002.岗位与地域分析.py
    @Time      :2024/11/29-10:28
    @Author    :Lenovo
'''
import pandas as pd



def main(file):
    df = pd.read_excel(file)

    # 01岗位与工作地点
    print('正在统计所有岗位各城市数量...')
    df_work_city = df['word_city'].value_counts().reset_index()    # 还可用其他方法
    df_work_city.columns = ['city', 'count']
    # print(df)
    df_work_city.to_csv(r'./result/工作岗位统计结果_全行业.csv', index=False)

    # 02各种岗位与工作地点
    work_types = ['数据', '游戏', '运维']

    for work_type in work_types:
        print(f'正在统计{work_type}行业各城市岗位数量...', end='')
        df_temp = df[df['job_name'].str.contains(work_type)]
        df_work_city = df_temp['word_city'].value_counts().reset_index()
        target_file = f'./result/工作岗位统计结果_{work_type}.csv'
        print('正在存储...', end='')
        df_work_city.to_csv(target_file)




if __name__ == "__main__":
    file = r'./result/招聘数据清洗.xlsx'
    main(file)