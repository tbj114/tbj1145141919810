#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
偏自相关函数图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import pacf


class PACFPlot(ChartBase):
    """偏自相关函数图"""
    
    def plot(self, data, lags=None, alpha=0.05, **kwargs):
        """绘制偏自相关函数图
        
        Args:
            data: 时间序列数据
            lags: 滞后阶数
            alpha: 显著性水平
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算偏自相关函数
        pacf_vals, confint = pacf(data, nlags=lags, alpha=alpha, method='ywm')
        
        # 绘制偏自相关函数
        lags = np.arange(len(pacf_vals))
        self.ax.stem(lags, pacf_vals, linefmt=self.color_palette[0], 
                    markerfmt=f'{self.color_palette[0]}o', basefmt='k-')
        
        # 绘制置信区间
        self.ax.fill_between(lags, confint[:, 0], confint[:, 1], 
                           color=self.ARCO_COLORS['arcoblue-1'], alpha=0.5)
        
        # 设置 y 轴范围
        self.ax.set_ylim(-1, 1)
        
        # 应用标签
        self._apply_labels()
        
        return self