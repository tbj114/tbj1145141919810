#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图表功能
"""

import numpy as np
import pandas as pd
from axaltyx.charting.bar_chart import BarChart
from axaltyx.charting.line_chart import LineChart
from axaltyx.charting.scatter_chart import ScatterChart
from axaltyx.charting.histogram import Histogram
from axaltyx.charting.boxplot import BoxPlot
from axaltyx.charting.pie_chart import PieChart

# 测试数据
np.random.seed(42)
x = np.arange(10)
y = np.random.randn(10)
data = {
    '类别A': 30,
    '类别B': 25,
    '类别C': 20,
    '类别D': 15,
    '类别E': 10
}
multi_data = {
    '系列1': np.random.randn(20),
    '系列2': np.random.randn(20) + 1,
    '系列3': np.random.randn(20) + 2
}

# 测试柱状图
print("测试柱状图...")
barchart = BarChart()
barchart.set_title("测试柱状图")
barchart.set_xlabel("类别")
barchart.set_ylabel("数值")
barchart.plot(data)
barchart.save("test_barchart.png")
print("柱状图测试完成")

# 测试折线图
print("\n测试折线图...")
linechart = LineChart()
linechart.set_title("测试折线图")
linechart.set_xlabel("时间")
linechart.set_ylabel("数值")
linechart.plot(multi_data)
linechart.save("test_linechart.png")
print("折线图测试完成")

# 测试散点图
print("\n测试散点图...")
scatterchart = ScatterChart()
scatterchart.set_title("测试散点图")
scatterchart.set_xlabel("X轴")
scatterchart.set_ylabel("Y轴")
scatterchart.plot(x, y, s=50)
scatterchart.save("test_scatterchart.png")
print("散点图测试完成")

# 测试直方图
print("\n测试直方图...")
histogram = Histogram()
histogram.set_title("测试直方图")
histogram.set_xlabel("数值")
histogram.set_ylabel("频率")
histogram.plot(np.random.randn(1000), bins=20)
histogram.save("test_histogram.png")
print("直方图测试完成")

# 测试箱线图
print("\n测试箱线图...")
boxplot = BoxPlot()
boxplot.set_title("测试箱线图")
boxplot.set_xlabel("类别")
boxplot.set_ylabel("数值")
boxplot.plot([np.random.randn(50), np.random.randn(50) + 1, np.random.randn(50) + 2],
            labels=['A', 'B', 'C'])
boxplot.save("test_boxplot.png")
print("箱线图测试完成")

# 测试饼图
print("\n测试饼图...")
iechart = PieChart()
iechart.set_title("测试饼图")
iechart.plot(list(data.values()), labels=list(data.keys()), autopct='%1.1f%%')
iechart.save("test_piechart.png")
print("饼图测试完成")

print("\n所有图表测试完成！")
