#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多层模型
"""

import numpy as np


class MultilevelModel:
    """多层模型类"""

    @staticmethod
    def hierarchical_linear_model(X, y, groups):
        """
        分层线性模型 (Hierarchical Linear Model, HLM)

        Args:
            X: 特征矩阵
            y: 目标向量
            groups: 分组变量

        Returns:
            dict: 包含模型结果的字典
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)
        if not isinstance(groups, np.ndarray):
            groups = np.array(groups)

        # 确保输入维度一致
        if len(X) != len(y) or len(X) != len(groups):
            raise ValueError("输入数据长度必须一致")

        # 获取唯一组
        unique_groups = np.unique(groups)
        n_groups = len(unique_groups)
        n_features = X.shape[1]

        # 第一层：每个组的回归
        group_models = {}
        group_coefs = []

        for group in unique_groups:
            # 提取组数据
            mask = groups == group
            X_group = X[mask]
            y_group = y[mask]

            if len(X_group) > 0:
                # 简单线性回归
                model = MultilevelModel._simple_linear_regression(X_group, y_group)
                group_models[group] = model
                group_coefs.append(model['coef'])

        # 第二层：组间回归
        if n_groups > 1:
            group_coefs = np.array(group_coefs)
            # 计算组间均值
            mean_coefs = np.mean(group_coefs, axis=0)
            # 计算组间方差
            var_coefs = np.var(group_coefs, axis=0)
        else:
            mean_coefs = None
            var_coefs = None

        return {
            'model': 'hierarchical_linear_model',
            'n_groups': n_groups,
            'unique_groups': unique_groups.tolist(),
            'group_models': group_models,
            'mean_coefs': mean_coefs.tolist() if mean_coefs is not None else None,
            'var_coefs': var_coefs.tolist() if var_coefs is not None else None,
            'n_features': n_features
        }

    @staticmethod
    def _simple_linear_regression(X, y):
        """简单线性回归"""
        # 添加截距项
        X_with_intercept = np.hstack([np.ones((X.shape[0], 1)), X])

        try:
            # 最小二乘法
            coefficients = np.linalg.inv(X_with_intercept.T.dot(X_with_intercept)).dot(X_with_intercept.T).dot(y)
        except np.linalg.LinAlgError:
            # 使用伪逆
            coefficients = np.linalg.pinv(X_with_intercept).dot(y)

        # 计算预测值
        y_pred = X_with_intercept.dot(coefficients)
        # 计算残差
        residuals = y - y_pred
        # 计算 R²
        ss_total = np.sum((y - np.mean(y)) ** 2)
        ss_residual = np.sum(residuals ** 2)
        r_squared = 1 - (ss_residual / ss_total) if ss_total > 0 else 0

        return {
            'intercept': coefficients[0],
            'coef': coefficients[1:],
            'r_squared': r_squared,
            'residuals': residuals.tolist()
        }

    @staticmethod
    def random_effects_model(X, y, groups):
        """
        随机效应模型

        Args:
            X: 特征矩阵
            y: 目标向量
            groups: 分组变量

        Returns:
            dict: 包含模型结果的字典
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)
        if not isinstance(groups, np.ndarray):
            groups = np.array(groups)

        # 确保输入维度一致
        if len(X) != len(y) or len(X) != len(groups):
            raise ValueError("输入数据长度必须一致")

        # 获取唯一组
        unique_groups = np.unique(groups)
        n_groups = len(unique_groups)

        # 计算组均值
        group_means = {}
        for group in unique_groups:
            mask = groups == group
            group_means[group] = np.mean(y[mask])

        # 计算总均值
        overall_mean = np.mean(y)

        # 计算组间方差和组内方差
        between_group_variance = 0
        within_group_variance = 0
        total_n = len(y)

        for group in unique_groups:
            mask = groups == group
            group_data = y[mask]
            n_group = len(group_data)
            between_group_variance += n_group * (group_means[group] - overall_mean) ** 2
            within_group_variance += np.sum((group_data - group_means[group]) ** 2)

        between_group_variance /= (n_groups - 1)
        within_group_variance /= (total_n - n_groups)

        # 计算 intraclass correlation (ICC)
        if (between_group_variance + within_group_variance) > 0:
            icc = between_group_variance / (between_group_variance + within_group_variance)
        else:
            icc = 0

        return {
            'model': 'random_effects_model',
            'n_groups': n_groups,
            'unique_groups': unique_groups.tolist(),
            'overall_mean': overall_mean,
            'group_means': group_means,
            'between_group_variance': between_group_variance,
            'within_group_variance': within_group_variance,
            'icc': icc
        }
