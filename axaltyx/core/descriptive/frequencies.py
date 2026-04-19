#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
频数分析功能实现
"""

import numpy as np
from collections import Counter


class Frequencies:
    """频数分析类"""
    
    @staticmethod
    def calculate_frequencies(data):
        """
        计算频数分布
        
        Args:
            data: 数据列表
            
        Returns:
            dict: 频数分布结果
        """
        # 过滤掉 None 值
        valid_data = []
        for x in data:
            if x is not None:
                # 对于数值类型，还要检查是否为 NaN
                if isinstance(x, (int, float)):
                    if not np.isnan(x):
                        valid_data.append(x)
                else:
                    # 对于非数值类型，只需要检查是否为 None
                    valid_data.append(x)
        
        if not valid_data:
            return {
                'count': 0,
                'valid_count': 0,
                'missing_count': len(data),
                'frequencies': []
            }
        
        # 计算频数
        counter = Counter(valid_data)
        
        # 计算总频数和缺失值
        total_count = len(data)
        valid_count = len(valid_data)
        missing_count = total_count - valid_count
        
        # 计算频率和累积频率
        frequencies = []
        cumulative_frequency = 0
        
        # 按值排序
        for value, frequency in sorted(counter.items()):
            percentage = (frequency / valid_count) * 100
            cumulative_frequency += frequency
            cumulative_percentage = (cumulative_frequency / valid_count) * 100
            
            frequencies.append({
                'value': value,
                'frequency': frequency,
                'percentage': percentage,
                'cumulative_frequency': cumulative_frequency,
                'cumulative_percentage': cumulative_percentage
            })
        
        return {
            'count': total_count,
            'valid_count': valid_count,
            'missing_count': missing_count,
            'frequencies': frequencies
        }
    
    @staticmethod
    def create_frequency_table(variable_name, frequency_result):
        """
        创建频数分布表格
        
        Args:
            variable_name: 变量名
            frequency_result: 频数分析结果
            
        Returns:
            dict: 表格数据
        """
        table = {
            'variable': variable_name,
            'count': frequency_result['count'],
            'valid_count': frequency_result['valid_count'],
            'missing_count': frequency_result['missing_count'],
            'frequencies': frequency_result['frequencies']
        }
        return table
    
    @staticmethod
    def calculate_percentiles(data, percentiles=None):
        """
        计算百分位数
        
        Args:
            data: 数据列表
            percentiles: 要计算的百分位数列表，默认为 [25, 50, 75]
            
        Returns:
            dict: 百分位数结果
        """
        if percentiles is None:
            percentiles = [25, 50, 75]
        
        # 过滤掉 None 值
        valid_data = []
        for x in data:
            if x is not None:
                # 对于数值类型，还要检查是否为 NaN
                if isinstance(x, (int, float)):
                    if not np.isnan(x):
                        valid_data.append(x)
                else:
                    # 对于非数值类型，只需要检查是否为 None
                    valid_data.append(x)
        
        if not valid_data:
            return {
                'count': 0,
                'valid_count': 0,
                'percentiles': {}
            }
        
        # 计算百分位数
        percentile_values = {}
        for p in percentiles:
            percentile_values[p] = np.percentile(valid_data, p)
        
        return {
            'count': len(data),
            'valid_count': len(valid_data),
            'percentiles': percentile_values
        }
    
    @staticmethod
    def create_percentile_table(variable_name, percentile_result):
        """
        创建百分位数表格
        
        Args:
            variable_name: 变量名
            percentile_result: 百分位数分析结果
            
        Returns:
            dict: 表格数据
        """
        table = {
            'variable': variable_name,
            'count': percentile_result['count'],
            'valid_count': percentile_result['valid_count'],
            'percentiles': percentile_result['percentiles']
        }
        return table