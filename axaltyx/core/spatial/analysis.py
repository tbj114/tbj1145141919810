#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
空间分析
"""

import numpy as np


class SpatialAnalysis:
    """空间分析类"""

    @staticmethod
    def euclidean_distance(p1, p2):
        """
        计算欧氏距离

        Args:
            p1: 第一个点的坐标
            p2: 第二个点的坐标

        Returns:
            float: 欧氏距离
        """
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.sqrt(np.sum((p1 - p2) ** 2))

    @staticmethod
    def manhattan_distance(p1, p2):
        """
        计算曼哈顿距离

        Args:
            p1: 第一个点的坐标
            p2: 第二个点的坐标

        Returns:
            float: 曼哈顿距离
        """
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.sum(np.abs(p1 - p2))

    @staticmethod
    def haversine_distance(p1, p2):
        """
        计算两点之间的球面距离（Haversine 公式）

        Args:
            p1: 第一个点的经纬度 (经度, 纬度)
            p2: 第二个点的经纬度 (经度, 纬度)

        Returns:
            float: 球面距离（单位：公里）
        """
        # 地球半径（单位：公里）
        R = 6371.0

        # 转换为弧度
        lon1, lat1 = np.radians(p1)
        lon2, lat2 = np.radians(p2)

        # 差值
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Haversine 公式
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c

        return distance

    @staticmethod
    def knn_search(query_point, points, k=5, distance_metric='euclidean'):
        """
        K最近邻搜索

        Args:
            query_point: 查询点的坐标
            points: 点集合
            k: 最近邻的数量
            distance_metric: 距离度量，'euclidean' 或 'manhattan'

        Returns:
            dict: 包含最近邻点及其距离的字典
        """
        if not isinstance(points, np.ndarray):
            points = np.array(points)

        distances = []
        for point in points:
            if distance_metric == 'euclidean':
                dist = SpatialAnalysis.euclidean_distance(query_point, point)
            elif distance_metric == 'manhattan':
                dist = SpatialAnalysis.manhattan_distance(query_point, point)
            else:
                raise ValueError("距离度量必须是 'euclidean' 或 'manhattan'")
            distances.append((point, dist))

        # 按距离排序
        distances.sort(key=lambda x: x[1])
        # 取前 k 个
        nearest_neighbors = distances[:k]

        return {
            'query_point': query_point,
            'k': k,
            'nearest_neighbors': [{'point': list(neighbor[0]), 'distance': neighbor[1]} for neighbor in nearest_neighbors],
            'distance_metric': distance_metric
        }

    @staticmethod
    def spatial_density(points, bandwidth=1.0, grid_size=10):
        """
        计算空间密度

        Args:
            points: 点集合
            bandwidth: 核密度估计的带宽
            grid_size: 网格大小

        Returns:
            dict: 包含密度网格的字典
        """
        if not isinstance(points, np.ndarray):
            points = np.array(points)

        # 确定边界
        min_x, min_y = np.min(points, axis=0)
        max_x, max_y = np.max(points, axis=0)

        # 创建网格
        x_grid = np.linspace(min_x, max_x, grid_size)
        y_grid = np.linspace(min_y, max_y, grid_size)
        density = np.zeros((grid_size, grid_size))

        # 计算每个网格点的密度
        for i, x in enumerate(x_grid):
            for j, y in enumerate(y_grid):
                grid_point = [x, y]
                for point in points:
                    dist = SpatialAnalysis.euclidean_distance(grid_point, point)
                    # 使用高斯核
                    density[i, j] += np.exp(-(dist ** 2) / (2 * bandwidth ** 2))

        return {
            'density': density.tolist(),
            'x_grid': x_grid.tolist(),
            'y_grid': y_grid.tolist(),
            'bandwidth': bandwidth,
            'grid_size': grid_size
        }
