# pandasをimportする。
# read_excel()関数でExcelファイルを取り込み、データフレームを生成する。
import pandas as pd

NOV_df = pd.read_excel('sample.xlsx', sheet_name='2020年11月') 

# データフレームの先頭5行を確認する。
NOV_df.head()

# 各データ型を確認する。
NOV_df.dtypes

# データ型を変更する。（int→float）
NOV_df.loc[:, '貨物重量'] = NOV_df.loc[:, '貨物重量'].astype(float)

# 各データ型を確認する。
NOV_df.dtypes

# 要約統計量を確認する。
NOV_df.describe()

# 旅客数の平均値を確認する。
NOV_df.loc[:, '旅客数'].mean()

# 旅客数の中央値を確認する。
NOV_df.loc[:, '旅客数'].median()


# 旅客数の（標本）標準偏差を確認する。
# 母集団の標準偏差を確認したい場合は、引数に ddof=0 を指定する。
NOV_df.loc[:, '旅客数'].std()

# 旅客数の最頻値を確認する。
NOV_df.mode().loc[0, '旅客数']

# 12月のデータフレームを作成する。
DEC_df = pd.read_excel('sample.xlsx', sheet_name='2020年12月') 

# 11月と12のデータフレームを結合する。
df = pd.concat([NOV_df, DEC_df], axis=0, ignore_index=True)

# 結合したデータフレームの中身を確認する。
df.head()

# 結合したデータフレームの中身を確認する。
df.tail()

# 日付列をindexに設定する。
df = df.set_index('日付')

# 確認する。
df.head()

# 元のデータフレームを書き換える場合は、引数にinplace=Trueを追加する。
df.set_index('日付', inplace=True)

# resampleメソッドで日付単位の集計を行う。
df_daily_sum = df.resample('D').sum()

#中身を確認する。
df_daily_sum.head()

# 結果をExcelに書き出す。
df_daily_sum.to_excel('df_daily_sum.xlsx')

# groupbyメソッドで周期的にデータをまとめる。
df.groupby(pd.Grouper(freq='M')).mean()

# 月曜日基準でまとめたデータフレームを作成する。
MON_df = df.groupby(pd.Grouper(freq='W-MON')).sum()

MON_df

# 到着空港がCTSのデータフレームを作成する。
CTS_df = df[df.loc[:, '到着空港'] == 'CTS']

CTS_df.head()

# 便名がABC011のデータフレームを作成する。
ABC_011 = df[df.loc[:, '便名'] == 'ABC011']

ABC_011.head()

# 旅客数が150以上のデータを抽出する。
df[df.loc[:, '旅客数'] >= 150]

# 到着空港が、CTSかAKJのデータにデータを抽出する。
CTS_AKJ = df.query('到着空港 == "CTS" or 到着空港 == "AKJ"')

CTS_AKJ.head()

# 到着空港がTOY、旅客数が150以上のデータを抽出する。
df.query('到着空港 == "TOY" and 旅客数 >= 150')

# 到着空港がOKA、貨物重量が15000以上のデータを抽出する。
df[(df.loc[:, '到着空港'] == 'OKA') & (df.loc[:, '貨物重量'] >= 15000)]

# 到着空港がFUK、またはOKAのデータを抽出する。
df[(df.loc[:, '到着空港'] == 'FUK') | (df.loc[:, '到着空港'] == 'OKA')]

# 日付が2020年11月10日から2020年12月10日のデータを抽出する。
df['2020-11-10': '2020-12-10']

# 日付が2020年11月25日から2020年12月05日で到着空港がHIJのデータを抽出する。
df.query('"2020-11-25" <= index <= "2020-12-05" and 到着空港 == "HIJ"')

# ↑の処理を分割する場合
df_1125_1205 = df['2020-11-25': '2020-12-05']

df_1125_1205[df_1125_1205.loc[:, '到着空港'] == 'HIJ']

# グラフを描画するためにmatplotlibを、
# 反映文字を日本語にするためにjapanize_matplotlibをimportする。
import matplotlib.pyplot as plt
import japanize_matplotlib

# pandasのplotメソッドでグラフを描画してみる。
df_daily_sum.plot()
plt.show()

# 折れ線グラフを描画する。
fig, ax = plt.subplots()

x = [i for i in range(1, 62)]

ax.plot(x, df_daily_sum.loc[:, '旅客数'], label='旅客数')
ax.set_xlabel('11月1日-12月31日')
ax.legend(loc='best')
ax.grid()

plt.show()

# X軸の目盛りに日付を表示して折れ線グラフを描画する。
fig, ax = plt.subplots(figsize=(9, 3))

x = pd.date_range(start='2020-11-01', end='2020-12-31')
# = df_daily_sum.indexと同じ

ax.plot(x, df_daily_sum.loc[:, '貨物重量'], label='貨物重量', 
        color='orange')
ax.set_ylabel('重量')
ax.legend(loc='best')
ax.grid()

plt.xticks(x, rotation=90)
plt.show()

# 1つの描画プロットに複数の折れ線グラフを描画する。
fig, ax = plt.subplots(nrows=2, figsize=(9, 6))

x = pd.date_range(start='2020-11-01', end='2020-12-31')

ax[0].plot(x, df_daily_sum.loc[:, '旅客数'], label='旅客数')
ax[0].legend(loc='best')
ax[0].grid()
ax[0].set_xticks(x)
plot1_labels = ax[0].get_xticklabels()
plt.setp(plot1_labels, rotation=90)

ax[1].plot(x, df_daily_sum.loc[:, '貨物重量'], label='貨物重量')
ax[1].legend(loc='best')
ax[1].grid()
ax[1].set_xticks(x)
plot2_labels = ax[1].get_xticklabels()
plt.setp(plot2_labels, rotation=90)

plt.tight_layout()
plt.show()

# 散布図を描画する。
fig, ax = plt.subplots()

x = df_daily_sum.loc[:, '旅客数']
y = df_daily_sum.loc[:, '貨物重量']

ax.scatter(x, y)
ax.set_title('旅客数/貨物重量')
ax.set_xlabel('旅客数')
ax.set_ylabel('貨物重量')
ax.grid()

plt.show()

# 棒グラフを描画する。
fig, ax = plt.subplots(figsize=(10,3))

x = pd.date_range('2020-11-01', '2020-12-31')

ax.bar(x, df_daily_sum.loc[:, '旅客数'])
ax.set_title('サブプロットのタイトル')
ax.grid()

plt.xticks(x, rotation=90) 
plt.suptitle('描画オブジェクトのタイトル')
plt.tight_layout()
plt.show()

# Y軸の目盛りを設定した棒グラフを描画する。
fig, ax = plt.subplots(figsize=(10,3))

x = pd.date_range('2020-11-01', '2020-12-31')

ax.bar(x, df_daily_sum.loc[:, '貨物重量'])

plt.xticks(x, rotation=90)
plt.ylim(ymin=60000) 
plt.show()

# ヒストグラムを描画する。
# ヒスとメソッドの返り値を使って度数分布表を表示する。
fig, ax = plt.subplots()

x = df_daily_sum.loc[:, '旅客数']

num, bin, void = ax.hist(x)

plt.show()

for i, j in enumerate(num):
    print('{:.1f} {:.1f} : {}'.format(bin[i], bin[i+1], j))