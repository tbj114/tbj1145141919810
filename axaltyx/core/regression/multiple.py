#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多元线性回归实现
"""

import numpy as np


class MultipleLinearRegression:
    """多元线性回归类"""

    @staticmethod
    def _filter_data(y, X):
        """过滤掉包含 None 和 NaN 的数据"""
        valid_rows = []
        for i in range(len(y)):
            row = [y[i]]
            for j in range(len(X)):
                row.append(X[j][i])
            valid = True
            for val in row:
                if val is None or (isinstance(val, (int, float)) and np.isnan(val)):
                    valid = False
                    break
            if valid:
                valid_rows.append([float(v) for v in row])
        
        if not valid_rows:
            return None, None
        
        arr = np.array(valid_rows)
        return arr[:, 0], arr[:, 1:].T

    @staticmethod
    def fit(y, X):
        """
        拟合多元线性回归模型

        Args:
            y: 因变量数据
            X: 自变量数据列表（每个元素是一个变量的数据）

        Returns:
            dict: 包含回归结果的字典
        """
        # 确保 X 是列表
        if not isinstance(X, (list, tuple)):
            X = [X]
        
        # 过滤数据
        y_arr, X_arr = MultipleLinearRegression._filter_data(y, X)
        
        if y_arr is None:
            return None
        
        n = len(y_arr)
        k = len(X_arr)  # 自变量数量
        
        if n < k + 2:  # 需要足够的自由度
            return None
        
        # 创建设计矩阵（包含截距项）
        design_matrix = np.column_stack([np.ones(n)] + [arr for arr in X_arr])
        
        # 使用最小二乘法求解
        try:
            # 使用 np.linalg.lstsq 求解
            beta_hat, residuals, rank, s = np.linalg.lstsq(design_matrix, y_arr, rcond=None)
        except np.linalg.LinAlgError:
            return None
        
        # 计算预测值
        y_pred = design_matrix @ beta_hat
        
        # 计算基本统计量
        mean_y = np.mean(y_arr)
        total_ss = np.sum((y_arr - mean_y) ** 2)
        residual_ss = np.sum((y_arr - y_pred) ** 2) if len(residuals) > 0 else None
        regression_ss = total_ss - residual_ss if residual_ss is not None else None
        
        # 计算 R-squared
        r_squared = 1 - (residual_ss / total_ss) if residual_ss is not None and total_ss != 0 else None
        
        # 计算调整的 R-squared
        adj_r_squared = 1 - ((residual_ss / (n - k - 1)) / (total_ss / (n - 1))) if residual_ss is not None and total_ss != 0 and n > k + 1 else None
        
        # 计算自由度
        df_total = n - 1
        df_regression = k
        df_residual = n - k - 1
        
        # 计算均方
        mse = residual_ss / df_residual if residual_ss is not None and df_residual > 0 else None
        rmse = np.sqrt(mse) if mse is not None else None
        
        ms_regression = regression_ss / df_regression if regression_ss is not None and df_regression > 0 else None
        
        # 计算 F 统计量
        f_statistic = None
        f_p_value = None
        if ms_regression is not None and mse is not None and mse > 0:
            f_statistic = ms_regression / mse
            try:
                from scipy import stats
                f_p_value = 1 - stats.f.cdf(f_statistic, df_regression, df_residual)
            except ImportError:
                pass
        
        # 计算系数的标准误、t值和p值
        se_coef = None
        t_values = None
        p_values = None
        
        if mse is not None and mse > 0:
            try:
                # 计算 (X'X)^{-1}
                xtx = design_matrix.T @ design_matrix
                xtx_inv = np.linalg.inv(xtx)
                
                # 计算标准误
                se_coef = np.sqrt(np.diag(xtx_inv) * mse)
                
                # 计算 t 值
                t_values = beta_hat / se_coef
                
                # 计算 p 值
                p_values = []
                try:
                    from scipy import stats
                    for t in t_values:
                        p_values.append(2 * (1 - stats.t.cdf(abs(t), df_residual)))
                    p_values = np.array(p_values)
                except ImportError:
                    pass
            except np.linalg.LinAlgError:
                pass
        
        # 计算方差膨胀因子 (VIF)
        vif = None
        if k > 1:
            vif = []
            for i in range(k):
                # 计算第 i 个自变量对其他自变量的回归
                y_vif = X_arr[i]
                X_vif = [X_arr[j] for j in range(k) if j != i]
                
                # 使用我们的简单回归或多元回归来计算
                vif_result = MultipleLinearRegression.fit(y_vif, X_vif)
                if vif_result is not None and vif_result['r_squared'] is not None:
                    vif_i = 1 / (1 - vif_result['r_squared']) if vif_result['r_squared'] < 1 else float('inf')
                    vif.append(vif_i)
                else:
                    vif.append(float('inf'))
            vif = np.array(vif)
        
        # 组织结果
        return {
            'coefficients': beta_hat,  # [intercept, coef1, coef2, ...]
            'n': len(y),
            'valid_n': n,
            'k': k,
            'df_total': df_total,
            'df_regression': df_regression,
            'df_residual': df_residual,
            'r_squared': r_squared,
            'adj_r_squared': adj_r_squared,
            'f_statistic': f_statistic,
            'f_p_value': f_p_value,
            'mse': mse,
            'rmse': rmse,
            'total_ss': total_ss,
            'regression_ss': regression_ss,
            'residual_ss': residual_ss,
            'se_coef': se_coef,
            't_values': t_values,
            'p_values': p_values,
            'vif': vif,
            'y_pred': y_pred,
            'residuals': y_arr - y_pred
        }

    @staticmethod
    def predict(model, X_new):
        """
        使用拟合的模型进行预测

        Args:
            model: 之前拟合的模型结果
            X_new: 新的自变量数据列表

        Returns:
            array: 预测值
        """
        if model is None or model['coefficients'] is None:
            return None
        
        beta = model['coefficients']
        
        # 处理新数据
        if not isinstance(X_new, (list, tuple)):
            X_new = [X_new]
        
        # 确保每个变量的数据长度一致
        n = len(X_new[0]) if X_new else 0
        for i in range(1, len(X_new)):
            if len(X_new[i]) != n:
                return None
        
        # 创建设计矩阵
        design_matrix = np.column_stack([np.ones(n)] + [np.array(arr) for arr in X_new])
        
        # 预测
        y_pred = design_matrix @ beta
        
        return y_pred
