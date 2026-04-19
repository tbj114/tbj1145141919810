#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
茎叶图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np


class StemLeaf(ChartBase):
    """茎叶图"""
    
    def plot(self, data, **kwargs):
        """绘制茎叶图
        
        Args:
            data: 数据
            **kwargs: 其他参数
        """
        # 设置图表
        self._setup_figure()
        
        # 计算茎叶
        stems, leaves = self._calculate_stem_leaf(data)
        
        # 绘制茎叶图
        for i, (stem, leaf_list) in enumerate(zip(stems, leaves)):
            leaf_str = ' '.join(map(str, leaf_list))
            self.ax.text(0, i, f'{stem:2d} | {leaf_str}', 
                       ha='left', va='center')
        
        # 设置轴范围
        self.ax.set_xlim(-1, 10)
        self.ax.set_ylim(-0.5, len(stems) - 0.5)
        self.ax.axis('off')
        
        # 应用标签
        self._apply_labels()
        
        return self
    
    def _calculate_stem_leaf(self, data):
        """计算茎叶"""
        data = sorted(data)
        stems = []
        leaves = []
        current_stem = None
        current_leaves = []
        
        for value in data:
            stem = int(value // 10)
            leaf = int(value % 10)
            
            if stem != current_stem:
                if current_stem is not None:
                    stems.append(current_stem)
                    leaves.append(current_leaves)
                current_stem = stem
                current_leaves = [leaf]
            else:
                current_leaves.append(leaf)
        
        if current_stem is not None:
            stems.append(current_stem)
            leaves.append(current_leaves)
        
        return stems, leaves