#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
箱线图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class BoxPlot(ChartBase):
    """箱线图"""
    
    def plot(self, data, labels=None, **kwargs):
        """绘制箱线图
        
        Args:
            data: 数据，可以是列表或数组
            labels: 标签
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制箱线图
        box = self.ax.boxplot(data, labels=labels, patch_artist=True, **kwargs)
        
        # 设置颜色
        for patch, color in zip(box['boxes'], self.color_palette):
            patch.set_facecolor(color)
        
        # 应用标签
        self._apply_labels()
        
        return self