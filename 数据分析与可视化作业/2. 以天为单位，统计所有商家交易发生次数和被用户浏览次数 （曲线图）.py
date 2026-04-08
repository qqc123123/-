# -*- coding:utf-8 -*-
'''
    @Project   :邱杰成202330906124 
    @FileName  :2. 以天为单位，统计所有商家交易发生次数和被用户浏览次数 （曲线图）.py
    @Time      :2024/12/30-13:10
    @Author    :Lenovo
'''


import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts


def line(file1, file2):
    print('正在读取数据...')
    user_pay_columns = ['user_id', 'shop_id', 'time_stamp']
    user_view_columns = ['user_id', 'shop_id', 'time_stamp']
    user_pay = pd.read_csv(file1, encoding='utf-8', header=None, names=user_pay_columns)
    user_view = pd.read_csv(file2, encoding='utf-8', header=None, names=user_view_columns)
    print('数据读取完毕...')

    user_pay['time_stamp'] = pd.to_datetime(user_pay['time_stamp']).dt.date
    user_view['time_stamp'] = pd.to_datetime(user_view['time_stamp']).dt.date
    print('时间转换格式完成...')

    transaction_count = user_pay['time_stamp'].value_counts().sort_index()
    print('统计交易次数...')

    browse_count = user_view['time_stamp'].value_counts().sort_index()
    print('统计浏览次数...')
    date_range = pd.date_range(start='2015-07-01', end='2016-10-31').date

    transaction_count = transaction_count.reindex(date_range, fill_value=None)
    browse_count = browse_count.reindex(date_range, fill_value=None)
    print('缺失值填充为空值...')

    print('进行可视化处理...')
    l = (
        Line(init_opts=opts.InitOpts(width="1500px", height="550px"))
        .add_xaxis(transaction_count.index.astype(str).tolist())
        .extend_axis(
            yaxis=opts.AxisOpts(
                name='交易发生次数',
                position='right',
                axislabel_opts=opts.LabelOpts(formatter='{value} 次')
            )
        )
        .add_yaxis('交易发生次数', transaction_count.values.tolist(), yaxis_index=1)
        .add_yaxis('浏览次数', browse_count.values.tolist(), yaxis_index=0)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='每日交易发生次数和浏览次数统计',
                # subtitle='数据范围：2015-07-01 至 2016-10-31',
                pos_left='center'),
            xaxis_opts=opts.AxisOpts(name='日期', axislabel_opts=opts.LabelOpts(rotate=-60)),
            yaxis_opts=opts.AxisOpts(name='浏览次数', axislabel_opts=opts.LabelOpts(formatter='{value} 次')),
            tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
            legend_opts=opts.LegendOpts(pos_top='5%', pos_left='center')
        )
    )

    l.render(r'./result/2.所有商家的交易次数和浏览次数（单位：天）.html')
    print("输出结果：'2.所有商家的交易次数和浏览次数（单位：天）.html'")

    print('合并数据...')
    df = pd.DataFrame({
        '日期': transaction_count.index.astype(str),
        '交易发生次数': transaction_count.values,
        '浏览次数': browse_count.values
    })

    df.to_excel(r'./result/2.所有商家的交易次数和浏览次数（单位：天）.xlsx', index=False)
    print("数据保存为excel文件输出：'2.所有商家的交易次数和浏览次数（单位：天）.xlsx'")


if __name__ == "__main__":
    file1 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/user_pay.txt'
    file2 = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/user_view.txt'
    line(file1, file2)


