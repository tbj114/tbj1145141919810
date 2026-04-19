#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逻辑回归实现
"""

import numpy as np


class LogisticRegression:
    """逻辑回归类"""

    @staticmethod
    def _sigmoid(z):
        """Sigmoid 函数"""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

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
    def fit(y, X, learning_rate=0.01, max_iter=10000, tol=1e-6):
        """
        拟合逻辑回归模型

        Args:
            y: 因变量数据（二分类 0/1）
            X: 自变量数据列表（每个元素是一个变量的数据）
            learning_rate: 学习率
            max_iter: 最大迭代次数
            tol: 收敛容差

        Returns:
            dict: 包含回归结果的字典
        """
        # 确保 X 是列表
        if not isinstance(X, (list, tuple)):
            X = [X]
        
        # 过滤数据
        y_arr, X_arr = LogisticRegression._filter_data(y, X)
        
        if y_arr is None:
            return None
        
        n = len(y_arr)
        k = len(X_arr)  # 自变量数量
        
        if n < k + 2:  # 需要足够的自由度
            return None
        
        # 确保 y 是 0/1
        y_arr = (y_arr >= 0.5).astype(float)
        
        # 创建设计矩阵（包含截距项）
        design_matrix = np.column_stack([np.ones(n)] + [arr for arr in X_arr])
        
        # 初始化参数
        beta = np.zeros(k + 1)
        loss_history = []
        
        # 梯度下降
        for i in range(max_iter):
            # 计算预测概率
            z = design_matrix @ beta
            p = LogisticRegression._sigmoid(z)
            
            # 计算损失（对数似然）
            loss = -np.sum(y_arr * np.log(p + 1e-10) + (1 - y_arr) * np.log(1 - p + 1e-10)) / n
            loss_history.append(loss)
            
            # 计算梯度
            gradient = (design_matrix.T @ (p - y_arr)) / n
            
            # 更新参数
            beta_new = beta - learning_rate * gradient
            
            # 检查收敛
            if np.max(np.abs(beta_new - beta)) < tol:
                beta = beta_new
                break
            
            beta = beta_new
        
        # 计算最终预测概率
        z = design_matrix @ beta
        p = LogisticRegression._sigmoid(z)
        
        # 计算系数的标准误（使用逆信息矩阵）
        se_coef = None
        z_scores = None
        p_values = None
        
        try:
            # 计算信息矩阵（Fisher信息）
            W = np.diag(p * (1 - p))
            xtx = design_matrix.T @ W @ design_matrix
            xtx_inv = np.linalg.inv(xtx)
            
            se_coef = np.sqrt(np.diag(xtx_inv))
            
            # 计算 z 分数和 p 值
            z_scores = beta / se_coef
            
            try:
                from scipy import stats
                p_values = []
                for z in z_scores:
                    p_values.append(2 * (1 - stats.norm.cdf(abs(z))))
                p_values = np.array(p_values)
            except ImportError:
                pass
        except np.linalg.LinAlgError:
            pass
        
        # 计算模型拟合指标
        # 计算 -2LL
        ll_null = -np.sum(y_arr * np.log(np.mean(y_arr) + 1e-10) + (1 - y_arr) * np.log(1 - np.mean(y_arr) + 1e-10))
        ll_model = -np.sum(y_arr * np.log(p + 1e-10) + (1 - y_arr) * np.log(1 - p + 1e-10))
        ll_ratio = 2 * (ll_null - ll_model)
        
        # 计算伪 R-squared（McFadden）
        pseudo_r2 = 1 - ll_model / ll_null
        
        # 计算似然比 p 值
        lr_p_value = None
        try:
            from scipy import stats
            lr_p_value = 1 - stats.chi2.cdf(ll_ratio, k)
        except ImportError:
            pass
        
        # 计算分类预测
        y_pred = (p >= 0.5).astype(int)
        
        # 计算分类准确率
        accuracy = np.mean(y_pred == y_arr)
        
        # 计算混淆矩阵
        true_positive = np.sum((y_pred == 1) & (y_arr == 1))
        true_negative = np.sum((y_pred == 0) & (y_arr == 0))
        false_positive = np.sum((y_pred == 1) & (y_arr == 0))
        false_negative = np.sum((y_pred == 0) & (y_arr == 1))
        
        # 计算其他指标
        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else None
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else None
        f1 = 2 * precision * recall / (precision + recall) if (precision is not None and recall is not None and (precision + recall) > 0) else None
        
        return {
            'coefficients': beta,  # [intercept, coef1, coef2, ...]
            'n': len(y),
            'valid_n': n,
            'k': k,
            'n_iterations': i + 1,
            'p': p,
            'y_pred': y_pred,
            'se_coef': se_coef,
            'z_scores': z_scores,
            'p_values': p_values,
            'accuracy': accuracy,
            'confusion_matrix': {
                'true_positive': true_positive,
                'true_negative': true_negative,
                'false_positive': false_positive,
                'false_negative': false_negative
            },
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'pseudo_r2': pseudo_r2,
            'll_null': ll_null,
            'll_model': ll_model,
            'll_ratio': ll_ratio,
            'lr_p_value': lr_p_value
        }

    @staticmethod
    def predict_proba(model, X_new):
        """
        使用拟合的模型预测概率

        Args:
            model: 之前拟合的模型结果
            X_new: 新的自变量数据列表

        Returns:
            array: 预测概率
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
        
        # 预测概率
        z = design_matrix @ beta
        p = LogisticRegression._sigmoid(z)
        
        return p

    @staticmethod
    def predict(model, X_new, threshold=0.5):
        """
        使用拟合的模型进行分类预测

        Args:
            model: 之前拟合的模型结果
            X_new: 新的自变量数据列表
            threshold: 分类阈值

        Returns:
            array: 预测分类
        """
        proba = LogisticRegression.predict_proba(model, X_new)
        if proba is None:
            return None
        
        return (proba >= threshold).astype(int)
