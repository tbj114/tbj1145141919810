#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meta 分析
"""

import numpy as np


class MetaAnalysis:
    """Meta 分析类"""

    @staticmethod
    def _filter_data(effect_sizes, standard_errors):
        """过滤无效数据"""
        if not isinstance(effect_sizes, np.ndarray):
            effect_sizes = np.array(effect_sizes)
        if not isinstance(standard_errors, np.ndarray):
            standard_errors = np.array(standard_errors)
        
        if effect_sizes.ndim != 1 or standard_errors.ndim != 1:
            raise ValueError("效应量和标准误必须是一维数组")
        if len(effect_sizes) != len(standard_errors):
            raise ValueError("效应量和标准误长度必须一致")
        
        # 过滤含有 NaN 的数据
        mask = ~np.isnan(effect_sizes) & ~np.isnan(standard_errors) & (standard_errors > 0)
        effect_sizes_filtered = effect_sizes[mask]
        standard_errors_filtered = standard_errors[mask]
        
        return effect_sizes_filtered, standard_errors_filtered

    @staticmethod
    def fixed_effect_model(effect_sizes, standard_errors):
        """
        固定效应模型 Meta 分析

        Args:
            effect_sizes: 各研究的效应量
            standard_errors: 各研究的标准误

        Returns:
            dict: 包含 Meta 分析结果的字典
        """
        # 过滤数据
        effect_sizes, standard_errors = MetaAnalysis._filter_data(effect_sizes, standard_errors)
        n_studies = len(effect_sizes)
        
        if n_studies == 0:
            raise ValueError("没有有效的数据")
        
        # 计算权重
        weights = 1 / (standard_errors ** 2)
        total_weight = np.sum(weights)
        
        # 计算合并效应量
        pooled_effect = np.sum(effect_sizes * weights) / total_weight
        
        # 计算合并效应量的标准误
        pooled_se = 1 / np.sqrt(total_weight)
        
        # 计算 95% 置信区间
        ci_lower = pooled_effect - 1.96 * pooled_se
        ci_upper = pooled_effect + 1.96 * pooled_se
        
        # 计算 Z 统计量和 p 值
        z_stat = pooled_effect / pooled_se
        p_value = MetaAnalysis._calculate_z_p_value(z_stat)
        
        # 计算异质性指标（Q 统计量）
        q_stat = np.sum(weights * (effect_sizes - pooled_effect) ** 2)
        df_q = n_studies - 1
        p_value_q = MetaAnalysis._calculate_chi_square_p_value(q_stat, df_q)
        
        return {
            'model': 'fixed_effect',
            'n_studies': n_studies,
            'pooled_effect': pooled_effect,
            'pooled_se': pooled_se,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'z_stat': z_stat,
            'p_value': p_value,
            'q_stat': q_stat,
            'df_q': df_q,
            'p_value_q': p_value_q,
            'weights': weights,
            'total_weight': total_weight
        }

    @staticmethod
    def random_effect_model(effect_sizes, standard_errors):
        """
        随机效应模型 Meta 分析

        Args:
            effect_sizes: 各研究的效应量
            standard_errors: 各研究的标准误

        Returns:
            dict: 包含 Meta 分析结果的字典
        """
        # 过滤数据
        effect_sizes, standard_errors = MetaAnalysis._filter_data(effect_sizes, standard_errors)
        n_studies = len(effect_sizes)
        
        if n_studies == 0:
            raise ValueError("没有有效的数据")
        
        # 首先计算固定效应模型的结果
        fixed_result = MetaAnalysis.fixed_effect_model(effect_sizes, standard_errors)
        
        # 计算异质性方差 τ²
        q_stat = fixed_result['q_stat']
        df_q = fixed_result['df_q']
        
        if q_stat > df_q:
            tau_squared = (q_stat - df_q) / (fixed_result['total_weight'] - np.sum(fixed_result['weights'] ** 2) / fixed_result['total_weight'])
            if tau_squared < 0:
                tau_squared = 0
        else:
            tau_squared = 0
        
        # 计算随机效应模型的权重
        random_weights = 1 / (standard_errors ** 2 + tau_squared)
        total_random_weight = np.sum(random_weights)
        
        # 计算合并效应量
        pooled_effect = np.sum(effect_sizes * random_weights) / total_random_weight
        
        # 计算合并效应量的标准误
        pooled_se = 1 / np.sqrt(total_random_weight)
        
        # 计算 95% 置信区间
        ci_lower = pooled_effect - 1.96 * pooled_se
        ci_upper = pooled_effect + 1.96 * pooled_se
        
        # 计算 Z 统计量和 p 值
        z_stat = pooled_effect / pooled_se
        p_value = MetaAnalysis._calculate_z_p_value(z_stat)
        
        # 计算 I² 和 H² 异质性指标
        if q_stat > 0:
            i_squared = max(0, (q_stat - df_q) / q_stat * 100)
            h_squared = q_stat / df_q
        else:
            i_squared = 0
            h_squared = 1
        
        return {
            'model': 'random_effect',
            'n_studies': n_studies,
            'pooled_effect': pooled_effect,
            'pooled_se': pooled_se,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'z_stat': z_stat,
            'p_value': p_value,
            'tau_squared': tau_squared,
            'i_squared': i_squared,
            'h_squared': h_squared,
            'q_stat': q_stat,
            'df_q': df_q,
            'p_value_q': fixed_result['p_value_q'],
            'weights': random_weights,
            'total_weight': total_random_weight
        }

    @staticmethod
    def _calculate_z_p_value(z_stat):
        """计算 Z 统计量的 p 值"""
        try:
            from scipy import stats
            p_value = 2 * (1 - stats.norm.cdf(np.abs(z_stat)))
            return p_value
        except ImportError:
            return None

    @staticmethod
    def _calculate_chi_square_p_value(chi_square, df):
        """计算卡方分布的 p 值"""
        try:
            from scipy import stats
            p_value = 1 - stats.chi2.cdf(chi_square, df)
            return p_value
        except ImportError:
            return None
