#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
折线图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class LineChart(ChartBase):
    """折线图"""
    
    def plot(self, data, x=None, y=None, **kwargs):
        """绘制折线图
        
        Args:
            data: 数据，可以是字典、列表或 DataFrame
            x: x 轴数据
            y: y 轴数据
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 处理数据
        if isinstance(data, dict):
            # 多个折线
            for i, (label, values) in enumerate(data.items()):
                if x is None:
                    x_vals = np.arange(len(values))
                else:
                    x_vals = x
                self.ax.plot(x_vals, values, label=label, 
                           color=self.color_palette[i % len(self.color_palette)], **kwargs)
        elif hasattr(data, 'columns'):
            # DataFrame
            if x is None and y is None:
                # 多列数据
                for i, col in enumerate(data.columns):
                    self.ax.plot(data.index, data[col], label=col, 
                               color=self.color_palette[i % len(self.color_palette)], **kwargs)
            elif x is None:
                # 单列数据
                self.ax.plot(data.index, data[y], 
                           color=self.color_palette[0], **kwargs)
            else:
                # 指定 x 和 y
                self.ax.plot(data[x], data[y], 
                           color=self.color_palette[0], **kwargs)
        else:
            # 单个数组
            if x is None:
                x_vals = np.arange(len(data))
            else:
                x_vals = x
            self.ax.plot(x_vals, data, 
                       color=self.color_palette[0], **kwargs)
        
        # 添加图例
        if len(self.ax.lines) > 1:
            self.ax.legend()
        
        # 应用标签
        self._apply_labels()
        
        return self