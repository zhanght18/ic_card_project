import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ====== 任务1：数据预处理 ======
# 1. 读取数据（注意分隔符是\t）
df = pd.read_csv('ICData.csv')

# 查看前5行
print(df.head())

# 查看数据基本信息
print(df.info())

# 2. 时间解析：转换为 datetime 类型
df['交易时间'] = pd.to_datetime(df['交易时间'])

# 提取小时字段
df['hour'] = df['交易时间'].dt.hour

# 3. 构造“搭乘站点数”
df['ride_stops'] = (df['下车站点'] - df['上车站点']).abs()

# 删除 ride_stops 为 0 的异常数据
before = len(df)
df = df[df['ride_stops'] != 0]
after = len(df)

print("删除的异常记录数：", before - after)

# 4. 缺失值检查
print("缺失值统计：")
print(df.isnull().sum())

# 简单处理：删除缺失值
df = df.dropna()

print("数据预处理完成")


# ====== 任务2：时间分析 ======
# 统计每小时刷卡量（只统计上车）
hour_counts = df[df['刷卡类型'] == 0]['hour'].value_counts().sort_index()

plt.figure(figsize=(10,6))

# 颜色控制
colors = ['blue'] * 24
for i in range(24):
    if i < 7 or i >= 22:
        colors[i] = 'red'

plt.bar(hour_counts.index, hour_counts.values, color=colors)

plt.xticks(range(0,24,2))
plt.xlabel("小时")
plt.ylabel("刷卡量")
plt.title("24小时刷卡分布")
plt.grid(axis='y')

plt.savefig("hour_distribution.png", dpi=150)
plt.show()