#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
点图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class DotPlot(ChartBase):
    """点图"""
    
    def plot(self, data, categories, **kwargs):
        """绘制点图
        
        Args:
            data: 数据
            categories: 分类标签
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制点图
        for i, (category, values) in enumerate(zip(categories, data)):
            x = np.random.normal(i, 0.1, len(values))
            self.ax.scatter(x, values, color=self.color_palette[i % len(self.color_palette)], **kwargs)
        
        # 设置 x 轴标签
        self.ax.set_xticks(np.arange(len(categories)))
        self.ax.set_xticklabels(categories)
        
        # 应用标签
        self._apply_labels()
        
        return self