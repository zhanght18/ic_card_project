张瀚天-25361047-第三次人工智能编程作业

一.    任务拆解与 AI 协作策略

在本次作业中，我将六项分析任务分步拆解，每步与 AI 协作完成：

1. 任务1 数据预处理
读取 CSV 文件、解析交易时间、构造 ride_stops。
修正实际分隔符（CSV 是逗号分隔）。
2. 任务2 时间分布分析
用 numpy 统计早峰前和深夜刷卡量。
用 matplotlib 绘制 24 小时刷卡量柱状图，早晚高亮。
3. 任务3 线路站点分析
封装 analyze_route_stops 函数。
seaborn 绘制前15条线路水平条形图，显示标准差。
4. 任务4 高峰小时系数 PHF
自动识别高峰小时。
5 分钟和 15 分钟粒度统计最大刷卡量，计算 PHF5 和 PHF15。
5. 任务5 线路驾驶员信息批量导出
筛选 1101~1120 的线路。
为每条线路生成 txt 文件，记录车辆编号 → 驾驶员编号对应关系。
6. 任务6 服务绩效排名与热力图
分析 Top10 司机、线路、上车站点、车辆。
用 seaborn 绘制 4×10 热力图，标注服务人次。

每完成一个任务就 commit，并逐步验证代码和可视化结果，保证符合评分标准。

二.    核心 Prompt 迭代记录
1. 任务2 matplotlib 中文显示
初代 Prompt：柱状图中文乱码
优化 Prompt：增加 plt.rcParams['font.sans-serif'] = ['SimHei'] 和早晚红色高亮
2. 任务3 seaborn 条形图
初代 Prompt：线路号当作数值
优化 Prompt：转换为字符串再画图
3. 任务4 PHF
初代 Prompt：固定高峰小时
优化 Prompt：自动查找最大刷卡量小时并用 resample 统计

三.    Debug 记录
1. 任务1 时间列 KeyError
原因：CSV 文件实际是逗号分隔
解决：修改 sep=','
2. 任务2 中文字体乱码
原因：matplotlib 默认字体不支持中文
解决：plt.rcParams['font.sans-serif'] = ['SimHei']
3. 任务3 条形图纵轴异常
原因：线路号数字被 seaborn 当作连续数值
解决：top15_routes['线路号'] = top15_routes['线路号'].astype(str)
4. GitHub push 连接中断
原因：网络波动或代理问题
解决：更换网络或多次 push，本地 commit 已保存
