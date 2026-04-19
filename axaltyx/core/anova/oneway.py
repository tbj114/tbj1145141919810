#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单因素方差分析实现
"""

import math
import numpy as np
from collections import Counter


class OneWayANOVA:
    """单因素方差分析类"""

    @staticmethod
    def _filter_data(data):
        """过滤掉 None 和 NaN 值"""
        return [x for x in data if x is not None and not np.isnan(x)]

    @staticmethod
    def calculate(*groups):
        """
        执行单因素方差分析

        Args:
            *groups: 多个组的数据列表

        Returns:
            dict: 包含方差分析结果的字典
        """
        # 过滤并验证各组数据
        filtered_groups = []
        group_names = []
        for i, group in enumerate(groups):
            filtered = OneWayANOVA._filter_data(group)
            if len(filtered) >= 2:
                filtered_groups.append(filtered)
                group_names.append(f"Group {i+1}")

        if len(filtered_groups) < 2:
            return {
                'f_value': None,
                'df_between': None,
                'df_within': None,
                'p_value': None,
                'group_stats': None,
                'sum_sq_between': None,
                'sum_sq_within': None,
                'mean_sq_between': None,
                'mean_sq_within': None
            }

        # 计算各组统计量
        group_stats = []
        all_data = []
        n_total = 0

        for i, group in enumerate(filtered_groups):
            n = len(group)
            mean = np.mean(group)
            var = np.var(group, ddof=1)
            std = math.sqrt(var)

            group_stats.append({
                'name': group_names[i],
                'count': n,
                'mean': mean,
                'std_dev': std,
                'variance': var
            })

            all_data.extend(group)
            n_total += n

        # 计算总均值
        grand_mean = np.mean(all_data)

        # 计算组间平方和 (SSB)
        sum_sq_between = 0
        for stats in group_stats:
            n = stats['count']
            mean = stats['mean']
            sum_sq_between += n * (mean - grand_mean) ** 2

        # 计算组内平方和 (SSW)
        sum_sq_within = 0
        for i, group in enumerate(filtered_groups):
            mean = group_stats[i]['mean']
            for x in group:
                sum_sq_within += (x - mean) ** 2

        # 计算自由度
        k = len(filtered_groups)  # 组数
        df_between = k - 1
        df_within = n_total - k

        # 计算均方 (MS)
        mean_sq_between = sum_sq_between / df_between if df_between > 0 else None
        mean_sq_within = sum_sq_within / df_within if df_within > 0 else None

        # 计算 F 值
        f_value = None
        p_value = None

        if mean_sq_between is not None and mean_sq_within is not None and mean_sq_within > 0:
            f_value = mean_sq_between / mean_sq_within
            p_value = OneWayANOVA._calculate_p_value(f_value, df_between, df_within)

        return {
            'f_value': f_value,
            'df_between': df_between,
            'df_within': df_within,
            'p_value': p_value,
            'group_stats': group_stats,
            'sum_sq_between': sum_sq_between,
            'sum_sq_within': sum_sq_within,
            'mean_sq_between': mean_sq_between,
            'mean_sq_within': mean_sq_within,
            'total_count': n_total,
            'grand_mean': grand_mean
        }

    @staticmethod
    def _calculate_p_value(f_value, df1, df2):
        """计算 F 检验的 p 值"""
        if df1 <= 0 or df2 <= 0 or f_value is None:
            return None

        try:
            from scipy import stats
            p_value = 1 - stats.f.cdf(f_value, df1, df2)
        except ImportError:
            p_value = None

        return p_value

    @staticmethod
    def tukey_hsd(*groups):
        """
        执行 Tukey's HSD 事后检验

        Args:
            *groups: 多个组的数据列表

        Returns:
            dict: 包含 Tukey 检验结果的字典
        """
        # 先计算单因素 ANOVA
        anova_result = OneWayANOVA.calculate(*groups)
        if anova_result['f_value'] is None:
            return None

        # 获取基本信息
        group_stats = anova_result['group_stats']
        k = len(group_stats)
        if k < 2:
            return None

        mse = anova_result['mean_sq_within']
        if mse is None or mse <= 0:
            return None

        # 计算所有组对的比较
        comparisons = []

        for i in range(k):
            for j in range(i + 1, k):
                # 获取组数据
                group_i = groups[i]
                group_j = groups[j]

                # 过滤数据
                filtered_i = OneWayANOVA._filter_data(group_i)
                filtered_j = OneWayANOVA._filter_data(group_j)

                if len(filtered_i) < 2 or len(filtered_j) < 2:
                    continue

                # 计算均值
                mean_i = np.mean(filtered_i)
                mean_j = np.mean(filtered_j)
                n_i = len(filtered_i)
                n_j = len(filtered_j)

                # 计算标准误差
                se = math.sqrt(mse * (1/n_i + 1/n_j))

                # 计算均值差
                mean_diff = mean_i - mean_j

                # 计算 t 值
                t_value = abs(mean_diff) / se

                # 计算 p 值
                p_value = OneWayANOVA._calculate_tukey_p_value(t_value, k, anova_result['df_within'])

                comparisons.append({
                    'group_i': group_stats[i]['name'],
                    'group_j': group_stats[j]['name'],
                    'mean_i': mean_i,
                    'mean_j': mean_j,
                    'mean_diff': mean_diff,
                    't_value': t_value,
                    'p_value': p_value
                })

        return {
            'anova_result': anova_result,
            'comparisons': comparisons
        }

    @staticmethod
    def _calculate_tukey_p_value(q_value, k, df):
        """计算 Tukey HSD 的 p 值"""
        try:
            from scipy import stats
            # 使用 studentized range 分布
            p_value = 1 - stats.studentized_range.cdf(q_value, k, df)
        except ImportError:
            p_value = None

        return p_value
