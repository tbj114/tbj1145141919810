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
    
    def plot(self, data, source, target, value, interactive=True, **kwargs):
        """绘制桑基图
        
        Args:
            data: 数据
            source: 源节点列
            target: 目标节点列
            value: 值列
            interactive: 是否启用交互
            **kwargs: 其他参数
        """
        # 绘制桑基图
        fig = px.sankey(data, source=source, target=target, value=value, 
                       color_discrete_sequence=self.color_palette, 
                       **kwargs)
        
        # 启用交互
        if interactive:
            fig.update_layout(
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    font_size=12,
                    font_family="SimHei"
                )
            )
        
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