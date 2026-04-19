#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
描述性统计功能实现
"""

import math
import numpy as np


class DescriptiveStats:
    """描述性统计类"""
    
    @staticmethod
    def calculate_mean(data):
        """计算均值"""
        if not data:
            return None
        return np.mean(data)
    
    @staticmethod
    def calculate_std_dev(data):
        """计算标准差"""
        if not data:
            return None
        return np.std(data, ddof=1)
    
    @staticmethod
    def calculate_variance(data):
        """计算方差"""
        if not data:
            return None
        return np.var(data, ddof=1)
    
    @staticmethod
    def calculate_range(data):
        """计算全距（极差）"""
        if not data:
            return None
        return np.max(data) - np.min(data)
    
    @staticmethod
    def calculate_min(data):
        """计算最小值"""
        if not data:
            return None
        return np.min(data)
    
    @staticmethod
    def calculate_max(data):
        """计算最大值"""
        if not data:
            return None
        return np.max(data)
    
    @staticmethod
    def calculate_kurtosis(data):
        """计算峰度"""
        if not data:
            return None
        n = len(data)
        if n < 4:
            return None
        
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        
        if std == 0:
            return None
        
        # 计算峰度
        kurtosis = sum(((x - mean) / std) ** 4 for x in data) * (n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))
        kurtosis -= 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))
        return kurtosis
    
    @staticmethod
    def calculate_skewness(data):
        """计算偏度"""
        if not data:
            return None
        n = len(data)
        if n < 3:
            return None
        
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        
        if std == 0:
            return None
        
        # 计算偏度
        skewness = sum(((x - mean) / std) ** 3 for x in data) * n / ((n - 1) * (n - 2))
        return skewness
    
    @staticmethod
    def calculate_standard_error(data):
        """计算标准误"""
        if not data:
            return None
        n = len(data)
        if n == 0:
            return None
        std = np.std(data, ddof=1)
        return std / math.sqrt(n)
    
    @staticmethod
    def calculate_statistics(data, statistics_options=None):
        """
        计算指定的统计量
        
        Args:
            data: 数据列表
            statistics_options: 统计量选项字典
            
        Returns:
            dict: 计算结果
        """
        if not statistics_options:
            statistics_options = {
                'mean': True,
                'std_dev': True,
                'variance': True,
                'range': True,
                'min': True,
                'max': True,
                'kurtosis': True,
                'skewness': True,
                'standard_error': True
            }
        
        results = {}
        
        if statistics_options.get('mean'):
            results['mean'] = DescriptiveStats.calculate_mean(data)
        
        if statistics_options.get('std_dev'):
            results['std_dev'] = DescriptiveStats.calculate_std_dev(data)
        
        if statistics_options.get('variance'):
            results['variance'] = DescriptiveStats.calculate_variance(data)
        
        if statistics_options.get('range'):
            results['range'] = DescriptiveStats.calculate_range(data)
        
        if statistics_options.get('min'):
            results['min'] = DescriptiveStats.calculate_min(data)
        
        if statistics_options.get('max'):
            results['max'] = DescriptiveStats.calculate_max(data)
        
        if statistics_options.get('kurtosis'):
            results['kurtosis'] = DescriptiveStats.calculate_kurtosis(data)
        
        if statistics_options.get('skewness'):
            results['skewness'] = DescriptiveStats.calculate_skewness(data)
        
        if statistics_options.get('standard_error'):
            results['standard_error'] = DescriptiveStats.calculate_standard_error(data)
        
        # 添加基本信息
        results['count'] = len(data)
        results['valid_count'] = len([x for x in data if x is not None and not np.isnan(x)])
        
        return results
    
    @staticmethod
    def create_result_table(variable_name, statistics):
        """
        创建结果表格数据
        
        Args:
            variable_name: 变量名
            statistics: 统计量字典
            
        Returns:
            dict: 结果表格数据
        """
        table = {
            'variable': variable_name,
            'statistics': statistics
        }
        return table


class HistogramGenerator:
    """直方图生成器"""
    
    @staticmethod
    def generate_histogram_data(data, bins=10):
        """
        生成直方图数据
        
        Args:
            data: 数据列表
            bins: 区间数量
            
        Returns:
            tuple: (bin_edges, frequencies)
        """
        data = [x for x in data if x is not None and not np.isnan(x)]
        if not data:
            return None, None
        
        # 计算直方图
        hist, bin_edges = np.histogram(data, bins=bins)
        return bin_edges, hist
    
    @staticmethod
    def create_histogram_table(variable_name, bin_edges, frequencies):
        """
        创建直方图表格数据
        
        Args:
            variable_name: 变量名
            bin_edges: 区间边界
            frequencies: 频率
            
        Returns:
            list: 直方图表格数据
        """
        if bin_edges is None or frequencies is None:
            return []
        
        histogram_data = []
        for i in range(len(frequencies)):
            histogram_data.append({
                'bin_start': bin_edges[i],
                'bin_end': bin_edges[i + 1],
                'frequency': int(frequencies[i])
            })
        
        return histogram_data
