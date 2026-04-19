#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轮廓图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class ProfilePlot(ChartBase):
    """轮廓图"""
    
    def plot(self, data, **kwargs):
        """绘制轮廓图
        
        Args:
            data: 数据
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制轮廓图
        sns.heatmap(data, ax=self.ax, cmap='Blues', **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self