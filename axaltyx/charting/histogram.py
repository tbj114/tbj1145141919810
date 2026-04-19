#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直方图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class Histogram(ChartBase):
    """直方图"""
    
    def plot(self, data, bins=10, range=None, density=False, **kwargs):
        """绘制直方图
        
        Args:
            data: 数据
            bins:  bins 数量
            range: 范围
            density: 是否标准化
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制直方图
        self.ax.hist(data, bins=bins, range=range, density=density, 
                    color=self.color_palette[0], **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self