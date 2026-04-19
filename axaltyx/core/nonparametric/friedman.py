#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Friedman 检验
"""

import numpy as np


class FriedmanTest:
    """Friedman 检验类"""

    @staticmethod
    def _filter_data(*groups):
        """过滤无效数据，确保所有组有相同的有效样本"""
        # 首先过滤无效值
        filtered_groups = []
        for group in groups:
            valid = [v for v in group if v is not None and not np.isnan(v)]
            filtered_groups.append(np.array(valid))
        
        # 检查是否所有组长度相同
        if not filtered_groups:
            return []
        
        n = len(filtered_groups[0])
        for group in filtered_groups[1:]:
            if len(group) != n:
                return []
        
        return filtered_groups

    @staticmethod
    def test(*groups):
        """
        执行 Friedman 检验

        Args:
            *groups: 多个组的数据（每组长度相同）

        Returns:
            dict: 包含检验结果的字典
        """
        filtered_groups = FriedmanTest._filter_data(*groups)
        
        k = len(filtered_groups)
        if k < 2:
            return {
                'k': len(groups),
                'n': None,
                'statistic': None,
                'p_value': None
            }
        
        n = len(filtered_groups[0])
        if n < 2:
            return {
                'k': len(groups),
                'n': n,
                'statistic': None,
                'p_value': None
            }
        
        # 对每个块（每个样本）内的组进行排名
        rank_matrix = np.zeros((n, k))
        for i in range(n):
            values = [group[i] for group in filtered_groups]
            ranks = FriedmanTest._rank_within_block(values)
            rank_matrix[i, :] = ranks
        
        # 计算每个组的秩和
        rank_sums = np.sum(rank_matrix, axis=0)
        
        # 计算统计量
        sum_R_sq = np.sum(rank_sums ** 2)
        chi2 = (12 / (n * k * (k + 1))) * sum_R_sq - 3 * n * (k + 1)
        
        # 计算 p 值
        p_value = FriedmanTest._calculate_p_value(chi2, k - 1)
        
        return {
            'k': len(groups),
            'n': n,
            'statistic': chi2,
            'rank_sums': rank_sums.tolist(),
            'rank_matrix': rank_matrix.tolist(),
            'df': k - 1,
            'p_value': p_value
        }

    @staticmethod
    def _rank_within_block(values):
        """对一个块内的值进行排名"""
        data = np.array(values)
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
    def _calculate_p_value(chi2, df):
        """计算 Friedman 检验的 p 值"""
        try:
            from scipy import stats
            p_value = 1 - stats.chi2.cdf(chi2, df)
            return p_value
        except ImportError:
            return None
