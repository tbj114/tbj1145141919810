#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROC 曲线
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc


class ROCCurve(ChartBase):
    """ROC 曲线"""
    
    def plot(self, y_true, y_score, **kwargs):
        """绘制 ROC 曲线
        
        Args:
            y_true: 真实标签
            y_score: 预测得分
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算 ROC 曲线
        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        
        # 绘制 ROC 曲线
        self.ax.plot(fpr, tpr, color=self.color_palette[0], 
                    label=f'ROC curve (area = {roc_auc:.2f})')
        
        # 绘制对角线
        self.ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        
        # 设置轴范围
        self.ax.set_xlim([0.0, 1.0])
        self.ax.set_ylim([0.0, 1.05])
        
        # 添加图例
        self.ax.legend(loc='lower right')
        
        # 应用标签
        self._apply_labels()
        
        return self