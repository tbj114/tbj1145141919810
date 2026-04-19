#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密度图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class DensityChart(ChartBase):
    """密度图"""
    
    def plot(self, data, kernel='gaussian', bw_method=None, **kwargs):
        """绘制密度图
        
        Args:
            data: 数据
            kernel: 核函数
            bw_method: 带宽方法
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算密度
        kde = stats.gaussian_kde(data, bw_method=bw_method)
        x = np.linspace(min(data), max(data), 1000)
        y = kde(x)
        
        # 绘制密度图
        self.ax.plot(x, y, color=self.color_palette[0], **kwargs)
        
        # 填充区域
        self.ax.fill_between(x, y, alpha=0.3, color=self.color_palette[0])
        
        # 应用标签
        self._apply_labels()
        
        return self