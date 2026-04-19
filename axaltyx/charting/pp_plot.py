#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P-P 图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class PPPlot(ChartBase):
    """P-P 图"""
    
    def plot(self, data, dist=stats.norm, **kwargs):
        """绘制 P-P 图
        
        Args:
            data: 数据
            dist: 分布，默认为正态分布
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算经验分布和理论分布
        n = len(data)
        sorted_data = np.sort(data)
        empirical = np.arange(1, n+1) / n
        theoretical = dist.cdf(sorted_data)
        
        # 绘制 P-P 图
        self.ax.scatter(theoretical, empirical, color=self.color_palette[0])
        
        # 绘制参考线
        self.ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        
        # 设置轴范围
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        
        # 应用标签
        self._apply_labels()
        
        return self