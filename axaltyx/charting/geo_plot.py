#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地理图
"""

from .chart_base import ChartBase
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import folium


class GeoPlot(ChartBase):
    """地理图"""
    
    def plot(self, data, lat_col, lon_col, value_col, **kwargs):
        """绘制地理图
        
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
        
        # 添加标记
        for _, row in data.iterrows():
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=row[value_col] / 10,
                color=self.color_palette[0],
                fill=True,
                fill_color=self.color_palette[0],
                fill_opacity=0.6
            ).add_to(m)
        
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