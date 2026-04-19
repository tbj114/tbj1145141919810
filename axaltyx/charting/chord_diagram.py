#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弦图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Wedge
from matplotlib.path import Path
from matplotlib.transforms import Affine2D


class ChordDiagram(ChartBase):
    """弦图"""
    
    def plot(self, matrix, names, **kwargs):
        """绘制弦图
        
        Args:
            matrix: 邻接矩阵
            names: 节点名称
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算节点角度
        n = len(names)
        theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
        width = 2 * np.pi / n
        
        # 绘制节点
        for i in range(n):
            wedge = Wedge((0, 0), 1, theta[i], theta[i] + width, 
                         facecolor=self.color_palette[i % len(self.color_palette)], 
                         edgecolor='white')
            self.ax.add_patch(wedge)
            
            # 添加标签
            angle = theta[i] + width / 2
            x = 1.1 * np.cos(angle)
            y = 1.1 * np.sin(angle)
            ha = 'center' if x > 0 else 'center'
            self.ax.text(x, y, names[i], ha=ha, va='center')
        
        # 绘制弦
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i, j] > 0:
                    # 计算弦的路径
                    start = theta[i] + width / 2
                    end = theta[j] + width / 2
                    
                    # 绘制弦
                    path = Path([
                        (np.cos(start), np.sin(start)),
                        (0.8 * np.cos(start), 0.8 * np.sin(start)),
                        (0.8 * np.cos(end), 0.8 * np.sin(end)),
                        (np.cos(end), np.sin(end))
                    ])
                    self.ax.plot(path.vertices[:, 0], path.vertices[:, 1], 
                               color=self.color_palette[i % len(self.color_palette)], 
                               alpha=0.5)
        
        # 设置轴范围
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.axis('off')
        
        # 应用标签
        self._apply_labels()
        
        return self