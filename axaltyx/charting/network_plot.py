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
    
    def plot(self, graph, interactive=False, **kwargs):
        """绘制网络图
        
        Args:
            graph: 网络对象
            interactive: 是否启用交互
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制网络图
        self.pos = nx.spring_layout(graph)
        self.nodes = nx.draw_networkx_nodes(graph, self.pos, ax=self.ax, 
                                          node_color=self.color_palette[0], 
                                          **kwargs)
        self.edges = nx.draw_networkx_edges(graph, self.pos, ax=self.ax, 
                                          edge_color=self.ARCO_COLORS['border'], 
                                          **kwargs)
        
        # 添加节点标签
        nx.draw_networkx_labels(graph, self.pos, ax=self.ax)
        
        # 应用标签
        self._apply_labels()
        
        # 启用交互
        if interactive:
            self.graph = graph
            self.fig.canvas.mpl_connect('motion_notify_event', self._on_hover)
            self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        
        return self
    
    def _on_hover(self, event):
        """鼠标悬停事件处理"""
        if event.inaxes == self.ax:
            # 计算鼠标位置最近的节点
            min_dist = float('inf')
            hovered_node = None
            for node, (x, y) in self.pos.items():
                dist = np.sqrt((x - event.xdata)**2 + (y - event.ydata)**2)
                if dist < min_dist and dist < 0.1:
                    min_dist = dist
                    hovered_node = node
            
            if hovered_node is not None:
                self.ax.set_title(f'Node: {hovered_node}')
            else:
                self.ax.set_title('')
            self.fig.canvas.draw_idle()
    
    def _on_click(self, event):
        """鼠标点击事件处理"""
        if event.inaxes == self.ax:
            # 计算鼠标位置最近的节点
            min_dist = float('inf')
            clicked_node = None
            for node, (x, y) in self.pos.items():
                dist = np.sqrt((x - event.xdata)**2 + (y - event.ydata)**2)
                if dist < min_dist and dist < 0.1:
                    min_dist = dist
                    clicked_node = node
            
            if clicked_node is not None:
                print(f'Clicked node: {clicked_node}')
                print(f'Neighbors: {list(self.graph.neighbors(clicked_node))}')