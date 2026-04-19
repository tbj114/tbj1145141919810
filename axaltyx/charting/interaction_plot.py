#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互作用图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class InteractionPlot(ChartBase):
    """交互作用图"""
    
    def plot(self, data, x_col, hue_col, y_col, **kwargs):
        """绘制交互作用图
        
        Args:
            data: 数据
            x_col: x 轴列名
            hue_col: 分组列名
            y_col: y 轴列名
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制交互作用图
        sns.lineplot(data=data, x=x_col, hue=hue_col, y=y_col, 
                    palette=self.color_palette, ax=self.ax, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self