#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游程检验
"""

import numpy as np


class RunsTest:
    """游程检验类"""

    @staticmethod
    def _filter_data(x):
        """过滤无效数据"""
        data = [v for v in x if v is not None and not np.isnan(v)]
        return np.array(data)

    @staticmethod
    def test(x, cut='median'):
        """
        执行游程检验

        Args:
            x: 数据序列
            cut: 划分点，'median'（中位数，默认）或 'mean'（均值）

        Returns:
            dict: 包含检验结果的字典
        """
        x_arr = RunsTest._filter_data(x)
        n = len(x_arr)

        if n < 2:
            return {
                'n': len(x),
                'valid_n': n,
                'statistic': None,
                'p_value': None
            }

        # 确定划分点
        if cut == 'median':
            cut_point = np.median(x_arr)
        else:
            cut_point = np.mean(x_arr)

        # 计算游程数
        # 将数据分为高于和低于划分点（等于的排除）
        above = x_arr > cut_point
        below = x_arr < cut_point
        n1 = np.sum(above)
        n2 = np.sum(below)

        if n1 < 1 or n2 < 1:
            return {
                'n': len(x),
                'valid_n': n,
                'cut_point': cut_point,
                'n1': n1,
                'n2': n2,
                'statistic': None,
                'p_value': None
            }

        # 计算游程数
        runs = 1
        prev = x_arr[0] > cut_point
        for val in x_arr[1:]:
            curr = val > cut_point
            if curr != prev:
                runs += 1
                prev = curr

        # 计算期望和方差
        N = n1 + n2
        expected_runs = (2 * n1 * n2 / N) + 1
        var_runs = (2 * n1 * n2 * (2 * n1 * n2 - N)) / (N ** 2 * (N - 1))

        # 计算 z 统计量
        z = (runs - expected_runs) / np.sqrt(var_runs)

        # 计算 p 值
        p_value = RunsTest._calculate_p_value(z)

        return {
            'n': len(x),
            'valid_n': n,
            'cut_point': cut_point,
            'n1': n1,
            'n2': n2,
            'N': N,
            'statistic': runs,
            'expected_runs': expected_runs,
            'var_runs': var_runs,
            'z': z,
            'p_value': p_value
        }

    @staticmethod
    def _calculate_p_value(z):
        """计算游程检验的 p 值"""
        try:
            from scipy import stats
            p_value = 2 * min(stats.norm.cdf(z), 1 - stats.norm.cdf(z))
            return p_value
        except ImportError:
            return None
