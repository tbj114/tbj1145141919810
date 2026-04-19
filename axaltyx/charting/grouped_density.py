#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分组密度图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class GroupedDensity(ChartBase):
    """分组密度图"""
    
    def plot(self, data, group_col, value_col, **kwargs):
        """绘制分组密度图
        
        Args:
            data: 数据
            group_col: 分组列名
            value_col: 值列名
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制分组密度图
        sns.kdeplot(data=data, x=value_col, hue=group_col, 
                   palette=self.color_palette, ax=self.ax, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self