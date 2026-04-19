#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单样本 t 检验实现
"""

import math
import numpy as np


class TTestOne:
    """单样本 t 检验类"""

    @staticmethod
    def _filter_data(data):
        """过滤掉 None 和 NaN 值"""
        return [x for x in data if x is not None and not np.isnan(x)]

    @staticmethod
    def calculate(data, popmean):
        """
        执行单样本 t 检验

        Args:
            data: 样本数据列表
            popmean: 总体均值

        Returns:
            dict: 包含 t 值、自由度、p 值和置信区间的字典
        """
        filtered_data = TTestOne._filter_data(data)
        n = len(filtered_data)
        if n < 2:
            return {
                't_value': None,
                'df': None,
                'p_value': None,
                'confidence_interval': None,
                'mean': None,
                'std_dev': None,
                'count': len(data),
                'valid_count': n
            }

        # 计算样本均值和标准差
        sample_mean = np.mean(filtered_data)
        sample_std = np.std(filtered_data, ddof=1)

        # 计算 t 值
        t_value = (sample_mean - popmean) / (sample_std / math.sqrt(n))

        # 自由度
        df = n - 1

        # 计算 p 值
        p_value = TTestOne._calculate_p_value(t_value, df)

        # 计算 95% 置信区间
        ci = TTestOne._calculate_confidence_interval(sample_mean, sample_std, n)

        return {
            't_value': t_value,
            'df': df,
            'p_value': p_value,
            'confidence_interval': ci,
            'mean': sample_mean,
            'std_dev': sample_std,
            'count': len(data),
            'valid_count': n
        }

    @staticmethod
    def _calculate_p_value(t_value, df):
        """计算 t 检验的 p 值（双侧）"""
        if df <= 0:
            return None

        # 使用 Student's t 分布计算 p 值
        # 这里我们使用了一个简单的实现，但在实际应用中可能需要使用更精确的方法
        # 为了简化，我们使用 scipy 的实现风格，但这里只是一个近似

        # 首先，我们可以使用 scipy 中的统计函数
        try:
            from scipy import stats
            p_value = 2 * (1 - stats.t.cdf(abs(t_value), df))
        except ImportError:
            # 如果没有 scipy，我们使用一个近似方法
            # 对于大样本（df > 30），可以使用正态分布近似
            if df > 30:
                from scipy import stats
                p_value = 2 * (1 - stats.norm.cdf(abs(t_value)))
            else:
                p_value = None

        return p_value

    @staticmethod
    def _calculate_confidence_interval(mean, std_dev, n, confidence_level=0.95):
        """计算置信区间"""
        alpha = 1 - confidence_level

        try:
            from scipy import stats
            t_critical = stats.t.ppf(1 - alpha/2, n-1)
        except ImportError:
            t_critical = 1.96  # 默认使用正态分布 95% 置信区间的临界值

        margin_of_error = t_critical * (std_dev / math.sqrt(n))
        ci_lower = mean - margin_of_error
        ci_upper = mean + margin_of_error

        return (ci_lower, ci_upper)
