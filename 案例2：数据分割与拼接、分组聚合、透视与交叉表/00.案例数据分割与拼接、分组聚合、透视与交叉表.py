import pandas as pd

if __name__ == '__main__':
    df0 = pd.read_excel(r'./任务05.xlsx', sheet_name='利润表20')
    df1 = pd.read_excel(r'./任务05.xlsx', sheet_name='利润表21')
    df2 = pd.read_excel(r'./任务05.xlsx', sheet_name='房屋销售数据20')
    df3 = pd.read_excel(r'./任务05.xlsx', sheet_name='房屋销售数据21')
    df4 = pd.read_excel(r'./任务05.xlsx', sheet_name='销售代表编码表')
    # print(df4)

    dff0 = pd.merge(df0, df1, how='outer')
    dff0 = dff0.groupby(by='月').sum()
    dff0 = dff0.drop('年', axis=1)
    dff0.diff(periods=1)
    dff0 = dff0.pct_change(1).round(4)
    # print(dff0)

    dff1 = pd.merge(df2, df3, how='outer')
    dff1['提成'] = dff1['销售数量'] * 800
    dff1['收入'] = dff1['提成'] + dff1['底薪']
    # print(dff1)

    dff2 = pd.merge(dff1, df4, on='销售代表编码')
    # print(dff2)

    dff3 = dff2.groupby(by=['年']).agg({'销售数量': 'sum'})
    # print(dff3)

    dff4 = dff2.groupby(by=['姓名']).agg({'收入': 'sum'})
    dff4 = dff4.sort_values(by=['收入'], ascending=False)
    # print(dff4)

    dff5 = dff2.groupby(by=['性别']).agg({'提成': 'mean'}).round(2)
    # print(dff5)

    dff6 = dff2.groupby(by=['姓名']).agg({'销售数量': 'sum', '提成': 'mean'})
    dff6['提成'] = dff6['提成'].round(2)
    # print(dff6)

    dff7 = dff2.groupby(by=['姓名']).agg({'销售数量': 'sum', '收入': 'mean'})
    dff8 = dff2.groupby(by=['姓名']).agg({'销售数量': 'mean', '收入': 'max'})
    dff9 = dff2.groupby(by=['姓名']).agg({'收入': 'min'})
    dff7 = dff7.rename(columns={'销售数量': '销售数量sum', '收入': '收入mean'})
    dff8 = dff8.rename(columns={'销售数量': '销售数量mean', '收入': '收入max'})
    dff9 = dff9.rename(columns={'收入': '收入min'})
    dff7['收入mean'] = dff7['收入mean'].round(2)
    dff8['销售数量mean'] = dff8['销售数量mean'].round(2)
    dff10 = pd.merge(dff7, dff8, on='姓名')
    dff11 = pd.merge(dff10, dff9, on='姓名')
    # print(dff11)

    dff12 = pd.crosstab(index=dff2['年'], columns=dff2['姓名'], values=dff2['提成'], aggfunc='sum')
    # print(dff12)

    dff13 = pd.crosstab(index=dff2['姓名'], columns=dff2['月'], values=dff2['销售数量'], aggfunc='sum')
    # print(dff13)

    dff14 = pd.crosstab(index=dff2['姓名'], columns=dff2['月'], values=dff2['销售数量'], aggfunc='sum', margins=True, margins_name='合计')
    # print(dff14)

    dff15 = pd.crosstab(index=dff2['年'], columns=dff2['姓名'], values=dff2['收入'], aggfunc='sum', margins=True, margins_name='ALL')
    # print(dff15)

    dff16 = pd.crosstab(index=dff2['年'], columns=dff2['姓名'], values=dff2['提成'], aggfunc='sum', margins=True, margins_name='ALL')
    # print(dff16)


    dfs = [dff0, dff1, dff2, dff3, dff4, dff5, dff6, dff7, dff8, dff9, dff9, dff10, dff11, dff12, dff13, dff14, dff15, dff16]
    sheet_names = ['表0', '表1', '表2', '表3', '表4', '表5', '表6', '表7','表8', '表9', '表10', '表11', '表12', '表13', '表14', '表15', '表16']
    with pd.ExcelWriter(r'E:\课程文件\商务数据分析\案例2：数据分割与拼接、分组聚合、透视与交叉表\处理后任务05.xlsx') as writer:
        for df, sheet_name in zip(dfs, sheet_names):
            df.to_excel(writer, sheet_name=sheet_name)



