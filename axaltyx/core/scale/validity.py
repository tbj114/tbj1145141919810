#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
效度分析
"""

import numpy as np


class Validity:
    """效度分析类"""

    @staticmethod
    def _filter_data(X, y=None):
        """过滤无效数据"""
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        
        if y is not None:
            if not isinstance(y, np.ndarray):
                y = np.array(y)
            
            # 过滤含有 NaN 的行
            mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
            X_filtered = X[mask]
            y_filtered = y[mask]
            return X_filtered, y_filtered
        else:
            # 过滤含有 NaN 的行
            mask = ~np.isnan(X).any(axis=1)
            X_filtered = X[mask]
            return X_filtered

    @staticmethod
    def criterion_validity(X, y):
        """
        计算效标效度（与外部效标的相关）

        Args:
            X: 测量工具的得分矩阵，形状为 (n_samples, n_items)
            y: 效标变量，形状为 (n_samples,)

        Returns:
            dict: 包含效标效度及相关指标的字典
        """
        # 过滤数据
        X, y = Validity._filter_data(X, y)
        n_samples, n_items = X.shape
        
        # 计算总分
        total_scores = np.sum(X, axis=1)
        
        # 计算与效标的相关
        correlation = np.corrcoef(total_scores, y)[0, 1]
        
        # 计算每个项目与效标的相关
        item_correlations = []
        for i in range(n_items):
            item_corr = np.corrcoef(X[:, i], y)[0, 1]
            item_correlations.append(item_corr)
        
        return {
            'n_samples': n_samples,
            'n_items': n_items,
            'total_correlation': correlation,
            'item_correlations': item_correlations,
            'mean_item_correlation': np.mean(item_correlations),
            'std_item_correlation': np.std(item_correlations, ddof=1)
        }

    @staticmethod
    def convergent_validity(X, Y):
        """
        计算收敛效度（与相似构念测量工具的相关）

        Args:
            X: 测量工具 A 的得分矩阵
            Y: 测量工具 B 的得分矩阵（测量相似构念）

        Returns:
            dict: 包含收敛效度及相关指标的字典
        """
        # 过滤数据
        X = Validity._filter_data(X)
        Y = Validity._filter_data(Y)
        
        # 确保样本量一致
        min_samples = min(len(X), len(Y))
        X = X[:min_samples]
        Y = Y[:min_samples]
        
        # 计算总分
        total_X = np.sum(X, axis=1)
        total_Y = np.sum(Y, axis=1)
        
        # 计算相关
        correlation = np.corrcoef(total_X, total_Y)[0, 1]
        
        return {
            'n_samples': min_samples,
            'correlation': correlation
        }

    @staticmethod
    def discriminant_validity(X, Y):
        """
        计算区分效度（与不同构念测量工具的相关）

        Args:
            X: 测量工具 A 的得分矩阵
            Y: 测量工具 B 的得分矩阵（测量不同构念）

        Returns:
            dict: 包含区分效度及相关指标的字典
        """
        # 过滤数据
        X = Validity._filter_data(X)
        Y = Validity._filter_data(Y)
        
        # 确保样本量一致
        min_samples = min(len(X), len(Y))
        X = X[:min_samples]
        Y = Y[:min_samples]
        
        # 计算总分
        total_X = np.sum(X, axis=1)
        total_Y = np.sum(Y, axis=1)
        
        # 计算相关
        correlation = np.corrcoef(total_X, total_Y)[0, 1]
        
        return {
            'n_samples': min_samples,
            'correlation': correlation
        }

    @staticmethod
    def construct_validity_factor_analysis(X, n_factors=1):
        """
        通过因子分析评估构念效度

        Args:
            X: 测量工具的得分矩阵
            n_factors: 因子数量

        Returns:
            dict: 包含因子分析结果的字典
        """
        # 过滤数据
        X = Validity._filter_data(X)
        
        # 使用因子分析模块
        try:
            from axaltyx.core.advanced.factor_analysis import FactorAnalysis
            result = FactorAnalysis.fit(X, n_factors=n_factors)
            
            # 计算因子载荷的均值和标准差
            loadings = result['loadings']
            mean_loading = np.mean(np.abs(loadings))
            std_loading = np.std(np.abs(loadings), ddof=1)
            
            return {
                'n_samples': X.shape[0],
                'n_items': X.shape[1],
                'n_factors': n_factors,
                'mean_factor_loading': mean_loading,
                'std_factor_loading': std_loading,
                'factor_loadings': loadings,
                'communalities': result['communalities']
            }
        except ImportError:
            raise ImportError("因子分析模块未找到")
