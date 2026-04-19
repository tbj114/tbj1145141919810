#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高低图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class HiLo(ChartBase):
    """高低图"""
    
    def plot(self, data, **kwargs):
        """绘制高低图
        
        Args:
            data: 数据，包含 high, low, open, close 列
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制高低图
        for i, row in data.iterrows():
            # 绘制高低线
            self.ax.plot([i, i], [row['low'], row['high']], 
                       color=self.color_palette[0], **kwargs)
            # 绘制开盘和收盘
            if row['open'] < row['close']:
                color = self.ARCO_COLORS['success']
            else:
                color = self.ARCO_COLORS['danger']
            self.ax.plot([i, i], [row['open'], row['close']], 
                       color=color, linewidth=2, **kwargs)
        
        # 设置 x 轴标签
        self.ax.set_xticks(np.arange(len(data)))
        self.ax.set_xticklabels(data.index, rotation=45, ha='right')
        
        # 应用标签
        self._apply_labels()
        
        return self