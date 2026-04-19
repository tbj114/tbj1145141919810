#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
序列图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class SequencePlot(ChartBase):
    """序列图"""
    
    def plot(self, data, **kwargs):
        """绘制序列图
        
        Args:
            data: 序列数据
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制序列图
        self.ax.plot(data, color=self.color_palette[0], **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self