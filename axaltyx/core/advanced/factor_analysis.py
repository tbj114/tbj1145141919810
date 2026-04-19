#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因子分析 (Factor Analysis)
"""

import numpy as np


class FactorAnalysis:
    """因子分析类"""

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
    def fit(data, n_factors=3, method='principal_axis', max_iter=100, tol=1e-6):
        """
        执行因子分析

        Args:
            data: 输入数据矩阵，形状为 (n_samples, n_features)
            n_factors: 要提取的因子数量
            method: 提取方法，'principal_axis'（主轴法，默认）或 'ml'（最大似然法）
            max_iter: 最大迭代次数
            tol: 收敛阈值

        Returns:
            dict: 包含分析结果的字典
        """
        # 过滤数据
        X = FactorAnalysis._filter_data(data)
        n_samples, n_features = X.shape
        
        if n_factors >= n_features:
            n_factors = n_features - 1
        
        # 数据标准化
        mean = np.mean(X, axis=0)
        X_centered = X - mean
        
        # 计算相关矩阵
        correlation_matrix = np.corrcoef(X_centered, rowvar=False)
        
        if method == 'principal_axis':
            # 主轴因子法
            return FactorAnalysis._principal_axis_method(
                correlation_matrix, n_factors, max_iter, tol
            )
        elif method == 'ml':
            # 最大似然法（简化实现）
            return FactorAnalysis._maximum_likelihood_method(
                X_centered, n_factors, max_iter, tol
            )
        else:
            raise ValueError("方法必须是 'principal_axis' 或 'ml'")

    @staticmethod
    def _principal_axis_method(correlation_matrix, n_factors, max_iter, tol):
        """主轴因子法"""
        n_features = correlation_matrix.shape[0]
        
        # 初始 communalities（使用变量的方差，即相关矩阵的对角线）
        communalities = np.diag(correlation_matrix)
        
        for i in range(max_iter):
            # 创建约相关矩阵
            reduced_correlation = correlation_matrix - np.diag(1 - communalities)
            
            # 计算特征值和特征向量
            eigenvalues, eigenvectors = np.linalg.eigh(reduced_correlation)
            
            # 按特征值降序排序
            sorted_indices = np.argsort(eigenvalues)[::-1]
            eigenvalues = eigenvalues[sorted_indices]
            eigenvectors = eigenvectors[:, sorted_indices]
            
            # 选择前 n_factors 个因子
            eigenvalues = eigenvalues[:n_factors]
            eigenvectors = eigenvectors[:, :n_factors]
            
            # 计算因子载荷
            loadings = eigenvectors * np.sqrt(eigenvalues)
            
            # 更新 communalities
            new_communalities = np.sum(loadings ** 2, axis=1)
            
            # 检查收敛
            if np.max(np.abs(new_communalities - communalities)) < tol:
                break
            
            communalities = new_communalities
        
        # 计算因子得分（使用回归方法）
        inverse_correlation = np.linalg.inv(correlation_matrix)
        factor_score_coefficients = np.dot(inverse_correlation, loadings)
        
        return {
            'method': 'principal_axis',
            'n_factors': n_factors,
            'loadings': loadings,
            'communalities': communalities,
            'eigenvalues': eigenvalues,
            'factor_score_coefficients': factor_score_coefficients
        }

    @staticmethod
    def _maximum_likelihood_method(X, n_factors, max_iter, tol):
        """最大似然法（简化实现）"""
        n_samples, n_features = X.shape
        
        # 初始因子载荷
        pca_result = __import__('axaltyx.core.advanced.pca').core.advanced.pca.PCA.fit(X, n_factors)
        loadings = pca_result['eigenvectors'] * np.sqrt(pca_result['eigenvalues'])
        
        # 初始特殊因子方差
        communalities = np.sum(loadings ** 2, axis=1)
        uniqueness = 1 - communalities
        
        for i in range(max_iter):
            # 计算因子协方差矩阵
            psi = np.diag(uniqueness)
            
            # 计算矩阵乘积
            L_psi_inv = np.dot(loadings, np.linalg.inv(psi))
            I_plus_L_psi_inv_Lt = np.eye(n_factors) + np.dot(L_psi_inv, loadings.T)
            
            # 计算权重矩阵
            weights = np.dot(L_psi_inv.T, np.linalg.inv(I_plus_L_psi_inv_Lt))
            
            # 更新因子载荷
            new_loadings = np.dot(np.cov(X, rowvar=False), weights)
            
            # 更新唯一性
            new_communalities = np.sum(new_loadings ** 2, axis=1)
            new_uniqueness = 1 - new_communalities
            
            # 检查收敛
            if np.max(np.abs(new_uniqueness - uniqueness)) < tol:
                break
            
            loadings = new_loadings
            uniqueness = new_uniqueness
        
        return {
            'method': 'maximum_likelihood',
            'n_factors': n_factors,
            'loadings': loadings,
            'uniqueness': uniqueness,
            'communalities': 1 - uniqueness
        }
