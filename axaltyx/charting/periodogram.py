#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周期图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


class Periodogram(ChartBase):
    """周期图"""
    
    def plot(self, data, fs=1.0, **kwargs):
        """绘制周期图
        
        Args:
            data: 时间序列数据
            fs: 采样频率
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算周期图
        f, Pxx = signal.periodogram(data, fs=fs)
        
        # 绘制周期图
        self.ax.semilogy(f, Pxx, color=self.color_palette[0], **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self