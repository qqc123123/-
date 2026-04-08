# -*- coding:utf-8 -*-
'''
    @Project   :邱杰成202330906124 
    @FileName  :7. 找到被浏览次数最多的 50 个商家，并输出他们的城市以及人均消费，并选择合适的图表对结果进行可视化.py
    @Time      :2024/12/29-19:40
    @Author    :Lenovo
'''


import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts


def bar(file1, file2):
    print('正在读取数据...')
    user_view_columns = ['user_id', 'shop_id', 'time_stamp']
    shop_info_columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt', 'shop_level', 'cate_1_name', 'cate_2_name', 'cate_3_name']
    user_view = pd.read_csv(file1, encoding='utf-8', header=None, names=user_view_columns)
    shop_info = pd.read_csv(file2, encoding='utf-8', header=None, names=shop_info_columns)
    print('数据读取完毕...')

    print('统计浏览次数...')
    view_count = user_view['shop_id'].value_counts().reset_index()
    view_count.columns = ['shop_id', 'view_times']

    print('合并数据,缺失值填充为0...')
    merged_data = pd.merge(shop_info, view_count, on='shop_id', how='right')
    merged_data['per_pay'].fillna(0, inplace=True)

    print('降序排序，取前50个...')
    top_50_shops = merged_data.sort_values(by='view_times', ascending=False).head(50)

    print('x轴...')
    x_axis_data = [f"{shop_id}({city})" for shop_id, city in zip(top_50_shops['shop_id'], top_50_shops['city_name'])]

    print('进行可视化处理...')
    b = (
        Bar(init_opts=opts.InitOpts(width="1500px", height="600px"))
        .add_xaxis(x_axis_data)
        .add_yaxis('浏览次数', top_50_shops['view_times'].tolist(), itemstyle_opts=opts.ItemStyleOpts(color='#5793f3'))
        .add_yaxis('人均消费', top_50_shops['per_pay'].tolist(), itemstyle_opts=opts.ItemStyleOpts(color='#d14a61'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title='被浏览次数最多的50个商家'),
            legend_opts=opts.LegendOpts(orient='vertical', pos_right='5%'),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60, font_size=8)),
            yaxis_opts=opts.AxisOpts(name='数值'),
            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross')
        )
    )

    b.render(r'./result/7.top_50_shops.html')
    top_50_shops.to_excel(r'./result/7.top_50_shops.xlsx')
    print("可视化处理已生成并保存为 '7.top_50_shops.html'")
    print("数据保存为excel文件输出：'7.top_50_shops.xlsx'")


if __name__ == "__main__":
    file1 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/user_view.txt'
    file2 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/shop_info.txt'
    bar(file1, file2)


