# -*- coding:utf-8 -*-
'''
    @Project   :案例4：招聘网站数据分析 
    @FileName  :6、与数据分析相关技能分析’.py
    @Time      :2024/11/20-23:53
    @Author    :Lenovo
'''


import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    df = pd.read_excel(r'./result/招聘数据清洗.xlsx')


    skills = ['LR', '神策', '聚类', 'GBDT', 'SAS', 'NLP', 'Html', 'Shell', 'Caffe', '金融', 'Tensorflow', 'Hbase',
              'Oracle', 'Mapreduce', 'Nodejs', 'Storm', 'SQL', 'Congos', '决策树', 'Python', 'Impala', 'Excel',
              'Superset', 'Abtest', 'Highcharts', 'Kettle', '算法', '大数据', '数据挖掘', '风控', 'Kafka', 'SPSS',
              'Datastage', '数据结构', '回归', 'Presto', 'Ruby', 'Flume', 'Flink', 'Bi', 'Spark', '可视化', 'Scala',
              'Hive', '模型设计', 'Tableau', 'Hql', 'Etl', 'D3', 'Powerpoint', 'Echarts', '机器学习']
    skill_counts = df['parse2_job_detail'].apply(lambda x: sum([skill in x for skill in skills])).value_counts().sort_index()
    print(skill_counts)

    # 输出并存储柱形图
    skill_counts.plot(kind='bar')
    plt.xlabel('技能点')
    plt.ylabel('出现频率')
    plt.title('数据分析相关技能出现频率')
    plt.xticks(rotation=90)  # Rotate x-axis labels to make them readable
    plt.savefig(r'./result/数据分析相关技能频率图.png')
    plt.show()