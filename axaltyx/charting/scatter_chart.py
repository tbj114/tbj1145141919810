#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
散点图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class ScatterChart(ChartBase):
    """散点图"""
    
    def plot(self, x, y, s=None, c=None, **kwargs):
        """绘制散点图
        
        Args:
            x: x 轴数据
            y: y 轴数据
            s: 点的大小
            c: 点的颜色
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 处理颜色
        if c is None:
            c = self.color_palette[0]
        
        # 绘制散点图
        self.ax.scatter(x, y, s=s, c=c, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self