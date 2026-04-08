# -*- coding:utf-8 -*-
'''
    @Project   :邱杰成202330906124 
    @FileName  :4. 平均日交易额最大的前 10 个商家，并输出他们各自的交易额，并选择合适的图表对结果进行可视化.py
    @Time      :2024/12/29-20:13
    @Author    :Lenovo
'''
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts


def bar(file1, file2):
    print('正在读取数据...')
    shop_info_columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt', 'shop_level','cate_1_name', 'cate_2_name', 'cate_3_name']
    user_pay_columns = ['user_id', 'shop_id', 'time_stamp']
    shop_info = pd.read_csv(file1, sep=",", header=None, names=shop_info_columns, encoding='utf-8')
    user_pay = pd.read_csv(file2, sep=",", header=None, names=user_pay_columns, encoding='utf-8')
    print('数据读取完毕...')

    print('时间转换格式...')
    user_pay['time_stamp'] = pd.to_datetime(user_pay['time_stamp'])

    print('计算平均日交易额...')
    zjy = user_pay.groupby('shop_id')['time_stamp'].count()
    pjjy = zjy / (user_pay['time_stamp'].max() - user_pay['time_stamp'].min()).days
    shop_info['pjjy'] = pjjy

    print('进行降序排序...')
    top_10_shops = shop_info.sort_values('pjjy', ascending=False).head(10).round(3)

    print('进行可视化处理...')
    b = (
        Bar()
        .add_xaxis(top_10_shops['shop_id'].tolist())
        .add_yaxis("平均日交易额", top_10_shops['pjjy'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title='平均日交易额前10商家'),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45))
                         )
    )

    b.render(r'./result/4.平均交易额top_10.html')
    top_10_shops.to_excel(r'./result/4.平均交易额top_10.xlsx')
    print("可视化处理已生成并保存为 '4.平均交易额top_10.html'")
    print("数据保存为excel文件输出：'4.平均交易额top_10.xlsx'")


if __name__ == "__main__":
    file1 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/shop_info.txt'
    file2 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/user_pay.txt'
    bar(file1, file2)