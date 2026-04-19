#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配对样本 t 检验实现
"""

import math
import numpy as np


class TTestPaired:
    """配对样本 t 检验类"""

    @staticmethod
    def _filter_data(data1, data2):
        """
        过滤掉包含 None 和 NaN 的数据对
        
        Args:
            data1: 第一个样本数据列表
            data2: 第二个样本数据列表
            
        Returns:
            tuple: (过滤后的 data1, 过滤后的 data2)
        """
        filtered_data1 = []
        filtered_data2 = []

        for x, y in zip(data1, data2):
            # 检查 x 是否有效
            x_valid = False
            if x is not None:
                if isinstance(x, (int, float)):
                    if not np.isnan(x):
                        x_valid = True
                else:
                    x_valid = True

            # 检查 y 是否有效
            y_valid = False
            if y is not None:
                if isinstance(y, (int, float)):
                    if not np.isnan(y):
                        y_valid = True
                else:
                    y_valid = True

            if x_valid and y_valid:
                filtered_data1.append(x)
                filtered_data2.append(y)

        return filtered_data1, filtered_data2

    @staticmethod
    def calculate(data1, data2):
        """
        执行配对样本 t 检验

        Args:
            data1: 第一个样本数据列表（例如：前测数据）
            data2: 第二个样本数据列表（例如：后测数据）

        Returns:
            dict: 包含 t 值、自由度、p 值等统计信息的字典
        """
        filtered_data1, filtered_data2 = TTestPaired._filter_data(data1, data2)
        n = len(filtered_data1)

        if n < 2:
            return {
                't_value': None,
                'df': None,
                'p_value': None,
                'mean1': None,
                'mean2': None,
                'mean_diff': None,
                'std_dev_diff': None,
                'count': len(data1),
                'valid_count': n
            }

        # 计算差值
        diffs = [x - y for x, y in zip(filtered_data1, filtered_data2)]

        # 计算差值的均值和标准差
        mean_diff = np.mean(diffs)
        std_dev_diff = np.std(diffs, ddof=1)

        # 计算样本均值
        mean1 = np.mean(filtered_data1)
        mean2 = np.mean(filtered_data2)

        # 计算 t 值
        se_diff = std_dev_diff / math.sqrt(n)
        t_value = mean_diff / se_diff

        # 自由度
        df = n - 1

        # 计算 p 值
        p_value = TTestPaired._calculate_p_value(t_value, df)

        # 计算置信区间
        ci = TTestPaired._calculate_confidence_interval(mean_diff, std_dev_diff, n)

        return {
            't_value': t_value,
            'df': df,
            'p_value': p_value,
            'mean1': mean1,
            'mean2': mean2,
            'mean_diff': mean_diff,
            'std_dev_diff': std_dev_diff,
            'confidence_interval': ci,
            'count': len(data1),
            'valid_count': n
        }

    @staticmethod
    def _calculate_p_value(t_value, df):
        """计算 t 检验的 p 值（双侧）"""
        if df <= 0:
            return None

        try:
            from scipy import stats
            p_value = 2 * (1 - stats.t.cdf(abs(t_value), df))
        except ImportError:
            p_value = None

        return p_value

    @staticmethod
    def _calculate_confidence_interval(mean_diff, std_dev_diff, n, confidence_level=0.95):
        """计算差值的置信区间"""
        alpha = 1 - confidence_level

        try:
            from scipy import stats
            t_critical = stats.t.ppf(1 - alpha/2, n-1)
        except ImportError:
            t_critical = 1.96

        margin_of_error = t_critical * (std_dev_diff / math.sqrt(n))
        ci_lower = mean_diff - margin_of_error
        ci_upper = mean_diff + margin_of_error

        return (ci_lower, ci_upper)
