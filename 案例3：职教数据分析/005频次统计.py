# -*- coding:utf-8 -*-
'''
    @Project   :案例3：职教数据分析 
    @FileName  :005频次统计.py
    @Time      :2024/11/8-11:26
    @Author    :Lenovo
'''
import pandas as pd
from collections import Counter

def main(file):
    df = pd.read_excel(file)
    columns = ['关键词', '作者', '杂志名称', '一作姓名', '一作单位', '基金类型', '摘要_分词','主副标题_分词']
    for col in columns:
        print(f'正在统计{col}频次...', end='')
        all_words = []
        for item in df[col]:
            if isinstance(item, (int, float)) or item=='':
                continue
            all_words.extend(item.split(','))


        #统计频次
        word_freq = Counter(all_words).most_common()
        df_counts = pd.DataFrame(data=word_freq, columns=['word', 'freq'])

        #存储
        print(f'正在存储{col}频次...', end='')
        df_counts.to_excel(f'./result/{col}频次.xlsx', index=False)
        print('end!')

if __name__ == "__main__":
    file = r'./result/职教脱敏_分词处理.xlsx'
    main(file)
