#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习 - 回归算法
"""

import numpy as np


class LinearRegression:
    """线性回归模型"""

    def __init__(self):
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        """
        训练线性回归模型

        Args:
            X: 特征矩阵
            y: 目标向量

        Returns:
            self: 训练好的模型
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        # 添加截距项
        X_with_intercept = np.hstack([np.ones((X.shape[0], 1)), X])

        # 使用最小二乘法求解
        try:
            coefficients = np.linalg.inv(X_with_intercept.T.dot(X_with_intercept)).dot(X_with_intercept.T).dot(y)
        except np.linalg.LinAlgError:
            # 如果矩阵不可逆，使用伪逆
            coefficients = np.linalg.pinv(X_with_intercept).dot(y)

        self.intercept_ = coefficients[0]
        self.coef_ = coefficients[1:]

        return self

    def predict(self, X):
        """
        预测目标值

        Args:
            X: 特征矩阵

        Returns:
            np.ndarray: 预测值
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        return np.dot(X, self.coef_) + self.intercept_


class RidgeRegression:
    """岭回归模型"""

    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        """
        训练岭回归模型

        Args:
            X: 特征矩阵
            y: 目标向量

        Returns:
            self: 训练好的模型
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        # 添加截距项
        X_with_intercept = np.hstack([np.ones((X.shape[0], 1)), X])

        # 计算岭回归系数
        n_features = X_with_intercept.shape[1]
        identity = np.eye(n_features)
        identity[0, 0] = 0  # 不对截距项进行正则化

        coefficients = np.linalg.inv(X_with_intercept.T.dot(X_with_intercept) + self.alpha * identity).dot(X_with_intercept.T).dot(y)

        self.intercept_ = coefficients[0]
        self.coef_ = coefficients[1:]

        return self

    def predict(self, X):
        """
        预测目标值

        Args:
            X: 特征矩阵

        Returns:
            np.ndarray: 预测值
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        return np.dot(X, self.coef_) + self.intercept_


class KNeighborsRegressor:
    """K最近邻回归器"""

    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        """
        训练 KNN 回归模型

        Args:
            X: 特征矩阵
            y: 目标向量

        Returns:
            self: 训练好的模型
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        self.X_train = X
        self.y_train = y
        return self

    def predict(self, X):
        """
        预测目标值

        Args:
            X: 特征矩阵

        Returns:
            np.ndarray: 预测值
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        predictions = []
        for sample in X:
            # 计算距离
            distances = np.sqrt(np.sum((self.X_train - sample) ** 2, axis=1))
            # 找到最近的 K 个邻居
            k_indices = np.argsort(distances)[:self.n_neighbors]
            # 计算平均值
            predictions.append(np.mean(self.y_train[k_indices]))

        return np.array(predictions)
