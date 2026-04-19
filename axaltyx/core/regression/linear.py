#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单线性回归实现
"""

import numpy as np


class SimpleLinearRegression:
    """简单线性回归类"""

    @staticmethod
    def _filter_data(x, y):
        """过滤掉包含 None 和 NaN 的数据"""
        valid_x = []
        valid_y = []
        for xi, yi in zip(x, y):
            x_valid = xi is not None and (
                not isinstance(xi, (int, float)) or not np.isnan(xi)
            )
            y_valid = yi is not None and (
                not isinstance(yi, (int, float)) or not np.isnan(yi)
            )
            if x_valid and y_valid:
                valid_x.append(xi)
                valid_y.append(yi)
        return np.array(valid_x), np.array(valid_y)

    @staticmethod
    def fit(x, y):
        """
        拟合简单线性回归模型

        Args:
            x: 自变量数据
            y: 因变量数据

        Returns:
            dict: 包含回归结果的字典
        """
        x_arr, y_arr = SimpleLinearRegression._filter_data(x, y)
        n = len(x_arr)

        if n < 2:
            return {
                'intercept': None,
                'slope': None,
                'r_squared': None,
                'r': None,
                'f_statistic': None,
                'f_p_value': None,
                'n': len(x),
                'valid_n': n,
                'df': None,
                'mse': None,
                'rmse': None
            }

        # 计算基本统计量
        mean_x = np.mean(x_arr)
        mean_y = np.mean(y_arr)
        std_x = np.std(x_arr, ddof=1)
        std_y = np.std(y_arr, ddof=1)

        # 计算回归系数
        numerator = np.sum((x_arr - mean_x) * (y_arr - mean_y))
        denominator = np.sum((x_arr - mean_x) ** 2)

        slope = numerator / denominator if denominator != 0 else None
        intercept = mean_y - slope * mean_x if slope is not None else None

        if slope is None or intercept is None:
            return {
                'intercept': None,
                'slope': None,
                'r_squared': None,
                'r': None,
                'f_statistic': None,
                'f_p_value': None,
                'n': len(x),
                'valid_n': n,
                'df': None,
                'mse': None,
                'rmse': None
            }

        # 计算预测值
        y_pred = intercept + slope * x_arr

        # 计算 R-squared
        total_ss = np.sum((y_arr - mean_y) ** 2)
        residual_ss = np.sum((y_arr - y_pred) ** 2)
        regression_ss = total_ss - residual_ss

        r_squared = 1 - (residual_ss / total_ss) if total_ss != 0 else None

        # 计算 Pearson 相关系数
        r = np.sqrt(r_squared) if r_squared is not None else None
        if slope < 0 and r is not None:
            r = -r

        # 计算 MSE 和 RMSE
        df = n - 2
        mse = residual_ss / df if df > 0 else None
        rmse = np.sqrt(mse) if mse is not None else None

        # 计算 F 统计量
        f_statistic = None
        f_p_value = None
        if regression_ss is not None and residual_ss is not None and df > 0:
            ms_regression = regression_ss / 1
            ms_residual = residual_ss / df
            if ms_residual > 0:
                f_statistic = ms_regression / ms_residual
                try:
                    from scipy import stats
                    f_p_value = 1 - stats.f.cdf(f_statistic, 1, df)
                except ImportError:
                    pass

        # 计算系数的标准误、t值和p值
        intercept_se = None
        intercept_t = None
        intercept_p = None
        slope_se = None
        slope_t = None
        slope_p = None

        if mse is not None and denominator != 0:
            # 计算标准误
            slope_se = np.sqrt(mse / denominator)
            intercept_se = np.sqrt(mse * (1/n + mean_x**2 / denominator))
            
            # 计算 t 值
            slope_t = slope / slope_se if slope_se != 0 else None
            intercept_t = intercept / intercept_se if intercept_se != 0 else None
            
            # 计算 p 值
            try:
                from scipy import stats
                if slope_t is not None:
                    slope_p = 2 * (1 - stats.t.cdf(abs(slope_t), df))
                if intercept_t is not None:
                    intercept_p = 2 * (1 - stats.t.cdf(abs(intercept_t), df))
            except ImportError:
                pass

        return {
            'intercept': intercept,
            'slope': slope,
            'r_squared': r_squared,
            'r': r,
            'f_statistic': f_statistic,
            'f_p_value': f_p_value,
            'n': len(x),
            'valid_n': n,
            'df': df,
            'mse': mse,
            'rmse': rmse,
            'intercept_se': intercept_se,
            'intercept_t': intercept_t,
            'intercept_p': intercept_p,
            'slope_se': slope_se,
            'slope_t': slope_t,
            'slope_p': slope_p,
            'y_pred': y_pred,
            'residuals': y_arr - y_pred
        }

    @staticmethod
    def predict(model, x_new):
        """
        使用拟合的模型进行预测

        Args:
            model: 之前拟合的模型结果
            x_new: 新的自变量数据

        Returns:
            array: 预测值
        """
        if model is None or model['intercept'] is None or model['slope'] is None:
            return None
        
        intercept = model['intercept']
        slope = model['slope']
        
        # 处理新数据
        x_arr = np.array(x_new)
        
        # 预测
        y_pred = intercept + slope * x_arr
        
        return y_pred
