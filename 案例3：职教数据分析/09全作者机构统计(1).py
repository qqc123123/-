# -*- coding:utf-8 -*-
'''
    @Project   :python 
    @FileName  :09全作者机构统计.py
    @Time      :2024/11/15-11:19
    @Author    :Lenovo
'''
import pandas as pd
import numpy as np
import re
from collections import Counter

def get_all_org(text):
    # 正则表达式模式，匹配大学、学校、学院、研究院、中心、考试院、学会、教育工委、司、教育局、协会、工程院、委员会、评估院、党校、教育厅、出版社、研究所、中学、教育社、职教社
    pattern = r'([\u4e00-\u9fa5]+大学|[\u4e00-\u9fa5]+学校|[\u4e00-\u9fa5]+学院|[\u4e00-\u9fa5]+研究院|[\u4e00-\u9fa5]+中心|[\u4e00-\u9fa5]+考试院|[\u4e00-\u9fa5]+学会|[\u4e00-\u9fa5]+学会|[\u4e00-\u9fa5]+教育工委|[\u4e00-\u9fa5]+司|[\u4e00-\u9fa5]+教育局|[\u4e00-\u9fa5]+协会|[\u4e00-\u9fa5]+工程院|[\u4e00-\u9fa5]+委员会|[\u4e00-\u9fa5]+评估院|[\u4e00-\u9fa5]+教育厅|[\u4e00-\u9fa5]+出版社|[\u4e00-\u9fa5]+研究所|[\u4e00-\u9fa5]+中学|[\u4e00-\u9fa5]+教育社|[\u4e00-\u9fa5]+职教社)'

    matches = re.findall(pattern, text)
    return matches


def main(file):
    df = pd.read_excel(file)
    df['所有单位'] = df['作者单位'].map(get_all_org)
    # print(df[['作者单位', '所有单位']].head(10))

    all_kinds = []
    for kinds in df['所有单位']:
        all_kinds.extend(kinds)
    # print(all_kinds)
    kind_freq = Counter(all_kinds).most_common()
    df_counts = pd.DataFrame(data=kind_freq, columns=['机构', '次数'])
    print(df_counts)
    df_counts.to_csv(r'.\result\全作者机构统计.csv')

if __name__ == "__main__":
    file = r'./result/职教脱敏_分词处理.xlsx'
    main(file)
