#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kruskal-Wallis 检验
"""

import numpy as np


class KruskalWallis:
    """Kruskal-Wallis 检验类"""

    @staticmethod
    def _filter_data(*groups):
        """过滤无效数据"""
        filtered_groups = []
        for group in groups:
            valid = [v for v in group if v is not None and not np.isnan(v)]
            filtered_groups.append(np.array(valid))
        return filtered_groups

    @staticmethod
    def test(*groups):
        """
        执行 Kruskal-Wallis 检验

        Args:
            *groups: 多个组的数据

        Returns:
            dict: 包含检验结果的字典
        """
        filtered_groups = KruskalWallis._filter_data(*groups)
        
        # 检查每个组的大小
        n_list = []
        for i, group in enumerate(filtered_groups):
            n = len(group)
            if n < 2:
                return {
                    'k': len(groups),
                    'n_list': [len(g) for g in groups],
                    'valid_n_list': [len(g) for g in filtered_groups],
                    'statistic': None,
                    'p_value': None
                }
            n_list.append(n)
        
        k = len(filtered_groups)
        N = sum(n_list)
        
        # 合并所有数据并排序
        combined = np.concatenate(filtered_groups)
        ranks = KruskalWallis._rank_data(combined)
        
        # 计算每个组的秩和
        rank_sums = []
        start_idx = 0
        for i in range(k):
            end_idx = start_idx + n_list[i]
            group_ranks = ranks[start_idx:end_idx]
            rank_sums.append(np.sum(group_ranks))
            start_idx = end_idx
        
        # 计算统计量 H
        H = (12 / (N * (N + 1))) * sum((Ri ** 2) / ni for Ri, ni in zip(rank_sums, n_list)) - 3 * (N + 1)
        
        # 处理并列值，校正 H
        unique_values, counts = np.unique(combined, return_counts=True)
        tie_correction = 1 - sum(t**3 - t for t in counts) / (N**3 - N)
        if tie_correction > 0:
            H_corrected = H / tie_correction
        else:
            H_corrected = H
        
        # 计算 p 值
        p_value = KruskalWallis._calculate_p_value(H_corrected, k - 1)
        
        return {
            'k': len(groups),
            'n_list': [len(g) for g in groups],
            'valid_n_list': n_list,
            'N': N,
            'statistic': H_corrected,
            'H': H,
            'tie_correction': tie_correction,
            'rank_sums': rank_sums,
            'df': k - 1,
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
    def _calculate_p_value(H, df):
        """计算 Kruskal-Wallis 检验的 p 值"""
        try:
            from scipy import stats
            p_value = 1 - stats.chi2.cdf(H, df)
            return p_value
        except ImportError:
            return None
