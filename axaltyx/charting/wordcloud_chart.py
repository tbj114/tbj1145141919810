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
    
    def plot(self, text, interactive=False, **kwargs):
        """绘制词云图
        
        Args:
            text: 文本
            interactive: 是否启用交互
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 绘制词云图
        wordcloud = WordCloud(width=800, height=600, 
                            background_color=self.ARCO_COLORS['bg_1'], 
                            colormap='Blues', **kwargs)
        self.wordcloud = wordcloud.generate(text)
        
        # 显示词云图
        self.imshow = self.ax.imshow(self.wordcloud, interpolation='bilinear')
        self.ax.axis('off')
        
        # 应用标签
        self._apply_labels()
        
        # 启用交互
        if interactive:
            self.fig.canvas.mpl_connect('motion_notify_event', self._on_hover)
        
        return self
    
    def _on_hover(self, event):
        """鼠标悬停事件处理"""
        if event.inaxes == self.ax:
            # 获取鼠标位置对应的单词
            x = int(event.xdata)
            y = int(event.ydata)
            
            # 检查是否在词云范围内
            if 0 <= x < self.wordcloud.width and 0 <= y < self.wordcloud.height:
                # 这里可以添加更复杂的单词检测逻辑
                self.ax.set_title(f'Position: ({x}, {y})')
            else:
                self.ax.set_title('')
            self.fig.canvas.draw_idle()