#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对应分析图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


class CorrespondencePlot(ChartBase):
    """对应分析图"""
    
    def plot(self, data, **kwargs):
        """绘制对应分析图
        
        Args:
            data:  contingency 表
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算对应分析
        n = data.sum().sum()
        row_margins = data.sum(axis=1) / n
        col_margins = data.sum(axis=0) / n
        
        # 标准化残差矩阵
        standardized = (data / n - np.outer(row_margins, col_margins)) / np.sqrt(np.outer(row_margins, col_margins))
        
        # PCA 分析
        pca = PCA(n_components=2)
        row_coords = pca.fit_transform(standardized)
        col_coords = pca.transform(standardized.T)
        
        # 绘制对应分析图
        self.ax.scatter(row_coords[:, 0], row_coords[:, 1], 
                       color=self.color_palette[0], label='Rows')
        self.ax.scatter(col_coords[:, 0], col_coords[:, 1], 
                       color=self.color_palette[1], label='Columns')
        
        # 添加标签
        for i, name in enumerate(data.index):
            self.ax.text(row_coords[i, 0], row_coords[i, 1], name, 
                       ha='center', va='center', color=self.color_palette[0])
        for i, name in enumerate(data.columns):
            self.ax.text(col_coords[i, 0], col_coords[i, 1], name, 
                       ha='center', va='center', color=self.color_palette[1])
        
        # 添加图例
        self.ax.legend()
        
        # 应用标签
        self._apply_labels()
        
        return self