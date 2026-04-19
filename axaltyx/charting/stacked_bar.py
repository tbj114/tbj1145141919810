#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
堆叠柱状图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class StackedBar(ChartBase):
    """堆叠柱状图"""
    
    def plot(self, data, categories, group_names, **kwargs):
        """绘制堆叠柱状图
        
        Args:
            data: 数据，二维数组
            categories: 分类标签
            group_names: 组名
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制堆叠柱状图
        n_categories = len(data[0])
        bottom = np.zeros(len(data))
        
        for i in range(n_categories):
            values = [row[i] for row in data]
            self.ax.bar(categories, values, bottom=bottom, 
                       label=group_names[i], color=self.color_palette[i % len(self.color_palette)], **kwargs)
            bottom += values
        
        # 添加图例
        self.ax.legend()
        
        # 应用标签
        self._apply_labels()
        
        return self