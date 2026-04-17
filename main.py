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

# 任务3：线路站点分析
# =========================

def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    """
    计算各线路乘客的平均搭乘站点数及其标准差。
    Parameters
    ----------
    df : pd.DataFrame  预处理后的数据集
    route_col : str    线路号列名
    stops_col : str    搭乘站点数列名
    Returns
    -------
    pd.DataFrame  包含列：线路号、mean_stops、std_stops，按 mean_stops 降序排列
    """
    result = df.groupby(route_col)[stops_col].agg(
        mean_stops='mean',
        std_stops='std'
    ).reset_index()

    result = result.sort_values(by='mean_stops', ascending=False)
    return result


# 调用函数
route_result = analyze_route_stops(df)

print("各线路平均搭乘站点数及标准差（前10行）：")
print(route_result.head(10))

# 取前15条线路
top15_routes = route_result.head(15).copy()

# 把线路号转成字符串，防止 seaborn 当成连续数值
top15_routes['线路号'] = top15_routes['线路号'].astype(str)

plt.figure(figsize=(12, 8))

ax = sns.barplot(
    data=top15_routes,
    x='mean_stops',
    y='线路号',
    palette='Blues_d'
)

# 手动添加误差棒
plt.errorbar(
    x=top15_routes['mean_stops'],
    y=np.arange(len(top15_routes)),
    xerr=top15_routes['std_stops'],
    fmt='none',
    ecolor='black',
    capsize=3
)

plt.title("平均搭乘站点数最高的前15条线路")
plt.xlabel("平均搭乘站点数")
plt.ylabel("线路号")
plt.xlim(left=0)

plt.tight_layout()
plt.savefig("route_stops.png", dpi=150)
plt.show()

# 任务4：高峰小时系数计算
# =========================

# 只统计上车刷卡记录
board_df = df[df['刷卡类型'] == 0].copy()

# 1. 统计全天各小时刷卡量，找出高峰小时
hour_counts = board_df.groupby('hour').size()
peak_hour = hour_counts.idxmax()
peak_hour_count = hour_counts.max()

print(f"高峰小时：{peak_hour:02d}:00 ~ {peak_hour + 1:02d}:00，刷卡量：{peak_hour_count} 次")

# 2. 取出高峰小时内的数据
peak_df = board_df[board_df['hour'] == peak_hour].copy()

# 把交易时间设为索引，便于按时间窗口重采样
peak_df = peak_df.set_index('交易时间').sort_index()

# 3. 按5分钟粒度统计
count_5min = peak_df.resample('5min').size()

max_5 = count_5min.max()
max_5_start = count_5min.idxmax()
max_5_end = max_5_start + pd.Timedelta(minutes=5)

PHF5 = peak_hour_count / (12 * max_5)

print(f"最大5分钟刷卡量（{max_5_start.strftime('%H:%M')}~{max_5_end.strftime('%H:%M')}）：{max_5} 次")
print(f"PHF5  = {peak_hour_count} / (12 × {max_5}) = {PHF5:.4f}")

# 4. 按15分钟粒度统计
count_15min = peak_df.resample('15min').size()

max_15 = count_15min.max()
max_15_start = count_15min.idxmax()
max_15_end = max_15_start + pd.Timedelta(minutes=15)

PHF15 = peak_hour_count / (4 * max_15)

print(f"最大15分钟刷卡量（{max_15_start.strftime('%H:%M')}~{max_15_end.strftime('%H:%M')}）：{max_15} 次")
print(f"PHF15 = {peak_hour_count} / ( 4 × {max_15}) = {PHF15:.4f}")

# 任务5：线路驾驶员信息批量导出
# =========================

import os

# 目标线路
target_routes = list(range(1101, 1121))

# 创建文件夹
folder_path = "线路驾驶员信息"
os.makedirs(folder_path, exist_ok=True)

# 筛选目标线路数据
subset = df[df['线路号'].isin(target_routes)].copy()

# 遍历每条线路
for route in target_routes:
    route_data = subset[subset['线路号'] == route]

    # 车辆-驾驶员去重
    pairs = route_data[['车辆编号', '驾驶员编号']].drop_duplicates()

    # 写入文件
    file_path = os.path.join(folder_path, f"{route}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"线路号: {route}\n")
        f.write("车辆编号\t驾驶员编号\n")
        for _, row in pairs.iterrows():
            f.write(f"{row['车辆编号']}\t{row['驾驶员编号']}\n")

    print(f"生成文件：{file_path}")

