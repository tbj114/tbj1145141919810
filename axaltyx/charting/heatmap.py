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
    
    def plot(self, data, cmap=None, annot=False, fmt='.2f', **kwargs):
        """绘制热力图
        
        Args:
            data: 数据
            cmap: 颜色映射
            annot: 是否显示数值
            fmt: 数值格式
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
        
        return self