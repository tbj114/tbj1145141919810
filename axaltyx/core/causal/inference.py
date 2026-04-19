#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因果推断
"""

import numpy as np


class CausalInference:
    """因果推断类"""

    @staticmethod
    def _filter_data(X, y, treatment):
        """过滤无效数据"""
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)
        if not isinstance(treatment, np.ndarray):
            treatment = np.array(treatment)
        
        if X.ndim != 2:
            raise ValueError("特征数据必须是二维数组")
        if y.ndim != 1 or treatment.ndim != 1:
            raise ValueError("结果和处理变量必须是一维数组")
        if len(X) != len(y) or len(X) != len(treatment):
            raise ValueError("数据长度必须一致")
        
        # 过滤含有 NaN 的行
        mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y) & ~np.isnan(treatment)
        X_filtered = X[mask]
        y_filtered = y[mask]
        treatment_filtered = treatment[mask]
        
        return X_filtered, y_filtered, treatment_filtered

    @staticmethod
    def propensity_score_matching(X, y, treatment, method='nearest_neighbor', caliper=0.2):
        """
        倾向得分匹配

        Args:
            X: 特征矩阵
            y: 结果变量
            treatment: 处理变量（1 表示处理组，0 表示对照组）
            method: 匹配方法，'nearest_neighbor'（最近邻匹配）
            caliper: 卡尺大小（标准化倾向得分的最大差异）

        Returns:
            dict: 包含匹配结果的字典
        """
        # 过滤数据
        X, y, treatment = CausalInference._filter_data(X, y, treatment)
        
        # 分离处理组和对照组
        treated = treatment == 1
        control = treatment == 0
        
        if np.sum(treated) == 0 or np.sum(control) == 0:
            raise ValueError("处理组或对照组为空")
        
        # 计算倾向得分（使用逻辑回归）
        propensity_scores = CausalInference._estimate_propensity_score(X, treatment)
        
        # 执行匹配
        if method == 'nearest_neighbor':
            matched_pairs = CausalInference._nearest_neighbor_matching(
                propensity_scores, treated, control, caliper
            )
        else:
            raise ValueError("匹配方法必须是 'nearest_neighbor'")
        
        # 计算平均处理效应 (ATT)
        treated_outcomes = y[treated][[p[0] for p in matched_pairs]]
        control_outcomes = y[control][[p[1] for p in matched_pairs]]
        att = np.mean(treated_outcomes - control_outcomes)
        
        # 计算标准误
        se = np.std(treated_outcomes - control_outcomes, ddof=1) / np.sqrt(len(matched_pairs))
        
        # 计算 95% 置信区间
        ci_lower = att - 1.96 * se
        ci_upper = att + 1.96 * se
        
        # 计算 Z 统计量和 p 值
        z_stat = att / se
        p_value = CausalInference._calculate_z_p_value(z_stat)
        
        return {
            'method': 'propensity_score_matching',
            'matching_method': method,
            'n_treated': np.sum(treated),
            'n_control': np.sum(control),
            'n_matched_pairs': len(matched_pairs),
            'att': att,
            'se': se,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'z_stat': z_stat,
            'p_value': p_value,
            'propensity_scores': propensity_scores,
            'matched_pairs': matched_pairs
        }

    @staticmethod
    def difference_in_differences(y_pre, y_post, treatment):
        """
        双重差分法 (Difference-in-Differences, DID)

        Args:
            y_pre: 处理前的结果变量
            y_post: 处理后的结果变量
            treatment: 处理变量（1 表示处理组，0 表示对照组）

        Returns:
            dict: 包含 DID 结果的字典
        """
        if not isinstance(y_pre, np.ndarray):
            y_pre = np.array(y_pre)
        if not isinstance(y_post, np.ndarray):
            y_post = np.array(y_post)
        if not isinstance(treatment, np.ndarray):
            treatment = np.array(treatment)
        
        if y_pre.ndim != 1 or y_post.ndim != 1 or treatment.ndim != 1:
            raise ValueError("所有输入必须是一维数组")
        if len(y_pre) != len(y_post) or len(y_pre) != len(treatment):
            raise ValueError("数据长度必须一致")
        
        # 过滤含有 NaN 的数据
        mask = ~np.isnan(y_pre) & ~np.isnan(y_post) & ~np.isnan(treatment)
        y_pre = y_pre[mask]
        y_post = y_post[mask]
        treatment = treatment[mask]
        
        # 分离处理组和对照组
        treated = treatment == 1
        control = treatment == 0
        
        if np.sum(treated) == 0 or np.sum(control) == 0:
            raise ValueError("处理组或对照组为空")
        
        # 计算差分
        treated_diff = np.mean(y_post[treated] - y_pre[treated])
        control_diff = np.mean(y_post[control] - y_pre[control])
        did_estimate = treated_diff - control_diff
        
        # 计算标准误（简化版）
        treated_var = np.var(y_post[treated] - y_pre[treated], ddof=1) / np.sum(treated)
        control_var = np.var(y_post[control] - y_pre[control], ddof=1) / np.sum(control)
        se = np.sqrt(treated_var + control_var)
        
        # 计算 95% 置信区间
        ci_lower = did_estimate - 1.96 * se
        ci_upper = did_estimate + 1.96 * se
        
        # 计算 Z 统计量和 p 值
        z_stat = did_estimate / se
        p_value = CausalInference._calculate_z_p_value(z_stat)
        
        return {
            'method': 'difference_in_differences',
            'n_treated': np.sum(treated),
            'n_control': np.sum(control),
            'treated_pre_mean': np.mean(y_pre[treated]),
            'treated_post_mean': np.mean(y_post[treated]),
            'control_pre_mean': np.mean(y_pre[control]),
            'control_post_mean': np.mean(y_post[control]),
            'treated_diff': treated_diff,
            'control_diff': control_diff,
            'did_estimate': did_estimate,
            'se': se,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'z_stat': z_stat,
            'p_value': p_value
        }

    @staticmethod
    def _estimate_propensity_score(X, treatment):
        """估计倾向得分"""
        try:
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression()
            model.fit(X, treatment)
            return model.predict_proba(X)[:, 1]
        except ImportError:
            # 如果没有 sklearn，使用简化的逻辑回归
            return CausalInference._simple_logistic_regression(X, treatment)

    @staticmethod
    def _simple_logistic_regression(X, y):
        """简化的逻辑回归"""
        # 添加截距项
        X = np.hstack([np.ones((X.shape[0], 1)), X])
        
        # 使用梯度下降
        beta = np.zeros(X.shape[1])
        learning_rate = 0.01
        max_iter = 1000
        
        for _ in range(max_iter):
            z = np.dot(X, beta)
            p = 1 / (1 + np.exp(-z))
            gradient = np.dot(X.T, p - y)
            beta -= learning_rate * gradient
        
        z = np.dot(X, beta)
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def _nearest_neighbor_matching(propensity_scores, treated, control, caliper):
        """最近邻匹配"""
        treated_indices = np.where(treated)[0]
        control_indices = np.where(control)[0]
        
        treated_scores = propensity_scores[treated]
        control_scores = propensity_scores[control]
        
        matched_pairs = []
        for i, score in enumerate(treated_scores):
            # 计算与所有对照组的距离
            distances = np.abs(score - control_scores)
            
            # 应用卡尺
            valid_indices = np.where(distances <= caliper * np.std(propensity_scores))[0]
            
            if len(valid_indices) > 0:
                # 找到最近的对照组
                nearest_idx = valid_indices[np.argmin(distances[valid_indices])]
                matched_pairs.append((i, nearest_idx))
        
        return matched_pairs

    @staticmethod
    def _calculate_z_p_value(z_stat):
        """计算 Z 统计量的 p 值"""
        try:
            from scipy import stats
            p_value = 2 * (1 - stats.norm.cdf(np.abs(z_stat)))
            return p_value
        except ImportError:
            return None
