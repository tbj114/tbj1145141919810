#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桑基图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


class SankeyDiagram(ChartBase):
    """桑基图"""
    
    def plot(self, data, source, target, value, **kwargs):
        """绘制桑基图
        
        Args:
            data: 数据
            source: 源节点列
            target: 目标节点列
            value: 值列
            **kwargs: 其他参数
        """
        # 绘制桑基图
        fig = px.sankey(data, source=source, target=target, value=value, 
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