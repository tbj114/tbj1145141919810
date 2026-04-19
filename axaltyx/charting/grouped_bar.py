#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分组柱状图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class GroupedBar(ChartBase):
    """分组柱状图"""
    
    def plot(self, data, categories, group_names, **kwargs):
        """绘制分组柱状图
        
        Args:
            data: 数据，二维数组
            categories: 分类标签
            group_names: 组名
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算柱子宽度
        n_groups = len(data)
        n_categories = len(data[0])
        width = 0.8 / n_categories
        
        # 绘制分组柱状图
        for i in range(n_categories):
            x = np.arange(n_groups) + i * width
            self.ax.bar(x, [row[i] for row in data], width=width, 
                       label=group_names[i], color=self.color_palette[i % len(self.color_palette)], **kwargs)
        
        # 设置 x 轴标签
        self.ax.set_xticks(np.arange(n_groups) + width * (n_categories - 1) / 2)
        self.ax.set_xticklabels(categories)
        
        # 添加图例
        self.ax.legend()
        
        # 应用标签
        self._apply_labels()
        
        return self