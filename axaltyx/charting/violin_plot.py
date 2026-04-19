#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小提琴图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class ViolinPlot(ChartBase):
    """小提琴图"""
    
    def plot(self, data, labels=None, **kwargs):
        """绘制小提琴图
        
        Args:
            data: 数据
            labels: 标签
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制小提琴图
        sns.violinplot(data=data, ax=self.ax, palette=self.color_palette, **kwargs)
        
        # 设置标签
        if labels:
            self.ax.set_xticklabels(labels)
        
        # 应用标签
        self._apply_labels()
        
        return self