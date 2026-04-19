#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分类图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class CategoryPlot(ChartBase):
    """分类图"""
    
    def plot(self, categories, values, **kwargs):
        """绘制分类图
        
        Args:
            categories: 分类标签
            values: 对应的值
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制分类图
        x = np.arange(len(categories))
        self.ax.bar(x, values, color=self.color_palette[0], **kwargs)
        
        # 设置 x 轴标签
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(categories, rotation=45, ha='right')
        
        # 应用标签
        self._apply_labels()
        
        return self