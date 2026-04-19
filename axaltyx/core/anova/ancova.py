#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协方差分析实现
"""

import numpy as np


class ANCOVA:
    """协方差分析类"""

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
        return filtered_data

    @staticmethod
    def calculate(y_data, covariate_data, group_labels):
        """
        执行协方差分析

        Args:
            y_data: 因变量数据
            covariate_data: 协变量数据（可以是多个协变量）
            group_labels: 分组标签

        Returns:
            dict: 包含 ANCOVA 结果的字典
        """
        # 验证数据长度
        n = len(y_data)
        if len(covariate_data) != n or len(group_labels) != n:
            raise ValueError("数据长度不一致")

        # 处理协变量，如果是一维数组，转换为二维数组
        if isinstance(covariate_data[0], (int, float)):
            covariate_data = [[x] for x in covariate_data]

        # 过滤数据
        valid_indices = []
        for i in range(n):
            is_valid = True
            # 检查因变量
            if y_data[i] is None or (isinstance(y_data[i], (int, float)) and np.isnan(y_data[i])):
                is_valid = False
            # 检查协变量
            if is_valid:
                for x in covariate_data[i]:
                    if x is None or (isinstance(x, (int, float)) and np.isnan(x)):
                        is_valid = False
                        break
            if is_valid:
                valid_indices.append(i)

        if len(valid_indices) < 3:
            return None

        # 提取有效数据
        y_valid = np.array([y_data[i] for i in valid_indices])
        covariate_valid = np.array([covariate_data[i] for i in valid_indices])
        groups_valid = np.array([group_labels[i] for i in valid_indices])

        # 获取唯一组
        unique_groups = np.unique(groups_valid)
        k = len(unique_groups)

        if k < 2:
            return None

        n_valid = len(y_valid)
        p_cov = covariate_valid.shape[1]  # 协变量数量

        # 构建设计矩阵 X
        # X 包含：截距、组指示变量（k-1个）、协变量（p个）
        X = np.zeros((n_valid, 1 + (k - 1) + p_cov))

        # 截距项
        X[:, 0] = 1

        # 组指示变量（使用参考编码）
        for i, idx in enumerate(valid_indices):
            group = groups_valid[i]
            # 找到组的索引
            group_idx = np.where(unique_groups == group)[0][0]
            if group_idx > 0:
                X[i, group_idx] = 1

        # 协变量
        X[:, 1 + (k - 1):] = covariate_valid

        # 构建只包含协变量和截距的设计矩阵（H0模型）
        X0 = np.zeros((n_valid, 1 + p_cov))
        X0[:, 0] = 1
        X0[:, 1:] = covariate_valid

        # 最小二乘回归
        try:
            # 完整模型
            beta_hat, residuals, rank, s = np.linalg.lstsq(X, y_valid, rcond=None)
            y_pred = np.dot(X, beta_hat)
            ss_total = np.sum((y_valid - np.mean(y_valid)) ** 2)
            ss_residual = np.sum(residuals ** 2)
            ss_model = ss_total - ss_residual

            # H0模型（没有组效应）
            beta_hat0, residuals0, rank0, s0 = np.linalg.lstsq(X0, y_valid, rcond=None)
            ss_residual0 = np.sum(residuals0 ** 2)

            # 计算组效应的平方和
            ss_group = ss_residual0 - ss_residual

            # 计算自由度
            df_total = n_valid - 1
            df_model = X.shape[1] - 1
            df_residual = n_valid - X.shape[1]
            df_cov = p_cov
            df_group = k - 1

            # 计算均方
            ms_group = ss_group / df_group if df_group > 0 else None
            ms_residual = ss_residual / df_residual if df_residual > 0 else None

            # 计算 F 值和 p 值
            f_value = None
            p_value = None

            if ms_group is not None and ms_residual is not None and ms_residual > 0:
                f_value = ms_group / ms_residual
                try:
                    from scipy import stats
                    p_value = 1 - stats.f.cdf(f_value, df_group, df_residual)
                except:
                    p_value = None

            # 计算协变量效应
            # 构建只包含组和截距的模型
            X1 = np.zeros((n_valid, 1 + (k - 1)))
            X1[:, 0] = 1
            for i in range(n_valid):
                group_idx = np.where(unique_groups == groups_valid[i])[0][0]
                if group_idx > 0:
                    X1[i, group_idx] = 1

            beta_hat1, residuals1, rank1, s1 = np.linalg.lstsq(X1, y_valid, rcond=None)
            ss_residual1 = np.sum(residuals1 ** 2)
            ss_covariate = ss_residual1 - ss_residual
            ms_covariate = ss_covariate / df_cov if df_cov > 0 else None

            return {
                'y_data': y_valid,
                'covariate_data': covariate_valid,
                'groups': groups_valid,
                'unique_groups': unique_groups,
                'group_count': k,
                'total_count': n_valid,
                'ss_total': ss_total,
                'ss_model': ss_model,
                'ss_group': ss_group,
                'ss_covariate': ss_covariate,
                'ss_residual': ss_residual,
                'df_total': df_total,
                'df_model': df_model,
                'df_group': df_group,
                'df_covariate': df_cov,
                'df_residual': df_residual,
                'ms_group': ms_group,
                'ms_covariate': ms_covariate,
                'ms_residual': ms_residual,
                'f_value': f_value,
                'p_value': p_value,
                'beta_hat': beta_hat
            }

        except ImportError:
            return None
