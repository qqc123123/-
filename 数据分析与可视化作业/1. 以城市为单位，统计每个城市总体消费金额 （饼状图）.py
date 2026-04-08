# -*- coding:utf-8 -*-
'''
    @Project   :邱杰成202330906124
    @FileName  :1. 以城市为单位，统计每个城市总体消费金额 （饼状图）.py
    @Time      :2024/12/26-10:39
    @Author    :Lenovo
'''


import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts


def pie(file):
    print('正在读取数据...')
    columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt', 'shop_level', 'cate_1_name', 'cate_2_name', 'cate_3_name']
    df = pd.read_csv(file, sep=",", header=None, names=columns, encoding='utf-8')
    c = df.groupby('city_name')['per_pay'].sum()
    print('数据读取完毕...')

    print('进行可视化处理...')
    # 创建饼状图对象
    p = (
        Pie(init_opts=opts.InitOpts(width="1200px", height="700px"))
        .add('总体消费金额',
             [list(z) for z in zip(c.index.tolist(), c.values.tolist())],
             radius=['20%', '55%'],  # 设置为环形饼状图
             center=['36%', '50%'],  # 饼状图的位置
             rosetype='radius'
             )
        .set_global_opts(title_opts=opts.TitleOpts(title='城市总体消费金额分布'),  # 全局标题
                         legend_opts=opts.LegendOpts(orient='horizontal', pos_top='20%', pos_left='66%'))  # 图例配置
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )

    p.render(r'./result/1.每个城市总体消费金额分布.html')
    c.to_excel(r'./result/1.每个城市总体消费金额分布.xlsx')
    print("饼状图已生成并保存为 '1.每个城市总体消费金额分布.html'")
    print("数据保存为excel文件输出：'1.每个城市总体消费金额分布.xlsx'")


if __name__ == "__main__":
    file = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/shop_info.txt'
    pie(file)
