#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面积图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class AreaChart(ChartBase):
    """面积图"""
    
    def plot(self, data, x=None, stacked=False, **kwargs):
        """绘制面积图
        
        Args:
            data: 数据，可以是字典、列表或 DataFrame
            x: x 轴数据
            stacked: 是否堆叠
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 处理数据
        if isinstance(data, dict):
            # 多个系列
            if x is None:
                x = np.arange(len(list(data.values())[0]))
            
            values = list(data.values())
            labels = list(data.keys())
            
            if stacked:
                self.ax.stackplot(x, values, labels=labels, 
                                colors=self.color_palette[:len(values)], **kwargs)
            else:
                for i, (label, vals) in enumerate(data.items()):
                    self.ax.fill_between(x, vals, label=label, 
                                       color=self.color_palette[i % len(self.color_palette)], **kwargs)
        elif hasattr(data, 'columns'):
            # DataFrame
            if x is None:
                x = data.index
            
            if stacked:
                self.ax.stackplot(x, data.T, labels=data.columns, 
                                colors=self.color_palette[:len(data.columns)], **kwargs)
            else:
                for i, col in enumerate(data.columns):
                    self.ax.fill_between(x, data[col], label=col, 
                                       color=self.color_palette[i % len(self.color_palette)], **kwargs)
        
        # 添加图例
        if len(self.ax.collections) > 1:
            self.ax.legend()
        
        # 应用标签
        self._apply_labels()
        
        return self