#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ridge 图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class RidgePlot(ChartBase):
    """Ridge 图"""
    
    def plot(self, data, **kwargs):
        """绘制 Ridge 图
        
        Args:
            data: 数据
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制 Ridge 图
        sns.kdeplot(data=data, multiple="stack", 
                   palette=self.color_palette, ax=self.ax, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self