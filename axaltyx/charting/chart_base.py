#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表基类
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# 确保中文字符显示
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei']  # 用于显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用于显示负号


class ChartBase:
    """图表基类"""
    
    # Arco Design 配色方案
    ARCO_COLORS = {
        'primary': '#165DFF',
        'success': '#00B42A',
        'warning': '#FF7D00',
        'danger': '#F53F3F',
        'info': '#86909C',
        'bg_1': '#F7F8FA',
        'bg_2': '#F2F3F5',
        'bg_3': '#E5E6EB',
        'text_1': '#1D2129',
        'text_2': '#4E5969',
        'text_3': '#86909C',
        'border': '#D9D9D9',
        'arcoblue-1': '#E8F3FF',
        'arcoblue-2': '#D1E7FF',
        'arcoblue-3': '#A3D0FF',
        'arcoblue-4': '#69B1FF',
        'arcoblue-5': '#3689FF',
        'arcoblue-6': '#165DFF',
        'arcoblue-7': '#0944D4',
        'arcoblue-8': '#0031A9',
        'arcoblue-9': '#002785',
    }

    def __init__(self, figsize=(8, 6), dpi=100):
        """初始化图表"""
        self.figsize = figsize
        self.dpi = dpi
        self.fig = None
        self.ax = None
        self.title = ""
        self.xlabel = ""
        self.ylabel = ""
        self.color_palette = [
            self.ARCO_COLORS['arcoblue-6'],
            self.ARCO_COLORS['success'],
            self.ARCO_COLORS['warning'],
            self.ARCO_COLORS['danger'],
            self.ARCO_COLORS['info'],
            self.ARCO_COLORS['arcoblue-4'],
            self.ARCO_COLORS['arcoblue-8'],
            self.ARCO_COLORS['arcoblue-3'],
        ]

    def _setup_figure(self):
        """设置图表对象"""
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        # 设置背景和边框
        self.ax.set_facecolor(self.ARCO_COLORS['bg_1'])
        self.fig.patch.set_facecolor(self.ARCO_COLORS['bg_1'])
        # 设置边框
        for spine in self.ax.spines.values():
            spine.set_color(self.ARCO_COLORS['border'])
        # 设置刻度标签颜色
        self.ax.tick_params(axis='x', colors=self.ARCO_COLORS['text_2'])
        self.ax.tick_params(axis='y', colors=self.ARCO_COLORS['text_2'])

    def set_title(self, title):
        """设置图表标题"""
        self.title = title

    def set_xlabel(self, xlabel):
        """设置 x 轴标签"""
        self.xlabel = xlabel

    def set_ylabel(self, ylabel):
        """设置 y 轴标签"""
        self.ylabel = ylabel

    def _apply_labels(self):
        """应用标签"""
        if self.title:
            self.ax.set_title(self.title, color=self.ARCO_COLORS['text_1'], fontsize=14, fontweight='bold')
        if self.xlabel:
            self.ax.set_xlabel(self.xlabel, color=self.ARCO_COLORS['text_2'], fontsize=12)
        if self.ylabel:
            self.ax.set_ylabel(self.ylabel, color=self.ARCO_COLORS['text_2'], fontsize=12)

    def plot(self, data):
        """绘制图表"""
        raise NotImplementedError("子类必须实现 plot 方法")

    def show(self):
        """显示图表"""
        if self.fig is None:
            raise ValueError("请先调用 plot 方法")
        plt.tight_layout()
        plt.show()

    def save(self, file_path, dpi=300, bbox_inches='tight'):
        """保存图表
        
        Args:
            file_path: 保存路径
            dpi: 分辨率
            bbox_inches: 边界设置
        """
        if self.fig is None:
            raise ValueError("请先调用 plot 方法")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        plt.tight_layout()
        self.fig.savefig(file_path, dpi=dpi, bbox_inches=bbox_inches)
        plt.close(self.fig)

    def get_figure(self):
        """获取图表对象"""
        if self.fig is None:
            raise ValueError("请先调用 plot 方法")
        return self.fig

    def get_axes(self):
        """获取坐标轴对象"""
        if self.ax is None:
            raise ValueError("请先调用 plot 方法")
        return self.ax
