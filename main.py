import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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