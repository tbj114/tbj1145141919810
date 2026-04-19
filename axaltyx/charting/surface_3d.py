#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 表面图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Surface3D(ChartBase):
    """3D 表面图"""
    
    def plot(self, x, y, z, **kwargs):
        """绘制 3D 表面图
        
        Args:
            x: x 轴数据
            y: y 轴数据
            z: z 轴数据
            **kwargs: 其他参数
        """
        # 设置图表
        self.fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # 绘制 3D 表面图
        self.ax.plot_surface(x, y, z, cmap='Blues', **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self