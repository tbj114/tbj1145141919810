#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热力图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Heatmap(ChartBase):
    """热力图"""
    
    def plot(self, data, cmap=None, annot=False, fmt='.2f', interactive=False, **kwargs):
        """绘制热力图
        
        Args:
            data: 数据
            cmap: 颜色映射
            annot: 是否显示数值
            fmt: 数值格式
            interactive: 是否启用交互
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制热力图
        if cmap is None:
            cmap = 'Blues'
        
        sns.heatmap(data, ax=self.ax, cmap=cmap, annot=annot, fmt=fmt, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        # 启用交互
        if interactive:
            self.fig.canvas.mpl_connect('motion_notify_event', self._on_hover)
        
        return self
    
    def _on_hover(self, event):
        """鼠标悬停事件处理"""
        if event.inaxes == self.ax:
            x = int(event.xdata + 0.5)
            y = int(event.ydata + 0.5)
            if 0 <= x < self.ax.get_xlim()[1] and 0 <= y < self.ax.get_ylim()[0]:
                self.ax.set_title(f'({x}, {y})')
                self.fig.canvas.draw_idle()