#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
冰柱图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


class IciclePlot(ChartBase):
    """冰柱图"""
    
    def plot(self, data, path, values, **kwargs):
        """绘制冰柱图
        
        Args:
            data: 数据
            path: 路径列
            values: 值列
            **kwargs: 其他参数
        """
        # 绘制冰柱图
        fig = px.icicle(data, path=path, values=values, 
                       color_discrete_sequence=self.color_palette, **kwargs)
        
        # 保存图表
        self.fig = fig
        
        return self
    
    def save(self, file_path):
        """保存图表
        
        Args:
            file_path: 保存路径
        """
        if hasattr(self, 'fig'):
            self.fig.write_html(file_path)
        else:
            raise ValueError("请先调用 plot 方法")