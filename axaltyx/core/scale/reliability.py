#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信度分析
"""

import numpy as np


class Reliability:
    """信度分析类"""

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
    def cronbach_alpha(data):
        """
        计算 Cronbach's Alpha 信度系数

        Args:
            data: 输入数据矩阵，形状为 (n_samples, n_items)

        Returns:
            dict: 包含 Cronbach's Alpha 及相关指标的字典
        """
        # 过滤数据
        X = Reliability._filter_data(data)
        n_samples, n_items = X.shape
        
        if n_items < 2:
            raise ValueError("至少需要 2 个项目来计算 Cronbach's Alpha")
        
        # 计算每个项目的方差
        item_variances = np.var(X, axis=0, ddof=1)
        
        # 计算总分的方差
        total_scores = np.sum(X, axis=1)
        total_variance = np.var(total_scores, ddof=1)
        
        # 计算 Cronbach's Alpha
        if total_variance == 0:
            alpha = 0
        else:
            alpha = (n_items / (n_items - 1)) * (1 - np.sum(item_variances) / total_variance)
        
        # 计算标准化 Cronbach's Alpha
        # 先标准化数据
        X_std = (X - np.mean(X, axis=0)) / np.std(X, axis=0, ddof=1)
        total_scores_std = np.sum(X_std, axis=1)
        total_variance_std = np.var(total_scores_std, ddof=1)
        item_variances_std = np.var(X_std, axis=0, ddof=1)
        
        if total_variance_std == 0:
            alpha_std = 0
        else:
            alpha_std = (n_items / (n_items - 1)) * (1 - np.sum(item_variances_std) / total_variance_std)
        
        return {
            'n_samples': n_samples,
            'n_items': n_items,
            'cronbach_alpha': alpha,
            'standardized_cronbach_alpha': alpha_std,
            'item_variances': item_variances,
            'total_variance': total_variance,
            'mean_item_variance': np.mean(item_variances),
            'std_item_variance': np.std(item_variances, ddof=1)
        }

    @staticmethod
    def split_half_reliability(data, split_method='random', n_splits=100, random_state=None):
        """
        计算分半信度

        Args:
            data: 输入数据矩阵
            split_method: 分半方法，'random'（随机分半，默认）或 'odd_even'（奇偶分半）
            n_splits: 随机分半时的重复次数
            random_state: 随机种子

        Returns:
            dict: 包含分半信度及相关指标的字典
        """
        # 过滤数据
        X = Reliability._filter_data(data)
        n_samples, n_items = X.shape
        
        if n_items < 2:
            raise ValueError("至少需要 2 个项目来计算分半信度")
        
        if split_method == 'odd_even':
            # 奇偶分半
            odd_items = X[:, ::2]
            even_items = X[:, 1::2]
            
            if odd_items.shape[1] == 0 or even_items.shape[1] == 0:
                raise ValueError("无法进行奇偶分半，项目数量不足")
            
            # 计算两半的总分
            odd_scores = np.sum(odd_items, axis=1)
            even_scores = np.sum(even_items, axis=1)
            
            # 计算相关系数
            correlation = np.corrcoef(odd_scores, even_scores)[0, 1]
            
            # 使用 Spearman-Brown 公式校正
            spearman_brown = (2 * correlation) / (1 + correlation)
            
            return {
                'method': 'odd_even',
                'correlation': correlation,
                'spearman_brown': spearman_brown,
                'n_samples': n_samples,
                'n_items_half1': odd_items.shape[1],
                'n_items_half2': even_items.shape[1]
            }
        
        elif split_method == 'random':
            # 随机分半
            if random_state is not None:
                np.random.seed(random_state)
            
            correlations = []
            for i in range(n_splits):
                # 随机分配项目到两半
                mask = np.random.choice([True, False], size=n_items, replace=True)
                half1 = X[:, mask]
                half2 = X[:, ~mask]
                
                if half1.shape[1] == 0 or half2.shape[1] == 0:
                    continue
                
                # 计算两半的总分
                scores1 = np.sum(half1, axis=1)
                scores2 = np.sum(half2, axis=1)
                
                # 计算相关系数
                corr = np.corrcoef(scores1, scores2)[0, 1]
                correlations.append(corr)
            
            if not correlations:
                raise ValueError("无法进行随机分半，尝试调整 n_splits")
            
            mean_correlation = np.mean(correlations)
            spearman_brown = (2 * mean_correlation) / (1 + mean_correlation)
            
            return {
                'method': 'random',
                'mean_correlation': mean_correlation,
                'spearman_brown': spearman_brown,
                'n_splits': n_splits,
                'n_samples': n_samples,
                'n_items': n_items
            }
        
        else:
            raise ValueError("分半方法必须是 'random' 或 'odd_even'")
