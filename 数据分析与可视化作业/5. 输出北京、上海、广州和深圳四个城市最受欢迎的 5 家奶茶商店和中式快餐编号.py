# -*- coding:utf-8 -*-
'''
    @Project   :邱杰成202330906124
    @FileName  :5. 输出北京、上海、广州和深圳四个城市最受欢迎的 5 家奶茶商店和中式快餐编号.py
    @Time      :2024/12/26-14:58
    @Author    :Lenovo
'''


import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts


def bar(shops, shop_type):
    shop_names = shops['shop_id'].tolist()
    scores = shops['score'].tolist()
    per_pays = shops['per_pay'].astype(float).tolist()

    b = (
        Bar()
        .add_xaxis(shop_names)
        .add_yaxis("最受欢迎得分", scores, label_opts=opts.LabelOpts(is_show=False))
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="人均消费",
                type_="value",
                min_=0,
                max_=max(per_pays) + 1,
                interval=1,
                axislabel_opts=opts.LabelOpts(formatter="{value} 元")
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{shop_type}受欢迎程度及人均消费"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color="rgba(245, 245, 245, 0.8)",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000")
            )
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("人均消费",
                   per_pays,
                   yaxis_index=1,
                   label_opts=opts.LabelOpts(is_show=False)
                   )
    )

    b.render(f"./result/5.四个城市最受欢迎{shop_type}相关数据.html")
    print(f"可视化处理已生成并保存为 '5.四个城市最受欢迎{shop_type}相关数据.html'")


def main(file):
    print('正在读取数据...')
    shop_info_columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt', 'shop_level', 'cate_1_name', 'cate_2_name', 'cate_3_name']
    shop_info = pd.read_csv(file, sep=",", header=None, names=shop_info_columns, encoding='utf-8')
    print('数据读取完毕...')

    print('筛选北京、上海、广州和深圳的商家...')
    cities = ['北京', '上海', '广州', '深圳']
    city_shops = shop_info[shop_info['city_name'].isin(cities)]

    print('筛选出奶茶店和中式快餐店的数据...')
    milk_tea_shops = city_shops[city_shops['cate_3_name'].isin(['奶茶'])]
    chinese_fast_food_shops = city_shops[city_shops['cate_3_name'].isin(['中式快餐'])]

    print('计算最高消费金额...')
    max_per_pay = shop_info['per_pay'].astype(float).max()

    print('计算受欢迎程度得分...')
    milk_tea_shops['score'] = 0.7 * (milk_tea_shops['score'] / 5) + 0.3 * (milk_tea_shops['per_pay'] / max_per_pay)
    chinese_fast_food_shops['score'] = 0.7 * (chinese_fast_food_shops['score'] / 5) + 0.3 * (chinese_fast_food_shops['per_pay'] / max_per_pay)

    print('降序排序,选top_5')
    milk_tea_shops = milk_tea_shops.sort_values('score', ascending=False)
    chinese_fast_food_shops = chinese_fast_food_shops.sort_values('score', ascending=False)
    milk_tea_shops = milk_tea_shops.head(5)
    fast_food_shops = chinese_fast_food_shops.head(5)

    print('调用函数，可视化处理...')
    bar(milk_tea_shops, "奶茶店")
    bar(fast_food_shops, "中式快餐店")


if __name__ == "__main__":
    file = r'./2. 项目2-阿里巴巴口碑商家流量分析系统(光环个人项目)/阿里巴巴口碑商家流量分析系统数据/dataset/shop_info.txt'
    main(file)