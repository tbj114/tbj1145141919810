#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wilcoxon 符号秩检验
"""

import numpy as np


class WilcoxonSignedRank:
    """Wilcoxon 符号秩检验类"""

    @staticmethod
    def _filter_data(x, y=None):
        """过滤无效数据"""
        if y is None:
            data = [v for v in x if v is not None and not np.isnan(v)]
            return np.array(data)
        else:
            valid_pairs = []
            for xi, yi in zip(x, y):
                x_valid = xi is not None and (not isinstance(xi, float) or not np.isnan(xi))
                y_valid = yi is not None and (not isinstance(yi, float) or not np.isnan(yi))
                if x_valid and y_valid:
                    valid_pairs.append((xi, yi))
            if not valid_pairs:
                return None
            x_arr = np.array([v[0] for v in valid_pairs])
            y_arr = np.array([v[1] for v in valid_pairs])
            return x_arr, y_arr

    @staticmethod
    def test(x, y=None, zero_method='wilcox', correction=True):
        """
        执行 Wilcoxon 符号秩检验

        Args:
            x: 第一组数据或差值
            y: 第二组数据（可选）
            zero_method: 处理零差值的方法，'wilcox'（默认）或 'pratt'
            correction: 是否使用连续性修正

        Returns:
            dict: 包含检验结果的字典
        """
        if y is not None:
            x_arr, y_arr = WilcoxonSignedRank._filter_data(x, y)
            if x_arr is None:
                return None
            diff = x_arr - y_arr
        else:
            diff = WilcoxonSignedRank._filter_data(x)
            if diff is None:
                return None

        # 排除零差值
        if zero_method == 'pratt':
            valid = diff != 0
            diff = diff[valid]
        else:
            valid = diff != 0
            diff = diff[valid]

        n = len(diff)
        if n < 2:
            return {
                'n': len(x),
                'valid_n': n,
                'statistic': None,
                'p_value': None
            }

        # 计算绝对秩
        abs_diff = np.abs(diff)
        ranks = WilcoxonSignedRank._rank_data(abs_diff)

        # 计算符号秩
        sign = np.sign(diff)
        pos_ranks = np.sum(ranks[sign > 0])
        neg_ranks = np.sum(ranks[sign < 0])

        # 计算统计量
        T = min(pos_ranks, neg_ranks)

        # 计算 p 值
        p_value = WilcoxonSignedRank._calculate_p_value(T, n, correction)

        return {
            'n': len(x),
            'valid_n': n,
            'statistic': T,
            'p_value': p_value,
            'pos_ranks': pos_ranks,
            'neg_ranks': neg_ranks
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
    def _calculate_p_value(T, n, correction):
        """计算 Wilcoxon 检验的 p 值"""
        try:
            from scipy import stats

            # 使用 scipy 的 wilcoxon 函数直接计算
            # 这里我们只用于获取 p 值
            # 实际上，为了方便，我们使用正态近似
            mean_T = n * (n + 1) / 4
            var_T = n * (n + 1) * (2 * n + 1) / 24
            z = (T - mean_T) / np.sqrt(var_T)
            if correction:
                z = (T - mean_T + 0.5) / np.sqrt(var_T) if T < mean_T else (T - mean_T - 0.5) / np.sqrt(var_T)
            p_value = 2 * stats.norm.cdf(z)

            return p_value
        except ImportError:
            return None
