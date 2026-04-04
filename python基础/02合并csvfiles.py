# -*- coding:utf-8 -*-
'''
    @Project   :2024春 
    @FileName  :02合并csvfiles.py
    @Time      :2024/6/17-16:18
    @Author    :Administrator--野牛首领
'''


import os, os.path
import wordcloud
import matplotlib.pyplot as plt

def merge_csvfiles(path):
    # step1:遍历所有文件
    csv_dict1 = {}
    files = [os.path.join(path, file) for file in os.listdir(path)]


    # step2:读取每一个csv文件的内容，转换成字典，并将每一个文件对应的字典合并到总字典中
    for i, file in enumerate(files, start=1):
        print(f'正在处理第{i}/{len(files)}个文件{file}...')
        try:
            with open(file, 'r', encoding='utf-8') as fr:
                fr.readline()
                csv_dict2 = {item.split(',')[0]: int(item.split(',')[1]) for item in fr.read().strip().split('\n')}
            for k, v in csv_dict2.items():
                if v > 5:
                    csv_dict1[k] = csv_dict1.get(k, 0) + v

            with open(r'./result/mearge_csv.csv', 'w', encoding='utf-8') as fw:
                for k, v in sorted(csv_dict1.items(), key=lambda x: x[1], reverse=True):
                    fw.write(f'{k}, {v}\n')

        except Exception as e:
            print('发生错误，错误信息已经记录！', end='')
            with open(r'./result/csv文件处理失败记录.txt', 'a', encoding='utf-8') as f:
                f.write(f'{file}, {e}\n')
            print('结束')


    # step3: 作词云图（哪种方法都可以,词云以文件的形式存储于result目录下)

    dic = {}
    n = 0
    for k, v in sorted(csv_dict1.items(), key=lambda x: x[1], reverse=True):
        n += 1
        if n <= 50:
            dic[k] = v

    font_path = r'c:/windows/Fonts/STXINGKA.TTF'  # 规定字体格式
    wc = wordcloud.WordCloud(font_path=font_path,
                             max_words=50,
                             background_color='white',
                             width=2000,
                             height=2000)
    wc.generate_from_frequencies(dic)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(r'./result/合并词频后的词云图.png', dpi=600)  # 将词云图存入磁盘指定位置
    plt.show()


if __name__ == "__main__":
    path = r'./csvfiles'
    merge_csvfiles(path)

