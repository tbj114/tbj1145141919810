#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主成分分析 (Principal Component Analysis, PCA)
"""

import numpy as np


class PCA:
    """主成分分析类"""

    @staticmethod
    def _filter_data(data):
        """过滤无效数据"""
        # 确保数据是二维数组
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        
        if data.ndim != 2:
            raise ValueError("数据必须是二维数组")
        
        # 过滤含有 NaN 的行
        mask = ~np.isnan(data).any(axis=1)
        filtered_data = data[mask]
        
        return filtered_data

    @staticmethod
    def fit(data, n_components=None):
        """
        执行主成分分析

        Args:
            data: 输入数据矩阵，形状为 (n_samples, n_features)
            n_components: 要保留的主成分数量，默认为 None（保留所有）

        Returns:
            dict: 包含分析结果的字典
        """
        # 过滤数据
        X = PCA._filter_data(data)
        n_samples, n_features = X.shape
        
        if n_components is None:
            n_components = min(n_samples, n_features)
        elif n_components > min(n_samples, n_features):
            n_components = min(n_samples, n_features)
        
        # 数据标准化
        mean = np.mean(X, axis=0)
        X_centered = X - mean
        
        # 计算协方差矩阵
        cov_matrix = np.cov(X_centered, rowvar=False)
        
        # 计算特征值和特征向量
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # 按特征值降序排序
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        
        # 选择前 n_components 个主成分
        eigenvalues = eigenvalues[:n_components]
        eigenvectors = eigenvectors[:, :n_components]
        
        # 计算主成分得分
        scores = np.dot(X_centered, eigenvectors)
        
        # 计算解释方差
        total_variance = np.sum(eigenvalues)
        explained_variance = eigenvalues / total_variance
        cumulative_variance = np.cumsum(explained_variance)
        
        return {
            'n_components': n_components,
            'n_samples': n_samples,
            'n_features': n_features,
            'mean': mean,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'explained_variance': explained_variance,
            'cumulative_variance': cumulative_variance,
            'scores': scores,
            'total_variance': total_variance
        }

    @staticmethod
    def transform(data, eigenvectors, mean):
        """
        使用已训练的主成分对新数据进行转换

        Args:
            data: 新数据矩阵
            eigenvectors: 主成分向量
            mean: 训练数据的均值

        Returns:
            np.ndarray: 转换后的主成分得分
        """
        X = PCA._filter_data(data)
        X_centered = X - mean
        return np.dot(X_centered, eigenvectors)
