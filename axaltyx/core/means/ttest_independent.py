#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立样本 t 检验实现
"""

import math
import numpy as np


class TTestIndependent:
    """独立样本 t 检验类"""

    @staticmethod
    def _filter_data(data):
        """过滤掉 None 和 NaN 值"""
        return [x for x in data if x is not None and not np.isnan(x)]

    @staticmethod
    def calculate(data1, data2, equal_var=True):
        """
        执行独立样本 t 检验

        Args:
            data1: 第一个样本数据列表
            data2: 第二个样本数据列表
            equal_var: 是否假设方差相等，默认为 True

        Returns:
            dict: 包含 t 值、自由度、p 值等统计信息的字典
        """
        filtered_data1 = TTestIndependent._filter_data(data1)
        filtered_data2 = TTestIndependent._filter_data(data2)

        n1, n2 = len(filtered_data1), len(filtered_data2)

        if n1 < 2 or n2 < 2:
            return {
                't_value': None,
                'df': None,
                'p_value': None,
                'mean1': None,
                'mean2': None,
                'std_dev1': None,
                'std_dev2': None,
                'equal_var': equal_var,
                'count1': len(data1),
                'count2': len(data2),
                'valid_count1': n1,
                'valid_count2': n2
            }

        # 计算样本均值和方差
        mean1 = np.mean(filtered_data1)
        mean2 = np.mean(filtered_data2)
        var1 = np.var(filtered_data1, ddof=1)
        var2 = np.var(filtered_data2, ddof=1)

        if equal_var:
            # 合并方差（pooled variance）
            pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
            se = math.sqrt(pooled_var * (1/n1 + 1/n2))
            df = n1 + n2 - 2
        else:
            # Welch-Satterthwaite 近似（不假设方差相等）
            se = math.sqrt(var1/n1 + var2/n2)
            # 计算 Welch-Satterthwaite 自由度
            df_num = (var1/n1 + var2/n2) ** 2
            df_den = (var1/(n1**2 * (n1 - 1))) + (var2/(n2**2 * (n2 - 1)))
            df = df_num / df_den if df_den != 0 else 1

        # 计算 t 值
        t_value = (mean1 - mean2) / se

        # 计算 p 值
        p_value = TTestIndependent._calculate_p_value(t_value, df)

        return {
            't_value': t_value,
            'df': df,
            'p_value': p_value,
            'mean1': mean1,
            'mean2': mean2,
            'mean_diff': mean1 - mean2,
            'std_dev1': math.sqrt(var1),
            'std_dev2': math.sqrt(var2),
            'var1': var1,
            'var2': var2,
            'equal_var': equal_var,
            'count1': len(data1),
            'count2': len(data2),
            'valid_count1': n1,
            'valid_count2': n2
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
    def levene_test(data1, data2):
        """
        执行 Levene 方差齐性检验

        Args:
            data1: 第一个样本数据列表
            data2: 第二个样本数据列表

        Returns:
            dict: 包含 F 值、p 值等的字典
        """
        filtered_data1 = TTestIndependent._filter_data(data1)
        filtered_data2 = TTestIndependent._filter_data(data2)

        n1, n2 = len(filtered_data1), len(filtered_data2)

        if n1 < 2 or n2 < 2:
            return {
                'w_value': None,
                'df1': None,
                'df2': None,
                'p_value': None
            }

        # 计算各组中位数
        median1 = np.median(filtered_data1)
        median2 = np.median(filtered_data2)

        # 计算绝对偏差
        z1 = [abs(x - median1) for x in filtered_data1]
        z2 = [abs(x - median2) for x in filtered_data2]

        # 计算各组均值
        z_mean1 = np.mean(z1)
        z_mean2 = np.mean(z2)
        z_total_mean = np.mean(z1 + z2)

        # 计算平方和
        numerator = (n1 * (z_mean1 - z_total_mean) ** 2 + n2 * (z_mean2 - z_total_mean) ** 2)
        denominator = (sum((x - z_mean1) ** 2 for x in z1) + sum((x - z_mean2) ** 2 for x in z2))

        # 计算 W 值
        if denominator == 0:
            w_value = None
        else:
            w_value = ((n1 + n2 - 2) * numerator) / denominator

        df1 = 1
        df2 = n1 + n2 - 2

        # 计算 p 值
        p_value = None
        if w_value is not None and df2 > 0:
            try:
                from scipy import stats
                p_value = 1 - stats.f.cdf(w_value, df1, df2)
            except ImportError:
                pass

        return {
            'w_value': w_value,
            'df1': df1,
            'df2': df2,
            'p_value': p_value
        }
