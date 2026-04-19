#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
矩阵散点图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class MatrixScatter(ChartBase):
    """矩阵散点图"""
    
    def plot(self, data, **kwargs):
        """绘制矩阵散点图
        
        Args:
            data: 数据
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制矩阵散点图
        sns.pairplot(data, palette=self.color_palette, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self