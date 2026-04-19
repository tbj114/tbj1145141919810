#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
层次聚类树状图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage


class Dendrogram(ChartBase):
    """层次聚类树状图"""
    
    def plot(self, data, method='ward', metric='euclidean', **kwargs):
        """绘制层次聚类树状图
        
        Args:
            data: 数据
            method: 聚类方法
            metric: 距离度量
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算 linkage
        Z = linkage(data, method=method, metric=metric)
        
        # 绘制树状图
        dendrogram(Z, ax=self.ax, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self