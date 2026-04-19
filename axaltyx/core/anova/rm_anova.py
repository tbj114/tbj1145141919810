#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重复测量方差分析实现
"""

import numpy as np


class RMANOVA:
    """重复测量方差分析类"""

    @staticmethod
    def _filter_data(data):
        """过滤掉包含 None 和 NaN 的数据"""
        filtered_data = []
        for row in data:
            is_valid = True
            for x in row:
                if x is None or (isinstance(x, (int, float)) and np.isnan(x)):
                    is_valid = False
                    break
            if is_valid:
                filtered_data.append(row)
        return np.array(filtered_data)

    @staticmethod
    def calculate(data):
        """
        执行单因素重复测量方差分析

        Args:
            data: 数据矩阵，每行是一个被试，每列是一个测量时间点

        Returns:
            dict: 包含 RM ANOVA 结果的字典
        """
        # 过滤数据
        filtered_data = RMANOVA._filter_data(data)

        if len(filtered_data) < 2 or filtered_data.shape[1] < 2:
            return None

        n, k = filtered_data.shape

        # 计算各种均值
        grand_mean = np.mean(filtered_data)
        subject_means = np.mean(filtered_data, axis=1)
        time_means = np.mean(filtered_data, axis=0)

        # 计算平方和
        # 总平方和 (SST)
        sst = np.sum((filtered_data - grand_mean) ** 2)

        # 处理间平方和 (SSBetween - Time)
        ssb_time = n * np.sum((time_means - grand_mean) ** 2)

        # 被试间平方和 (SSBetween - Subjects)
        ssb_subject = k * np.sum((subject_means - grand_mean) ** 2)

        # 误差平方和 (SSWithin - 时间×被试交互)
        sse = sst - ssb_time - ssb_subject

        # 计算自由度
        df_total = n * k - 1
        df_time = k - 1
        df_subject = n - 1
        df_error = (k - 1) * (n - 1)

        # 计算均方
        mst_time = ssb_time / df_time if df_time > 0 else None
        mse = sse / df_error if df_error > 0 else None

        # 计算 F 值和 p 值
        f_value = None
        p_value = None

        if mst_time is not None and mse is not None and mse > 0:
            f_value = mst_time / mse
            try:
                from scipy import stats
                p_value = 1 - stats.f.cdf(f_value, df_time, df_error)
            except:
                p_value = None

        # 计算球形检验
        sphericity_result = RMANOVA._calculate_sphericity(filtered_data)

        # 计算效应大小
        eta_squared = ssb_time / sst if sst > 0 else None
        partial_eta_squared = ssb_time / (ssb_time + sse) if (ssb_time + sse) > 0 else None

        return {
            'data': filtered_data,
            'n': n,
            'k': k,
            'grand_mean': grand_mean,
            'time_means': time_means,
            'subject_means': subject_means,
            'ss_total': sst,
            'ss_time': ssb_time,
            'ss_subject': ssb_subject,
            'ss_error': sse,
            'df_total': df_total,
            'df_time': df_time,
            'df_subject': df_subject,
            'df_error': df_error,
            'ms_time': mst_time,
            'ms_error': mse,
            'f_value': f_value,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'partial_eta_squared': partial_eta_squared,
            'sphericity': sphericity_result
        }

    @staticmethod
    def _calculate_sphericity(data):
        """
        计算 Mauchly's 球形检验

        Args:
            data: 重复测量数据

        Returns:
            dict: 包含球形检验结果的字典
        """
        n, k = data.shape

        if k < 3:
            return None

        try:
            # 计算协方差矩阵
            cov_matrix = np.cov(data, rowvar=False)

            # 计算协方差矩阵的特征值
            eigenvalues = np.linalg.eigvals(cov_matrix)
            eigenvalues = np.real(eigenvalues)

            # 计算球形检验统计量 W
            mean_eig = np.mean(eigenvalues)
            log_det = np.sum(np.log(eigenvalues))
            w = (np.prod(eigenvalues) / (mean_eig ** k)) if mean_eig != 0 else None

            # 计算近似卡方值
            chi_square = None
            df = k * (k - 1) / 2 - 1
            p_value = None

            if w is not None and w > 0:
                # 使用 Bartlett 近似
                chi_square = -(n - 1) * np.log(w)
                try:
                    from scipy import stats
                    p_value = 1 - stats.chi2.cdf(chi_square, df)
                except:
                    p_value = None

            # 计算 Greenhouse-Geisser epsilon
            sigma_bar = np.trace(cov_matrix) / k
            sum_sq_off_diag = (np.sum(cov_matrix ** 2) - np.sum(np.diag(cov_matrix) ** 2)) / 2
            sum_sq_cov = np.sum(cov_matrix ** 2)
            epsilon_gg = (k * sigma_bar ** 2) / (sum_sq_cov - 2 * sum_sq_off_diag / (n - 1)) if sum_sq_cov > 0 else None
            epsilon_gg = min(max(epsilon_gg, 1 / (k - 1)), 1)

            # 计算 Huynh-Feldt epsilon
            epsilon_hf = min(((n * (k - 1) * epsilon_gg - 2) / ((k - 1) * (n - 1) - (k - 1) * epsilon_gg)), 1)

            return {
                'w_statistic': w,
                'chi_square': chi_square,
                'df': df,
                'p_value': p_value,
                'epsilon_gg': epsilon_gg,
                'epsilon_hf': epsilon_hf
            }

        except:
            return None
