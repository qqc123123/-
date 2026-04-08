# -*- coding:utf-8 -*-
'''
    @Project   :邱杰成202330906124
    @FileName  :3. 统计最受欢迎的前 10 类商品（按照二级分类统计），并输出他们的人均消费（选择合适图表对其可视化，类似排行榜）.py
    @Time      :2024/12/26-13:31
    @Author    :Lenovo
'''


import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar


def bar(file1, file2):
    print('正在读取数据...')
    shop_info_columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt','shop_level', 'cate_1_name', 'cate_2_name', 'cate_3_name']
    user_pay_columns = ['user_id', 'shop_id', 'time_stamp']
    shop_info = pd.read_csv(file1, encoding='utf-8', header=None,names=shop_info_columns)
    user_pay = pd.read_csv(file2, encoding='utf-8', header=None, names=user_pay_columns)
    print('数据读取完毕...')

    print('计算交易次数和人均消费...')
    user_pay_grouped = user_pay.groupby('shop_id').agg({'time_stamp': 'count'}).reset_index()
    user_pay_grouped.rename(columns={'time_stamp': 'count'}, inplace=True)
    user_pay_grouped = user_pay_grouped.merge(shop_info[['shop_id', 'cate_2_name', 'per_pay']],
                                              on='shop_id',
                                              how='left')
    cate_2 = user_pay_grouped.groupby('cate_2_name').agg({'per_pay': 'mean', 'count': 'sum'}).reset_index()

    print('选择前10...')
    top_10 = cate_2.sort_values(by='count', ascending=False).head(10).round(3)

    # 构建排行榜
    b = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add_xaxis(top_10['cate_2_name'].tolist())
        .add_yaxis('人均消费', top_10['per_pay'].tolist())
        .add_yaxis('交易次数', top_10['count'].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="最受欢迎的前10类商品及其人均消费和交易次数"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            yaxis_opts=opts.AxisOpts(name="数值"),
            datazoom_opts=[
                opts.DataZoomOpts(),
                opts.DataZoomOpts(type_="inside")
            ]
        )
    )

    b.render(r'./result/3.最受欢迎商品top_10.html')
    top_10.to_excel(r'./result/3.最受欢迎商品top_10.xlsx')
    print("排行榜图表已生成并保存为 '3.最受欢迎商品.html'")
    print("数据保存为excel文件输出：'3.最受欢迎商品top_10.xlsx'")


if __name__ == "__main__":
    file1 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/shop_info.txt'
    file2 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/user_pay.txt'
    bar(file1, file2)

