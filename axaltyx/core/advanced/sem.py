#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结构方程模型 (Structural Equation Modeling, SEM)
"""

import numpy as np


class SEM:
    """结构方程模型类"""

    @staticmethod
    def _filter_data(data):
        """过滤无效数据"""
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        
        if data.ndim != 2:
            raise ValueError("数据必须是二维数组")
        
        # 过滤含有 NaN 的行
        mask = ~np.isnan(data).any(axis=1)
        filtered_data = data[mask]
        
        return filtered_data

    @staticmethod
    def fit(data, model_spec):
        """
        拟合结构方程模型

        Args:
            data: 输入数据矩阵，形状为 (n_samples, n_variables)
            model_spec: 模型规格，包含潜变量和测量模型的定义

        Returns:
            dict: 包含模型拟合结果的字典
        """
        # 过滤数据
        X = SEM._filter_data(data)
        n_samples, n_variables = X.shape
        
        # 计算相关矩阵
        correlation_matrix = np.corrcoef(X, rowvar=False)
        
        # 提取模型规格
        latent_variables = model_spec.get('latent_variables', {})
        measurement_model = model_spec.get('measurement_model', {})
        structural_model = model_spec.get('structural_model', {})
        
        # 检查模型规格
        SEM._validate_model_spec(latent_variables, measurement_model, structural_model, n_variables)
        
        # 计算基本统计量
        descriptive_stats = SEM._calculate_descriptive_statistics(X)
        
        # 计算模型拟合指标
        # 这里实现的是一个简化版本，实际的 SEM 需要更复杂的算法
        fit_indices = SEM._calculate_fit_indices(correlation_matrix, model_spec, n_samples)
        
        return {
            'n_samples': n_samples,
            'n_variables': n_variables,
            'correlation_matrix': correlation_matrix,
            'descriptive_statistics': descriptive_stats,
            'fit_indices': fit_indices,
            'model_spec': model_spec
        }

    @staticmethod
    def _validate_model_spec(latent_variables, measurement_model, structural_model, n_variables):
        """验证模型规格"""
        # 检查测量模型
        for latent_var, indicators in measurement_model.items():
            if latent_var not in latent_variables:
                raise ValueError(f"潜变量 {latent_var} 在 measurement_model 中但不在 latent_variables 中")
            for indicator in indicators:
                if indicator >= n_variables:
                    raise ValueError(f"指标 {indicator} 超出变量范围")
        
        # 检查结构模型
        for endogenous, exogenous in structural_model.items():
            if endogenous not in latent_variables:
                raise ValueError(f"内生变量 {endogenous} 在 structural_model 中但不在 latent_variables 中")
            for var in exogenous:
                if var not in latent_variables:
                    raise ValueError(f"外生变量 {var} 在 structural_model 中但不在 latent_variables 中")

    @staticmethod
    def _calculate_descriptive_statistics(data):
        """计算描述性统计量"""
        n_samples, n_variables = data.shape
        
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0, ddof=1)
        var = np.var(data, axis=0, ddof=1)
        
        return {
            'mean': mean,
            'std': std,
            'var': var,
            'n_samples': n_samples,
            'n_variables': n_variables
        }

    @staticmethod
    def _calculate_fit_indices(correlation_matrix, model_spec, n_samples):
        """计算模型拟合指标"""
        # 这里实现的是简化版本
        # 实际的 SEM 拟合需要使用最大似然估计等方法
        
        # 计算自由度
        n_variables = correlation_matrix.shape[0]
        measurement_model = model_spec.get('measurement_model', {})
        structural_model = model_spec.get('structural_model', {})
        
        # 计算自由参数数量
        free_params = 0
        
        # 测量模型参数
        for latent_var, indicators in measurement_model.items():
            # 每个指标有一个因子载荷（固定第一个为1）
            free_params += len(indicators) - 1
            # 每个指标有一个误差方差
            free_params += len(indicators)
        
        # 结构模型参数
        for endogenous, exogenous in structural_model.items():
            # 每个外生变量对内生变量的路径系数
            free_params += len(exogenous)
            # 每个内生变量的残差方差
            free_params += 1
        
        # 潜变量之间的协方差
        latent_variables = list(model_spec.get('latent_variables', {}).keys())
        n_latent = len(latent_variables)
        free_params += n_latent * (n_latent - 1) // 2
        
        # 计算自由度
        df = n_variables * (n_variables + 1) // 2 - free_params
        
        # 计算卡方值（简化版）
        chi_square = 0  # 实际需要通过拟合计算
        
        # 计算拟合指标
        if df > 0:
            p_value = SEM._calculate_chi_square_p_value(chi_square, df)
        else:
            p_value = None
        
        return {
            'chi_square': chi_square,
            'df': df,
            'p_value': p_value,
            'free_params': free_params,
            'n_variables': n_variables
        }

    @staticmethod
    def _calculate_chi_square_p_value(chi_square, df):
        """计算卡方分布的 p 值"""
        try:
            from scipy import stats
            p_value = 1 - stats.chi2.cdf(chi_square, df)
            return p_value
        except ImportError:
            return None
