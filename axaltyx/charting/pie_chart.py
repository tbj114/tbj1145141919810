#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
饼图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class PieChart(ChartBase):
    """饼图"""
    
    def plot(self, data, labels=None, autopct=None, **kwargs):
        """绘制饼图
        
        Args:
            data: 数据
            labels: 标签
            autopct: 百分比格式
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制饼图
        self.ax.pie(data, labels=labels, autopct=autopct, 
                   colors=self.color_palette, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self