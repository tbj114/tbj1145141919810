#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生存曲线
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter


class SurvivalCurve(ChartBase):
    """生存曲线"""
    
    def plot(self, duration, event, **kwargs):
        """绘制生存曲线
        
        Args:
            duration: 生存时间
            event: 事件发生指示
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算生存曲线
        kmf = KaplanMeierFitter()
        kmf.fit(duration, event)
        
        # 绘制生存曲线
        kmf.plot_survival_function(ax=self.ax, **kwargs)
        
        # 应用标签
        self._apply_labels()
        
        return self