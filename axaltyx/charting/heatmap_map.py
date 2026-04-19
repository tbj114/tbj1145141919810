#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热力地图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap


class HeatmapMap(ChartBase):
    """热力地图"""
    
    def plot(self, data, lat_col, lon_col, value_col, **kwargs):
        """绘制热力地图
        
        Args:
            data: 数据
            lat_col: 纬度列名
            lon_col: 经度列名
            value_col: 值列名
            **kwargs: 其他参数
        """
        # 创建地图
        m = folium.Map(location=[data[lat_col].mean(), data[lon_col].mean()], 
                      zoom_start=10, **kwargs)
        
        # 准备热力数据
        heat_data = [[row[lat_col], row[lon_col], row[value_col]] 
                    for _, row in data.iterrows()]
        
        # 添加热力层
        HeatMap(heat_data, radius=25, blur=15, max_zoom=10).add_to(m)
        
        # 保存地图
        self.map = m
        
        return self
    
    def save(self, file_path):
        """保存地图
        
        Args:
            file_path: 保存路径
        """
        if hasattr(self, 'map'):
            self.map.save(file_path)
        else:
            raise ValueError("请先调用 plot 方法")