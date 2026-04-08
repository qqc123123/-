# -*- coding:utf-8 -*-
'''
    @Project   :邱杰成202330906124
    @FileName  :6. 留存分析.py
    @Time      :2024/12/26-14:59
    @Author    :Lenovo
'''


import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
import numpy as np


def line(file1, file2, file3):
    print('正在读取数据...')
    shop_info_columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt', 'shop_level','cate_1_name', 'cate_2_name', 'cate_3_name']
    user_pay_columns = ['user_id', 'shop_id', 'time_stamp']
    user_view_columns = ['user_id', 'shop_id', 'time_stamp']
    shop_info = pd.read_csv(file1, sep=",", header=None, names=shop_info_columns, encoding='utf-8')
    user_pay = pd.read_csv(file2, sep=",", header=None, names=user_pay_columns, encoding='utf-8')
    user_view = pd.read_csv(file3, sep=",", header=None, names=user_view_columns, encoding='utf-8')
    print('数据读取完毕...')

    print('计算每个商家的总交易额...')
    merged_data = pd.merge(user_pay, shop_info, on='shop_id')
    total_sales = merged_data.groupby('shop_id')['per_pay'].sum().reset_index()

    print('取平均交易额top_3...')
    top_3_shops = total_sales.sort_values(by='per_pay', ascending=False).head(3)['shop_id'].tolist()
    data = {shop_id: {i: 0 for i in range(31)} for shop_id in top_3_shops}

    print('计算留存率...')
    for shop_id in top_3_shops:
        shop_viewers = set(user_view[user_view['shop_id'] == shop_id]['user_id'])
        for i in range(31):
            date = f'2016-10-{(i + 1):02d}'
            active_users = set(
                user_view[(user_view['shop_id'] == shop_id) & (user_view['time_stamp']
                                                               .str.startswith(date))]['user_id'])
            if i == 0:
                data[shop_id][i] = 1.0
            else:
                data[shop_id][i] = len(active_users.intersection(shop_viewers)) / len(shop_viewers)

    print('可视化处理')
    x_data = [f'2016-{month:02d}' for month in range(4, 11)]
    y_data = np.array([[round(data[shop_id][i] * 100, 2) for i in range(31)] for shop_id in top_3_shops])
    shop_ids = [f'商家{shop_id}' for shop_id in top_3_shops]

    l = (
        Line(init_opts=opts.InitOpts(width="1000px", height="700px"))
        .add_xaxis(x_data)
        .add_yaxis(shop_ids[0], y_data[0].tolist(), is_smooth=True)
        .add_yaxis(shop_ids[1], y_data[1].tolist(), is_smooth=True)
        .add_yaxis(shop_ids[2], y_data[2].tolist(), is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='留存分析'),
            yaxis_opts=opts.AxisOpts(name='留存率(%)')
        )
    )
    l.render(r'./result/留存分析.html')


if __name__ == "__main__":
    file1 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/shop_info.txt'
    file2 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/user_pay.txt'
    file3 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/user_view.txt'
    line(file1, file2, file3)
