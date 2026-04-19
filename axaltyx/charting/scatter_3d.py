#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 散点图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Scatter3D(ChartBase):
    """3D 散点图"""
    
    def plot(self, x, y, z, s=None, c=None, **kwargs):
        """绘制 3D 散点图
        
        Args:
            x: x 轴数据
            y: y 轴数据
            z: z 轴数据
            s: 点的大小
            c: 点的颜色
            **kwargs: 其他参数
        """
        # 设置图表
        self.fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # 处理颜色
        if c is None:
            c = self.color_palette[0]
        
        # 绘制 3D 散点图
        self.ax.scatter(x, y, z, s=s, c=c, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self