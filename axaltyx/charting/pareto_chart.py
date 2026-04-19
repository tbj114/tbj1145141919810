#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
帕累托图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class ParetoChart(ChartBase):
    """帕累托图"""
    
    def plot(self, data, categories, **kwargs):
        """绘制帕累托图
        
        Args:
            data: 数据
            categories: 分类标签
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 排序数据
        sorted_indices = np.argsort(data)[::-1]
        sorted_data = np.array(data)[sorted_indices]
        sorted_categories = np.array(categories)[sorted_indices]
        
        # 计算累计百分比
        cumulative = np.cumsum(sorted_data) / np.sum(sorted_data) * 100
        
        # 创建第二个 y 轴
        ax2 = self.ax.twinx()
        
        # 绘制柱状图
        bars = self.ax.bar(sorted_categories, sorted_data, 
                          color=self.color_palette[0], **kwargs)
        
        # 绘制累计百分比线
        ax2.plot(sorted_categories, cumulative, 'r-', marker='o')
        
        # 设置轴标签
        self.ax.set_ylabel('频率')
        ax2.set_ylabel('累计百分比 (%)')
        
        # 设置 x 轴标签
        self.ax.set_xticklabels(sorted_categories, rotation=45, ha='right')
        
        # 应用标签
        self._apply_labels()
        
        return self