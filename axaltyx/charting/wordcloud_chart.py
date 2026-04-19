#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词云图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud


class WordcloudChart(ChartBase):
    """词云图"""
    
    def plot(self, text, **kwargs):
        """绘制词云图
        
        Args:
            text: 文本
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制词云图
        wordcloud = WordCloud(width=800, height=600, 
                            background_color=self.ARCO_COLORS['bg_1'], 
                            colormap='Blues', **kwargs)
        wordcloud.generate(text)
        
        # 显示词云图
        self.ax.imshow(wordcloud, interpolation='bilinear')
        self.ax.axis('off')
        
        # 应用标签
        self._apply_labels()
        
        return self