#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
柱状图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt


class BarChart(ChartBase):
    """柱状图"""
    
    def plot(self, data, x=None, y=None, width=0.8, align='center', **kwargs):
        """绘制柱状图
        
        Args:
            data: 数据，可以是字典、列表或 DataFrame
            x: x 轴数据
            y: y 轴数据
            width: 柱子宽度
            align: 对齐方式
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 处理数据
        if isinstance(data, dict):
            x = list(data.keys())
            y = list(data.values())
        elif hasattr(data, 'columns'):
            # DataFrame
            if x is None and y is None:
                x = data.index.tolist()
                y = data.iloc[:, 0].tolist()
            elif x is None:
                y = data[y].tolist()
                x = data.index.tolist()
            elif y is None:
                y = data[x].tolist()
                x = data.index.tolist()
        
        # 绘制柱状图
        bars = self.ax.bar(x, y, width=width, align=align, 
                          color=self.color_palette[0], **kwargs)
        
        # 设置颜色
        for i, bar in enumerate(bars):
            bar.set_color(self.color_palette[i % len(self.color_palette)])
        
        # 应用标签
        self._apply_labels()
        
        return self