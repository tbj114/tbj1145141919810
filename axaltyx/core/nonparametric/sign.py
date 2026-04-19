#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
符号检验
"""

import numpy as np


class SignTest:
    """符号检验类"""

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
    def test(x, y=None, alternative='two-sided'):
        """
        执行符号检验

        Args:
            x: 第一组数据或差值
            y: 第二组数据（可选）
            alternative: 备择假设，'two-sided'（双侧），'less'（单侧小于），'greater'（单侧大于）

        Returns:
            dict: 包含检验结果的字典
        """
        if y is not None:
            x_arr, y_arr = SignTest._filter_data(x, y)
            if x_arr is None:
                return None
            diff = x_arr - y_arr
        else:
            diff = SignTest._filter_data(x)
            if diff is None:
                return None

        # 计算正号、负号和零的数量
        n_positive = np.sum(diff > 0)
        n_negative = np.sum(diff < 0)
        n_zero = np.sum(diff == 0)
        n = n_positive + n_negative

        if n < 1:
            return {
                'n': len(x),
                'valid_n': n,
                'n_positive': n_positive,
                'n_negative': n_negative,
                'n_zero': n_zero,
                'statistic': None,
                'p_value': None
            }

        # 检验统计量是较小的那个计数
        S = min(n_positive, n_negative)

        # 计算 p 值
        p_value = SignTest._calculate_p_value(S, n, alternative)

        return {
            'n': len(x),
            'valid_n': n,
            'n_positive': n_positive,
            'n_negative': n_negative,
            'n_zero': n_zero,
            'statistic': S,
            'p_value': p_value
        }

    @staticmethod
    def _calculate_p_value(S, n, alternative):
        """计算符号检验的 p 值"""
        try:
            from scipy import stats

            if alternative == 'two-sided':
                p_value = 2 * min(stats.binom.cdf(S, n, 0.5), 1 - stats.binom.cdf(S - 1, n, 0.5))
            elif alternative == 'less':
                p_value = stats.binom.cdf(S, n, 0.5)
            else:
                p_value = 1 - stats.binom.cdf(S - 1, n, 0.5)

            return p_value
        except ImportError:
            return None
