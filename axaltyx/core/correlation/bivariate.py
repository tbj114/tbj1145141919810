#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双变量相关分析实现
"""

import numpy as np


class BivariateCorrelation:
    """双变量相关分析类"""

    @staticmethod
    def _filter_data(x, y):
        """过滤掉包含 None 和 NaN 的数据"""
        valid_x = []
        valid_y = []
        for xi, yi in zip(x, y):
            x_valid = xi is not None and (
                not isinstance(xi, (int, float)) or not np.isnan(xi)
            )
            y_valid = yi is not None and (
                not isinstance(yi, (int, float)) or not np.isnan(yi)
            )
            if x_valid and y_valid:
                valid_x.append(xi)
                valid_y.append(yi)
        return np.array(valid_x), np.array(valid_y)

    @staticmethod
    def pearson(x, y):
        """
        计算 Pearson 相关系数

        Args:
            x: 第一个变量的数据
            y: 第二个变量的数据

        Returns:
            dict: 包含相关系数、p值、自由度等的字典
        """
        x_arr, y_arr = BivariateCorrelation._filter_data(x, y)
        n = len(x_arr)

        if n < 2:
            return {
                'correlation': None,
                'p_value': None,
                'n': n,
                'valid_n': len(x_arr),
                'mean_x': None,
                'mean_y': None,
                'std_x': None,
                'std_y': None
            }

        # 计算均值和标准差
        mean_x = np.mean(x_arr)
        mean_y = np.mean(y_arr)
        std_x = np.std(x_arr, ddof=1)
        std_y = np.std(y_arr, ddof=1)

        if std_x == 0 or std_y == 0:
            return {
                'correlation': None,
                'p_value': None,
                'n': len(x),
                'valid_n': len(x_arr),
                'mean_x': mean_x,
                'mean_y': mean_y,
                'std_x': std_x,
                'std_y': std_y
            }

        # 计算 Pearson 相关系数
        numerator = np.sum((x_arr - mean_x) * (y_arr - mean_y))
        denominator = np.sqrt(np.sum((x_arr - mean_x) ** 2) * np.sum((y_arr - mean_y) ** 2))
        r = numerator / denominator if denominator != 0 else None

        # 计算 p 值
        p_value = None
        if r is not None:
            try:
                from scipy import stats
                t_stat = r * np.sqrt((n - 2) / (1 - r ** 2)) if (1 - r ** 2) != 0 else None
                if t_stat is not None:
                    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))
            except ImportError:
                pass

        return {
            'correlation': r,
            'p_value': p_value,
            'n': len(x),
            'valid_n': n,
            'df': n - 2,
            'mean_x': mean_x,
            'mean_y': mean_y,
            'std_x': std_x,
            'std_y': std_y
        }

    @staticmethod
    def spearman(x, y):
        """
        计算 Spearman 秩相关系数

        Args:
            x: 第一个变量的数据
            y: 第二个变量的数据

        Returns:
            dict: 包含相关系数、p值等的字典
        """
        x_arr, y_arr = BivariateCorrelation._filter_data(x, y)
        n = len(x_arr)

        if n < 2:
            return {
                'correlation': None,
                'p_value': None,
                'n': len(x),
                'valid_n': n
            }

        # 计算秩
        def rank_data(arr):
            sorted_indices = np.argsort(arr)
            ranks = np.empty_like(sorted_indices)
            ranks[sorted_indices] = np.arange(1, len(arr) + 1)
            # 处理并列值
            unique, counts = np.unique(arr, return_counts=True)
            for val, count in zip(unique, counts):
                if count > 1:
                    indices = np.where(arr == val)[0]
                    ranks[indices] = np.mean(ranks[indices])
            return ranks

        rank_x = rank_data(x_arr)
        rank_y = rank_data(y_arr)

        # 使用秩计算 Pearson 相关
        return BivariateCorrelation.pearson(rank_x, rank_y)

    @staticmethod
    def correlation_matrix(data):
        """
        计算相关矩阵

        Args:
            data: 数据矩阵，每列是一个变量

        Returns:
            dict: 包含相关系数矩阵和p值矩阵的字典
        """
        n_vars = data.shape[1] if len(data.shape) > 1 else 1
        if n_vars <= 1:
            return None

        corr_matrix = np.zeros((n_vars, n_vars))
        p_matrix = np.zeros((n_vars, n_vars))

        for i in range(n_vars):
            for j in range(i, n_vars):
                if i == j:
                    corr_matrix[i, j] = 1.0
                    p_matrix[i, j] = 1.0
                else:
                    result = BivariateCorrelation.pearson(data[:, i], data[:, j])
                    corr_matrix[i, j] = result['correlation'] if result['correlation'] is not None else np.nan
                    corr_matrix[j, i] = corr_matrix[i, j]
                    p_matrix[i, j] = result['p_value'] if result['p_value'] is not None else np.nan
                    p_matrix[j, i] = p_matrix[i, j]

        return {
            'correlation_matrix': corr_matrix,
            'p_value_matrix': p_matrix,
            'n_vars': n_vars
        }
