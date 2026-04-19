#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雷达图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class RadarChart(ChartBase):
    """雷达图"""
    
    def plot(self, data, categories, **kwargs):
        """绘制雷达图
        
        Args:
            data: 数据
            categories: 分类标签
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算角度
        N = len(categories)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]
        
        # 处理数据
        if isinstance(data, dict):
            for i, (label, values) in enumerate(data.items()):
                values = np.array(values).tolist()
                values += values[:1]
                self.ax.plot(angles, values, label=label, 
                           color=self.color_palette[i % len(self.color_palette)], **kwargs)
                self.ax.fill(angles, values, alpha=0.2, 
                           color=self.color_palette[i % len(self.color_palette)])
        else:
            values = np.array(data).tolist()
            values += values[:1]
            self.ax.plot(angles, values, 
                       color=self.color_palette[0], **kwargs)
            self.ax.fill(angles, values, alpha=0.2, 
                       color=self.color_palette[0])
        
        # 设置标签
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(categories)
        
        # 设置极坐标
        self.ax.set_rlabel_position(0)
        
        # 添加图例
        if isinstance(data, dict):
            self.ax.legend()
        
        # 应用标签
        self._apply_labels()
        
        return self