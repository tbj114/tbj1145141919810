#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
偏相关分析实现
"""

import numpy as np
from axaltyx.core.correlation.bivariate import BivariateCorrelation


class PartialCorrelation:
    """偏相关分析类"""

    @staticmethod
    def _filter_data(x, y, controls):
        """过滤掉包含 None 和 NaN 的数据"""
        valid_rows = []
        for i in range(len(x)):
            row = [x[i], y[i]] + [control[i] for control in controls]
            valid = True
            for val in row:
                if val is None or (isinstance(val, (int, float)) and np.isnan(val)):
                    valid = False
                    break
            if valid:
                valid_rows.append([float(v) for v in row])
        
        if not valid_rows:
            return None, None, None
        
        arr = np.array(valid_rows)
        return arr[:, 0], arr[:, 1], arr[:, 2:].T

    @staticmethod
    def partial(x, y, controls):
        """
        计算偏相关系数，控制一个或多个变量

        Args:
            x: 第一个变量的数据
            y: 第二个变量的数据
            controls: 要控制的变量列表（可以是单个变量）

        Returns:
            dict: 包含偏相关系数、p值等的字典
        """
        # 确保 controls 是列表
        if not isinstance(controls, (list, tuple)):
            controls = [controls]
        
        # 过滤数据
        x_arr, y_arr, control_arrs = PartialCorrelation._filter_data(x, y, controls)
        
        if x_arr is None:
            return {
                'partial_correlation': None,
                'p_value': None,
                'n': len(x),
                'valid_n': 0,
                'n_controls': len(controls)
            }
        
        n = len(x_arr)
        n_controls = len(controls)
        
        if n < n_controls + 3:  # 需要足够的自由度
            return {
                'partial_correlation': None,
                'p_value': None,
                'n': len(x),
                'valid_n': n,
                'n_controls': n_controls
            }
        
        # 创建数据矩阵
        data_matrix = np.column_stack([x_arr, y_arr] + [arr for arr in control_arrs])
        
        # 计算相关矩阵
        corr_result = BivariateCorrelation.correlation_matrix(data_matrix)
        
        if corr_result is None:
            return {
                'partial_correlation': None,
                'p_value': None,
                'n': len(x),
                'valid_n': n,
                'n_controls': n_controls
            }
        
        corr_matrix = corr_result['correlation_matrix']
        
        # 使用矩阵方法计算偏相关系数
        # 构建子矩阵
        idx_x = 0
        idx_y = 1
        control_indices = list(range(2, 2 + n_controls))
        
        # 获取子矩阵
        # r_xy: x和y的相关
        # r_xz: x和控制变量的相关
        # r_yz: y和控制变量的相关
        # r_zz: 控制变量之间的相关
        r_xy = corr_matrix[idx_x, idx_y]
        r_xz = corr_matrix[idx_x, control_indices].reshape(1, -1)
        r_yz = corr_matrix[idx_y, control_indices].reshape(1, -1)
        r_zz = corr_matrix[np.ix_(control_indices, control_indices)]
        
        # 计算偏相关系数
        # r_xy.z = (r_xy - r_xz * r_zz^{-1} * r_yz') / sqrt((1 - r_xz * r_zz^{-1} * r_xz') * (1 - r_yz * r_zz^{-1} * r_yz'))
        try:
            # 处理可能的奇异矩阵
            r_zz_inv = np.linalg.inv(r_zz)
        except np.linalg.LinAlgError:
            # 使用伪逆
            r_zz_inv = np.linalg.pinv(r_zz)
        
        term1 = r_xz @ r_zz_inv @ r_yz.T
        term2 = r_xz @ r_zz_inv @ r_xz.T
        term3 = r_yz @ r_zz_inv @ r_yz.T
        
        numerator = r_xy - term1[0, 0]
        denominator = np.sqrt((1 - term2[0, 0]) * (1 - term3[0, 0]))
        
        partial_r = numerator / denominator if denominator != 0 else None
        
        # 计算 p 值
        p_value = None
        if partial_r is not None:
            df = n - n_controls - 2
            try:
                from scipy import stats
                if (1 - partial_r ** 2) != 0:
                    t_stat = partial_r * np.sqrt(df / (1 - partial_r ** 2))
                    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
            except ImportError:
                pass
        
        return {
            'partial_correlation': partial_r,
            'p_value': p_value,
            'n': len(x),
            'valid_n': n,
            'df': n - n_controls - 2,
            'n_controls': n_controls
        }

    @staticmethod
    def partial_correlation_matrix(data, control_indices):
        """
        计算偏相关矩阵，控制指定的变量

        Args:
            data: 数据矩阵
            control_indices: 要控制的变量索引列表

        Returns:
            dict: 包含偏相关系数矩阵和p值矩阵的字典
        """
        n_vars = data.shape[1] if len(data.shape) > 1 else 1
        
        if n_vars <= 2:
            return None
        
        # 首先计算简单相关矩阵
        corr_result = BivariateCorrelation.correlation_matrix(data)
        if corr_result is None:
            return None
        
        corr_matrix = corr_result['correlation_matrix']
        
        # 计算偏相关矩阵
        partial_corr_matrix = np.zeros((n_vars, n_vars))
        p_matrix = np.zeros((n_vars, n_vars))
        
        # 获取非控制变量的索引
        variable_indices = [i for i in range(n_vars) if i not in control_indices]
        
        # 计算每对变量的偏相关
        for i_idx, i in enumerate(variable_indices):
            for j_idx, j in enumerate(variable_indices):
                if i == j:
                    partial_corr_matrix[i, j] = 1.0
                    p_matrix[i, j] = 1.0
                else:
                    # 计算偏相关
                    x = data[:, i]
                    y = data[:, j]
                    controls = [data[:, k] for k in control_indices]
                    result = PartialCorrelation.partial(x, y, controls)
                    if result['partial_correlation'] is not None:
                        partial_corr_matrix[i, j] = result['partial_correlation']
                        partial_corr_matrix[j, i] = partial_corr_matrix[i, j]
                        if result['p_value'] is not None:
                            p_matrix[i, j] = result['p_value']
                            p_matrix[j, i] = p_matrix[i, j]
                    else:
                        partial_corr_matrix[i, j] = np.nan
                        partial_corr_matrix[j, i] = np.nan
                        p_matrix[i, j] = np.nan
                        p_matrix[j, i] = np.nan
        
        return {
            'partial_correlation_matrix': partial_corr_matrix,
            'p_value_matrix': p_matrix,
            'control_indices': control_indices,
            'variable_indices': variable_indices
        }
