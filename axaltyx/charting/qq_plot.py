#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Q-Q 图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class QQPlot(ChartBase):
    """Q-Q 图"""
    
    def plot(self, data, dist=stats.norm, **kwargs):
        """绘制 Q-Q 图
        
        Args:
            data: 数据
            dist: 分布，默认为正态分布
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制 Q-Q 图
        stats.probplot(data, dist=dist, plot=self.ax)
        
        # 自定义样式
        for line in self.ax.lines:
            line.set_color(self.color_palette[0])
        for scatter in self.ax.collections:
            scatter.set_color(self.color_palette[1])
        
        # 应用标签
        self._apply_labels()
        
        return self