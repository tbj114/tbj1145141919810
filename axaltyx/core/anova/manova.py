#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多元方差分析实现
"""

import numpy as np


class MANOVA:
    """多元方差分析类"""

    @staticmethod
    def _filter_data(data):
        """过滤掉包含 None 和 NaN 的数据"""
        filtered_data = []
        for row in data:
            is_valid = True
            for x in row:
                if x is None or (isinstance(x, (int, float)) and np.isnan(x)):
                    is_valid = False
                    break
            if is_valid:
                filtered_data.append(row)
        return np.array(filtered_data)

    @staticmethod
    def calculate(data, group_labels):
        """
        执行多元方差分析

        Args:
            data: 数据矩阵，每行是一个样本，每列是一个因变量
            group_labels: 分组标签

        Returns:
            dict: 包含 MANOVA 结果的字典
        """
        # 验证数据长度
        if len(data) != len(group_labels):
            raise ValueError("数据和分组标签长度不一致")

        # 过滤数据
        valid_rows = []
        valid_groups = []

        for i, (row, label) in enumerate(zip(data, group_labels)):
            is_valid = True
            for x in row:
                if x is None or (isinstance(x, (int, float)) and np.isnan(x)):
                    is_valid = False
                    break
            if is_valid:
                valid_rows.append(row)
                valid_groups.append(label)

        if len(valid_rows) < 3:
            return None

        data_array = np.array(valid_rows)
        groups = np.array(valid_groups)

        # 获取唯一组
        unique_groups = np.unique(groups)
        k = len(unique_groups)

        if k < 2:
            return None

        n, p = data_array.shape

        # 计算总均值
        grand_mean = np.mean(data_array, axis=0)

        # 计算组内协方差和组间协方差
        # 先收集各组数据
        group_data = []
        group_sizes = []

        for g in unique_groups:
            group_rows = data_array[groups == g]
            group_data.append(group_rows)
            group_sizes.append(len(group_rows))

        # 计算组内平方和和叉积矩阵 (W)
        w_matrix = np.zeros((p, p))
        for i in range(k):
            g_data = group_data[i]
            g_mean = np.mean(g_data, axis=0)
            n_g = group_sizes[i]
            for row in g_data:
                diff = row - g_mean
                w_matrix += np.outer(diff, diff)

        # 计算组间平方和和叉积矩阵 (B)
        b_matrix = np.zeros((p, p))
        for i in range(k):
            n_g = group_sizes[i]
            g_mean = np.mean(group_data[i], axis=0)
            diff = g_mean - grand_mean
            b_matrix += n_g * np.outer(diff, diff)

        # 计算各种检验统计量
        try:
            from scipy import linalg

            # 计算 Wilks' Lambda
            w_det = np.linalg.det(w_matrix)
            t_matrix = w_matrix + b_matrix
            t_det = np.linalg.det(t_matrix)
            lambda_wilks = w_det / t_det if t_det != 0 else None

            # 计算 Pillai's Trace
            try:
                w_inv = np.linalg.inv(w_matrix)
                w_inv_b = np.dot(w_inv, b_matrix)
                pillai_trace = np.trace(np.dot(w_inv_b, np.linalg.inv(np.eye(p) + w_inv_b)))
            except:
                pillai_trace = None

            # 计算 Hotelling-Lawley Trace
            try:
                if w_inv_b is not None:
                    hotelling_trace = np.trace(w_inv_b)
                else:
                    hotelling_trace = None
            except:
                hotelling_trace = None

            # 计算 Roy's Greatest Root
            try:
                if w_inv_b is not None:
                    eigenvalues = np.linalg.eigvals(w_inv_b)
                    roy_root = np.max(np.real(eigenvalues))
                else:
                    roy_root = None
            except:
                roy_root = None

            # 计算自由度
            df1 = p * (k - 1)
            df2 = p * (n - k)

            # 计算近似 F 值和 p 值（使用 Wilks' Lambda）
            f_value = None
            p_value = None

            if lambda_wilks is not None and df2 > 0:
                # Bartlett 近似
                r = df2 - (p - df1 + 1) / 2
                f_value = (1 - np.power(lambda_wilks, 1 / r)) / (np.power(lambda_wilks, 1 / r)) * (r * df2 - p * df1 / 2 + 1) / (p * df1)
                try:
                    from scipy import stats
                    p_value = 1 - stats.f.cdf(f_value, p * df1, r * df2 - p * df1 / 2 + 1)
                except:
                    p_value = None

            return {
                'w_matrix': w_matrix,
                'b_matrix': b_matrix,
                'lambda_wilks': lambda_wilks,
                'pillai_trace': pillai_trace,
                'hotelling_trace': hotelling_trace,
                'roy_root': roy_root,
                'f_value': f_value,
                'df1': df1,
                'df2': df2,
                'p_value': p_value,
                'group_count': k,
                'total_count': n
            }

        except ImportError:
            # 如果没有 scipy，返回基本的矩阵信息
            return {
                'w_matrix': w_matrix,
                'b_matrix': b_matrix,
                'group_count': k,
                'total_count': n
            }
