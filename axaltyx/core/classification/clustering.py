#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚类分析
"""

import numpy as np


class KMeans:
    """K-均值聚类"""

    @staticmethod
    def _filter_data(data):
        """过滤无效数据"""
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        
        if data.ndim != 2:
            raise ValueError("数据必须是二维数组")
        
        # 过滤含有 NaN 的行
        mask = ~np.isnan(data).any(axis=1)
        filtered_data = data[mask]
        
        return filtered_data

    @staticmethod
    def fit(data, n_clusters=3, max_iter=100, tol=1e-4, random_state=None):
        """
        执行 K-均值聚类

        Args:
            data: 输入数据矩阵，形状为 (n_samples, n_features)
            n_clusters: 聚类数量
            max_iter: 最大迭代次数
            tol: 收敛阈值
            random_state: 随机种子

        Returns:
            dict: 包含聚类结果的字典
        """
        # 过滤数据
        X = KMeans._filter_data(data)
        n_samples, n_features = X.shape
        
        # 初始化聚类中心
        if random_state is not None:
            np.random.seed(random_state)
        
        # 随机选择初始聚类中心
        centroids = X[np.random.choice(n_samples, n_clusters, replace=False)]
        
        for i in range(max_iter):
            # 计算每个样本到聚类中心的距离
            distances = np.sqrt(((X[:, np.newaxis] - centroids) ** 2).sum(axis=2))
            
            # 分配样本到最近的聚类中心
            labels = np.argmin(distances, axis=1)
            
            # 计算新的聚类中心
            new_centroids = np.array([X[labels == j].mean(axis=0) for j in range(n_clusters)])
            
            # 检查收敛
            if np.max(np.abs(new_centroids - centroids)) < tol:
                break
            
            centroids = new_centroids
        
        # 计算聚类内平方和
        inertia = 0
        for j in range(n_clusters):
            cluster_points = X[labels == j]
            if len(cluster_points) > 0:
                inertia += ((cluster_points - centroids[j]) ** 2).sum()
        
        return {
            'n_clusters': n_clusters,
            'labels': labels,
            'centroids': centroids,
            'inertia': inertia,
            'n_iter': i + 1
        }

    @staticmethod
    def predict(data, centroids):
        """
        预测新数据的聚类标签

        Args:
            data: 新数据矩阵
            centroids: 聚类中心

        Returns:
            np.ndarray: 聚类标签
        """
        X = KMeans._filter_data(data)
        distances = np.sqrt(((X[:, np.newaxis] - centroids) ** 2).sum(axis=2))
        return np.argmin(distances, axis=1)


class HierarchicalClustering:
    """层次聚类"""

    @staticmethod
    def _filter_data(data):
        """过滤无效数据"""
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        
        if data.ndim != 2:
            raise ValueError("数据必须是二维数组")
        
        # 过滤含有 NaN 的行
        mask = ~np.isnan(data).any(axis=1)
        filtered_data = data[mask]
        
        return filtered_data

    @staticmethod
    def fit(data, method='ward'):
        """
        执行层次聚类

        Args:
            data: 输入数据矩阵，形状为 (n_samples, n_features)
            method: 距离计算方法，'ward'（默认）、'single'、'complete'、'average'

        Returns:
            dict: 包含聚类结果的字典
        """
        # 过滤数据
        X = HierarchicalClustering._filter_data(data)
        n_samples = X.shape[0]
        
        # 计算距离矩阵
        distances = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                distances[i, j] = np.sqrt(((X[i] - X[j]) ** 2).sum())
                distances[j, i] = distances[i, j]
        
        # 初始化聚类
        clusters = [[i] for i in range(n_samples)]
        merge_history = []
        
        while len(clusters) > 1:
            # 找到距离最近的两个聚类
            min_dist = float('inf')
            merge_idx = (0, 1)
            
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    if method == 'ward':
                        # Ward 方法：最小化方差
                        dist = HierarchicalClustering._ward_distance(X, clusters[i], clusters[j])
                    elif method == 'single':
                        # 单链接：最小距离
                        dist = HierarchicalClustering._single_link_distance(distances, clusters[i], clusters[j])
                    elif method == 'complete':
                        # 完全链接：最大距离
                        dist = HierarchicalClustering._complete_link_distance(distances, clusters[i], clusters[j])
                    elif method == 'average':
                        # 平均链接：平均距离
                        dist = HierarchicalClustering._average_link_distance(distances, clusters[i], clusters[j])
                    else:
                        raise ValueError("方法必须是 'ward'、'single'、'complete' 或 'average'")
                    
                    if dist < min_dist:
                        min_dist = dist
                        merge_idx = (i, j)
            
            # 合并聚类
            i, j = merge_idx
            new_cluster = clusters[i] + clusters[j]
            merge_history.append((clusters[i], clusters[j], min_dist))
            
            # 更新聚类列表
            clusters = [c for k, c in enumerate(clusters) if k not in (i, j)]
            clusters.append(new_cluster)
        
        return {
            'merge_history': merge_history,
            'n_samples': n_samples,
            'method': method
        }

    @staticmethod
    def _ward_distance(X, cluster1, cluster2):
        """Ward 距离"""
        n1, n2 = len(cluster1), len(cluster2)
        mean1 = X[cluster1].mean(axis=0)
        mean2 = X[cluster2].mean(axis=0)
        return n1 * n2 / (n1 + n2) * ((mean1 - mean2) ** 2).sum()

    @staticmethod
    def _single_link_distance(distances, cluster1, cluster2):
        """单链接距离"""
        min_dist = float('inf')
        for i in cluster1:
            for j in cluster2:
                if distances[i, j] < min_dist:
                    min_dist = distances[i, j]
        return min_dist

    @staticmethod
    def _complete_link_distance(distances, cluster1, cluster2):
        """完全链接距离"""
        max_dist = 0
        for i in cluster1:
            for j in cluster2:
                if distances[i, j] > max_dist:
                    max_dist = distances[i, j]
        return max_dist

    @staticmethod
    def _average_link_distance(distances, cluster1, cluster2):
        """平均链接距离"""
        total_dist = 0
        count = 0
        for i in cluster1:
            for j in cluster2:
                total_dist += distances[i, j]
                count += 1
        return total_dist / count
