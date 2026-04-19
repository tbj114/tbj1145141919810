#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间序列分析
"""

import numpy as np


class TimeSeriesAnalysis:
    """时间序列分析类"""

    @staticmethod
    def _filter_data(data):
        """过滤无效数据"""
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        
        if data.ndim != 1:
            raise ValueError("时间序列数据必须是一维数组")
        
        # 过滤含有 NaN 的数据
        mask = ~np.isnan(data)
        filtered_data = data[mask]
        
        return filtered_data

    @staticmethod
    def descriptive_statistics(data):
        """
        计算时间序列的描述性统计量

        Args:
            data: 时间序列数据

        Returns:
            dict: 包含描述性统计量的字典
        """
        # 过滤数据
        data = TimeSeriesAnalysis._filter_data(data)
        n = len(data)
        
        if n == 0:
            raise ValueError("没有有效的数据")
        
        mean = np.mean(data)
        median = np.median(data)
        std = np.std(data, ddof=1)
        var = np.var(data, ddof=1)
        min_val = np.min(data)
        max_val = np.max(data)
        range_val = max_val - min_val
        
        # 计算偏度和峰度
        skewness = TimeSeriesAnalysis._calculate_skewness(data, mean, std)
        kurtosis = TimeSeriesAnalysis._calculate_kurtosis(data, mean, std)
        
        return {
            'n': n,
            'mean': mean,
            'median': median,
            'std': std,
            'var': var,
            'min': min_val,
            'max': max_val,
            'range': range_val,
            'skewness': skewness,
            'kurtosis': kurtosis
        }

    @staticmethod
    def _calculate_skewness(data, mean, std):
        """计算偏度"""
        n = len(data)
        if n < 3 or std == 0:
            return 0
        return np.sum((data - mean) ** 3) / (n * std ** 3)

    @staticmethod
    def _calculate_kurtosis(data, mean, std):
        """计算峰度"""
        n = len(data)
        if n < 4 or std == 0:
            return 0
        return np.sum((data - mean) ** 4) / (n * std ** 4) - 3

    @staticmethod
    def acf(data, nlags=20):
        """
        计算自相关函数 (ACF)

        Args:
            data: 时间序列数据
            nlags: 滞后阶数

        Returns:
            dict: 包含自相关系数的字典
        """
        # 过滤数据
        data = TimeSeriesAnalysis._filter_data(data)
        n = len(data)
        
        if n < 2:
            raise ValueError("至少需要 2 个数据点")
        
        # 标准化数据
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        if std == 0:
            return {'acf': [1.0] * (nlags + 1)}
        
        data_std = (data - mean) / std
        
        # 计算自相关系数
        acf_values = []
        for lag in range(nlags + 1):
            if lag == 0:
                acf_values.append(1.0)
            else:
                numerator = np.sum(data_std[:-lag] * data_std[lag:])
                denominator = n - 1
                acf_values.append(numerator / denominator)
        
        return {
            'acf': acf_values,
            'nlags': nlags
        }

    @staticmethod
    def pacf(data, nlags=20):
        """
        计算偏自相关函数 (PACF)

        Args:
            data: 时间序列数据
            nlags: 滞后阶数

        Returns:
            dict: 包含偏自相关系数的字典
        """
        # 过滤数据
        data = TimeSeriesAnalysis._filter_data(data)
        n = len(data)
        
        if n < 2:
            raise ValueError("至少需要 2 个数据点")
        
        # 计算 ACF
        acf_result = TimeSeriesAnalysis.acf(data, nlags=nlags)
        acf_values = acf_result['acf']
        
        # 使用 Yule-Walker 方程计算 PACF
        pacf_values = []
        for k in range(nlags + 1):
            if k == 0:
                pacf_values.append(1.0)
            else:
                # 构建 Yule-Walker 矩阵
                matrix = np.zeros((k, k))
                for i in range(k):
                    for j in range(k):
                        matrix[i, j] = acf_values[abs(i - j)]
                
                # 构建右侧向量
                vector = acf_values[1:k+1]
                
                # 求解线性方程组
                try:
                    coefficients = np.linalg.solve(matrix, vector)
                    pacf_values.append(coefficients[-1])
                except np.linalg.LinAlgError:
                    pacf_values.append(0.0)
        
        return {
            'pacf': pacf_values,
            'nlags': nlags
        }

    @staticmethod
    def simple_moving_average(data, window=3):
        """
        计算简单移动平均

        Args:
            data: 时间序列数据
            window: 窗口大小

        Returns:
            dict: 包含移动平均结果的字典
        """
        # 过滤数据
        data = TimeSeriesAnalysis._filter_data(data)
        n = len(data)
        
        if n < window:
            raise ValueError(f"数据长度必须至少为窗口大小 ({window})")
        
        # 计算移动平均
        sma = []
        for i in range(n - window + 1):
            sma.append(np.mean(data[i:i+window]))
        
        return {
            'sma': sma,
            'window': window,
            'n': len(sma)
        }

    @staticmethod
    def exponential_smoothing(data, alpha=0.2):
        """
        计算指数平滑

        Args:
            data: 时间序列数据
            alpha: 平滑参数 (0 < alpha < 1)

        Returns:
            dict: 包含指数平滑结果的字典
        """
        # 过滤数据
        data = TimeSeriesAnalysis._filter_data(data)
        n = len(data)
        
        if n == 0:
            raise ValueError("没有有效的数据")
        
        if alpha <= 0 or alpha >= 1:
            raise ValueError("平滑参数必须在 (0, 1) 之间")
        
        # 计算指数平滑
        es = [data[0]]  # 初始值
        for i in range(1, n):
            es_val = alpha * data[i] + (1 - alpha) * es[i-1]
            es.append(es_val)
        
        return {
            'es': es,
            'alpha': alpha,
            'n': n
        }
