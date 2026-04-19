#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
误差条形图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class ErrorBar(ChartBase):
    """误差条形图"""
    
    def plot(self, x, y, yerr=None, xerr=None, **kwargs):
        """绘制误差条形图
        
        Args:
            x: x 轴数据
            y: y 轴数据
            yerr: y 轴误差
            xerr: x 轴误差
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制误差条形图
        self.ax.errorbar(x, y, yerr=yerr, xerr=xerr, 
                       color=self.color_palette[0], **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self