#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多面板图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class MultiPanel(ChartBase):
    """多面板图"""
    
    def plot(self, data_list, rows, cols, **kwargs):
        """绘制多面板图
        
        Args:
            data_list: 数据列表
            rows: 行数
            cols: 列数
            **kwargs: 其他参数
        """
        # 设置图表
        self.fig, self.axes = plt.subplots(rows, cols, figsize=self.figsize, dpi=self.dpi)
        self.axes = np.ravel(self.axes)
        
        # 绘制多面板图
        for i, (data, ax) in enumerate(zip(data_list, self.axes)):
            # 设置子图背景和边框
            ax.set_facecolor(self.ARCO_COLORS['bg_1'])
            for spine in ax.spines.values():
                spine.set_color(self.ARCO_COLORS['border'])
            # 设置刻度标签颜色
            ax.tick_params(axis='x', colors=self.ARCO_COLORS['text_2'])
            ax.tick_params(axis='y', colors=self.ARCO_COLORS['text_2'])
            
            # 绘制数据
            if isinstance(data, dict):
                ax.bar(data.keys(), data.values(), color=self.color_palette[i % len(self.color_palette)])
            elif isinstance(data, list):
                ax.plot(data, color=self.color_palette[i % len(self.color_palette)])
        
        # 应用标签
        self._apply_labels()
        
        return self