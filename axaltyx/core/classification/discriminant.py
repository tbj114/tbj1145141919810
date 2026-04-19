#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
判别分析
"""

import numpy as np


class LinearDiscriminantAnalysis:
    """线性判别分析 (Linear Discriminant Analysis, LDA)"""

    @staticmethod
    def _filter_data(X, y):
        """过滤无效数据"""
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)
        
        if X.ndim != 2:
            raise ValueError("特征数据必须是二维数组")
        if y.ndim != 1:
            raise ValueError("标签数据必须是一维数组")
        if len(X) != len(y):
            raise ValueError("特征数据和标签数据长度必须一致")
        
        # 过滤含有 NaN 的行
        mask = ~np.isnan(X).any(axis=1)
        X_filtered = X[mask]
        y_filtered = y[mask]
        
        return X_filtered, y_filtered

    @staticmethod
    def fit(X, y, n_components=None):
        """
        训练线性判别分析模型

        Args:
            X: 输入特征矩阵，形状为 (n_samples, n_features)
            y: 标签向量，形状为 (n_samples,)
            n_components: 要保留的判别分量数量

        Returns:
            dict: 包含模型参数的字典
        """
        # 过滤数据
        X, y = LinearDiscriminantAnalysis._filter_data(X, y)
        n_samples, n_features = X.shape
        
        # 获取唯一类别
        classes = np.unique(y)
        n_classes = len(classes)
        
        if n_components is None:
            n_components = min(n_classes - 1, n_features)
        elif n_components > min(n_classes - 1, n_features):
            n_components = min(n_classes - 1, n_features)
        
        # 计算类均值
        class_means = []
        for cls in classes:
            class_means.append(X[y == cls].mean(axis=0))
        class_means = np.array(class_means)
        
        # 计算总体均值
        overall_mean = X.mean(axis=0)
        
        # 计算类内散布矩阵
        Sw = np.zeros((n_features, n_features))
        for i, cls in enumerate(classes):
            class_data = X[y == cls]
            mean_diff = class_data - class_means[i]
            Sw += np.dot(mean_diff.T, mean_diff)
        
        # 计算类间散布矩阵
        Sb = np.zeros((n_features, n_features))
        for i, cls in enumerate(classes):
            n_cls = len(X[y == cls])
            mean_diff = class_means[i] - overall_mean
            Sb += n_cls * np.outer(mean_diff, mean_diff)
        
        # 计算 Sw^-1 * Sb 的特征值和特征向量
        try:
            # 求解特征值问题
            eigenvalues, eigenvectors = np.linalg.eigh(np.dot(np.linalg.inv(Sw), Sb))
        except np.linalg.LinAlgError:
            # 如果 Sw 是奇异的，添加一个小的正则化项
            Sw += np.eye(n_features) * 1e-6
            eigenvalues, eigenvectors = np.linalg.eigh(np.dot(np.linalg.inv(Sw), Sb))
        
        # 按特征值降序排序
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        
        # 选择前 n_components 个特征向量
        eigenvectors = eigenvectors[:, :n_components]
        
        # 计算投影矩阵
        projections = np.dot(X, eigenvectors)
        
        return {
            'classes': classes,
            'n_classes': n_classes,
            'n_components': n_components,
            'class_means': class_means,
            'overall_mean': overall_mean,
            'Sw': Sw,
            'Sb': Sb,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'projections': projections
        }

    @staticmethod
    def transform(X, eigenvectors):
        """
        使用训练好的模型转换数据

        Args:
            X: 输入特征矩阵
            eigenvectors: 特征向量矩阵

        Returns:
            np.ndarray: 转换后的数据
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        return np.dot(X, eigenvectors)

    @staticmethod
    def predict(X, model):
        """
        预测新数据的类别

        Args:
            X: 输入特征矩阵
            model: 训练好的模型

        Returns:
            np.ndarray: 预测的类别
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        
        # 转换数据
        X_transformed = LinearDiscriminantAnalysis.transform(X, model['eigenvectors'])
        
        # 计算每个样本到各类别均值的距离
        predictions = []
        for sample in X_transformed:
            distances = []
            for i, cls in enumerate(model['classes']):
                # 计算类均值在判别空间中的投影
                mean_proj = np.dot(model['class_means'][i], model['eigenvectors'])
                # 计算欧氏距离
                dist = np.sqrt(((sample - mean_proj) ** 2).sum())
                distances.append(dist)
            # 选择距离最小的类别
            predictions.append(model['classes'][np.argmin(distances)])
        
        return np.array(predictions)
