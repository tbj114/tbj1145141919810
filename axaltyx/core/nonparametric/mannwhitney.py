#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mann-Whitney U 检验
"""

import numpy as np


class MannWhitneyU:
    """Mann-Whitney U 检验类"""

    @staticmethod
    def _filter_data(x, y):
        """过滤无效数据"""
        # 处理 x
        x_valid = [v for v in x if v is not None and not np.isnan(v)]
        # 处理 y
        y_valid = [v for v in y if v is not None and not np.isnan(v)]
        return np.array(x_valid), np.array(y_valid)

    @staticmethod
    def test(x, y, alternative='two-sided', continuity=True):
        """
        执行 Mann-Whitney U 检验

        Args:
            x: 第一组数据
            y: 第二组数据
            alternative: 备择假设，'two-sided'（双侧，'less' 单侧小于，'greater' 单侧大于
            continuity: 是否使用连续性修正

        Returns:
            dict: 包含检验结果的字典
        """
        x_arr, y_arr = MannWhitneyU._filter_data(x, y)
        n1 = len(x_arr)
        n2 = len(y_arr)

        if n1 < 2 or n2 < 2:
            return {
                'n1': len(x),
                'n2': len(y),
                'valid_n1': n1,
                'valid_n2': n2,
                'statistic': None,
                'p_value': None
            }

        # 合并并排序
        combined = np.concatenate([x_arr, y_arr])
        ranks = MannWhitneyU._rank_data(combined)
        ranks_x = ranks[:n1]
        ranks_y = ranks[n1:]

        # 计算 U 统计量
        R1 = np.sum(ranks_x)
        U1 = n1 * n2 + n1 * (n1 + 1) / 2 - R1
        U2 = n1 * n2 - U1
        U = min(U1, U2)

        # 计算 p 值
        p_value = MannWhitneyU._calculate_p_value(U, n1, n2, alternative, continuity)

        return {
            'n1': len(x),
            'n2': len(y),
            'valid_n1': n1,
            'valid_n2': n2,
            'U': U,
            'U1': U1,
            'U2': U2,
            'R1': R1,
            'statistic': U,
            'p_value': p_value
        }

    @staticmethod
    def _rank_data(data):
        """对数据进行排序，处理并列排名"""
        sorted_indices = np.argsort(data)
        ranks = np.empty_like(data)
        ranks[sorted_indices] = np.arange(1, len(data) + 1)

        # 处理并列值
        unique_values, counts = np.unique(data, return_counts=True)
        for value, count in zip(unique_values, counts):
            if count > 1:
                indices = np.where(data == value)[0]
                ranks[indices] = np.mean(ranks[indices])

        return ranks

    @staticmethod
    def _calculate_p_value(U, n1, n2, alternative, continuity):
        """计算 Mann-Whitney U 检验的 p 值"""
        try:
            from scipy import stats

            # 使用正态近似
            mu_U = n1 * n2 / 2
            sigma_U = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
            z = (U - mu_U) / sigma_U
            if continuity:
                z = (U - mu_U + 0.5) / sigma_U if U < mu_U else (U - mu_U - 0.5) / sigma_U

            if alternative == 'two-sided':
                p_value = 2 * min(stats.norm.cdf(z), 1 - stats.norm.cdf(z))
            elif alternative == 'less':
                p_value = stats.norm.cdf(z)
            else:
                p_value = 1 - stats.norm.cdf(z)

            return p_value
        except ImportError:
            return None
