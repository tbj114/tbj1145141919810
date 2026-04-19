#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


class NetworkPlot(ChartBase):
    """网络图"""
    
    def plot(self, graph, **kwargs):
        """绘制网络图
        
        Args:
            graph: 网络对象
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制网络图
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, ax=self.ax, 
               node_color=self.color_palette[0], 
               edge_color=self.ARCO_COLORS['border'], 
               **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self