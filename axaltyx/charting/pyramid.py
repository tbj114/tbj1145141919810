#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金字塔图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class Pyramid(ChartBase):
    """金字塔图"""
    
    def plot(self, data, categories, **kwargs):
        """绘制金字塔图
        
        Args:
            data: 数据，包含左右两部分
            categories: 分类标签
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算数据
        left_data, right_data = data
        x = np.arange(len(categories))
        width = 0.4
        
        # 绘制左侧柱状图
        self.ax.barh(x - width/2, -left_data, width=width, 
                    color=self.color_palette[0], label='左侧', **kwargs)
        
        # 绘制右侧柱状图
        self.ax.barh(x + width/2, right_data, width=width, 
                    color=self.color_palette[1], label='右侧', **kwargs)
        
        # 设置 y 轴标签
        self.ax.set_yticks(x)
        self.ax.set_yticklabels(categories)
        
        # 设置 x 轴范围
        max_val = max(max(left_data), max(right_data))
        self.ax.set_xlim(-max_val * 1.1, max_val * 1.1)
        
        # 添加图例
        self.ax.legend()
        
        # 应用标签
        self._apply_labels()
        
        return self