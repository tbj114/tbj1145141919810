#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交叉表分析功能实现
"""

import numpy as np
from collections import defaultdict, Counter


class Crosstabs:
    """交叉表分析类"""
    
    @staticmethod
    def calculate_crosstab(row_data, column_data, row_name='Row', column_name='Column'):
        """
        计算交叉表
        
        Args:
            row_data: 行变量数据列表
            column_data: 列变量数据列表
            row_name: 行变量名称
            column_name: 列变量名称
            
        Returns:
            dict: 交叉表结果
        """
        # 检查数据长度是否一致
        if len(row_data) != len(column_data):
            raise ValueError("Row and column data must have the same length")
        
        # 过滤掉无效数据
        valid_pairs = []
        for r, c in zip(row_data, column_data):
            # 检查行数据
            r_valid = False
            if r is not None:
                if isinstance(r, (int, float)):
                    if not np.isnan(r):
                        r_valid = True
                else:
                    r_valid = True
            
            # 检查列数据
            c_valid = False
            if c is not None:
                if isinstance(c, (int, float)):
                    if not np.isnan(c):
                        c_valid = True
                else:
                    c_valid = True
            
            if r_valid and c_valid:
                valid_pairs.append((r, c))
        
        if not valid_pairs:
            return {
                'row_name': row_name,
                'column_name': column_name,
                'count': len(row_data),
                'valid_count': 0,
                'missing_count': len(row_data),
                'crosstab': {},
                'row_totals': {},
                'column_totals': {},
                'grand_total': 0
            }
        
        # 计算交叉表
        crosstab = defaultdict(dict)
        row_totals = Counter()
        column_totals = Counter()
        grand_total = 0
        
        # 统计频数
        for r, c in valid_pairs:
            if c not in crosstab[r]:
                crosstab[r][c] = 0
            crosstab[r][c] += 1
            row_totals[r] += 1
            column_totals[c] += 1
            grand_total += 1
        
        # 转换为普通字典
        crosstab_dict = {}
        for r, cols in crosstab.items():
            crosstab_dict[r] = dict(cols)
        
        return {
            'row_name': row_name,
            'column_name': column_name,
            'count': len(row_data),
            'valid_count': grand_total,
            'missing_count': len(row_data) - grand_total,
            'crosstab': crosstab_dict,
            'row_totals': dict(row_totals),
            'column_totals': dict(column_totals),
            'grand_total': grand_total
        }
    
    @staticmethod
    def calculate_percentages(crosstab_result, percentage_type='row'):
        """
        计算交叉表的百分比
        
        Args:
            crosstab_result: 交叉表结果
            percentage_type: 百分比类型，可选值：'row', 'column', 'total'
            
        Returns:
            dict: 带百分比的交叉表结果
        """
        crosstab = crosstab_result['crosstab']
        row_totals = crosstab_result['row_totals']
        column_totals = crosstab_result['column_totals']
        grand_total = crosstab_result['grand_total']
        
        percentages = {}
        
        for row, cols in crosstab.items():
            percentages[row] = {}
            for col, count in cols.items():
                if percentage_type == 'row':
                    if row_totals[row] > 0:
                        percentages[row][col] = (count / row_totals[row]) * 100
                    else:
                        percentages[row][col] = 0
                elif percentage_type == 'column':
                    if column_totals[col] > 0:
                        percentages[row][col] = (count / column_totals[col]) * 100
                    else:
                        percentages[row][col] = 0
                elif percentage_type == 'total':
                    if grand_total > 0:
                        percentages[row][col] = (count / grand_total) * 100
                    else:
                        percentages[row][col] = 0
        
        return percentages
    
    @staticmethod
    def create_crosstab_table(crosstab_result, include_percentages=True, percentage_type='row'):
        """
        创建交叉表表格
        
        Args:
            crosstab_result: 交叉表结果
            include_percentages: 是否包含百分比
            percentage_type: 百分比类型
            
        Returns:
            dict: 表格数据
        """
        table = {
            'row_name': crosstab_result['row_name'],
            'column_name': crosstab_result['column_name'],
            'count': crosstab_result['count'],
            'valid_count': crosstab_result['valid_count'],
            'missing_count': crosstab_result['missing_count'],
            'crosstab': crosstab_result['crosstab'],
            'row_totals': crosstab_result['row_totals'],
            'column_totals': crosstab_result['column_totals'],
            'grand_total': crosstab_result['grand_total']
        }
        
        if include_percentages:
            table['percentages'] = Crosstabs.calculate_percentages(crosstab_result, percentage_type)
        
        return table
    
    @staticmethod
    def calculate_chi_square(crosstab_result):
        """
        计算卡方检验
        
        Args:
            crosstab_result: 交叉表结果
            
        Returns:
            dict: 卡方检验结果
        """
        crosstab = crosstab_result['crosstab']
        row_totals = crosstab_result['row_totals']
        column_totals = crosstab_result['column_totals']
        grand_total = crosstab_result['grand_total']
        
        if grand_total == 0:
            return {
                'chi_square': None,
                'degrees_of_freedom': None,
                'p_value': None
            }
        
        # 计算期望频数
        expected = {}
        for row, cols in crosstab.items():
            expected[row] = {}
            for col in cols.keys():
                expected[row][col] = (row_totals[row] * column_totals[col]) / grand_total
        
        # 计算卡方统计量
        chi_square = 0
        for row, cols in crosstab.items():
            for col, count in cols.items():
                exp = expected[row][col]
                if exp > 0:
                    chi_square += ((count - exp) ** 2) / exp
        
        # 计算自由度
        degrees_of_freedom = (len(row_totals) - 1) * (len(column_totals) - 1)
        
        # 计算p值（使用卡方分布）
        # 这里使用近似计算，实际应用中可能需要使用更精确的方法
        from scipy.stats import chi2
        p_value = 1 - chi2.cdf(chi_square, degrees_of_freedom)
        
        return {
            'chi_square': chi_square,
            'degrees_of_freedom': degrees_of_freedom,
            'p_value': p_value
        }