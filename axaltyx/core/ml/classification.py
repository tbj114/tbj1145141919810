#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习 - 分类算法
"""

import numpy as np


class LogisticRegression:
    """逻辑回归分类器"""

    def __init__(self, learning_rate=0.01, max_iter=1000, random_state=None):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.random_state = random_state
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        """
        训练逻辑回归模型

        Args:
            X: 特征矩阵
            y: 标签向量

        Returns:
            self: 训练好的模型
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        n_samples, n_features = X.shape
        
        # 初始化参数
        if self.random_state is not None:
            np.random.seed(self.random_state)
        self.coef_ = np.random.randn(n_features)
        self.intercept_ = np.random.randn()

        # 梯度下降
        for _ in range(self.max_iter):
            # 计算线性组合
            z = np.dot(X, self.coef_) + self.intercept_
            # 计算 sigmoid 函数
            y_pred = 1 / (1 + np.exp(-z))
            # 计算梯度
            gradient_w = np.dot(X.T, (y_pred - y)) / n_samples
            gradient_b = np.mean(y_pred - y)
            # 更新参数
            self.coef_ -= self.learning_rate * gradient_w
            self.intercept_ -= self.learning_rate * gradient_b

        return self

    def predict_proba(self, X):
        """
        预测概率

        Args:
            X: 特征矩阵

        Returns:
            np.ndarray: 预测概率
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        z = np.dot(X, self.coef_) + self.intercept_
        return 1 / (1 + np.exp(-z))

    def predict(self, X, threshold=0.5):
        """
        预测类别

        Args:
            X: 特征矩阵
            threshold: 阈值

        Returns:
            np.ndarray: 预测类别
        """
        return (self.predict_proba(X) >= threshold).astype(int)


class KNearestNeighbors:
    """K最近邻分类器"""

    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        """
        训练 KNN 模型

        Args:
            X: 特征矩阵
            y: 标签向量

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
        预测类别

        Args:
            X: 特征矩阵

        Returns:
            np.ndarray: 预测类别
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        predictions = []
        for sample in X:
            # 计算距离
            distances = np.sqrt(np.sum((self.X_train - sample) ** 2, axis=1))
            # 找到最近的 K 个邻居
            k_indices = np.argsort(distances)[:self.n_neighbors]
            # 投票
            k_neighbors = self.y_train[k_indices]
            unique, counts = np.unique(k_neighbors, return_counts=True)
            predictions.append(unique[np.argmax(counts)])

        return np.array(predictions)


class DecisionTreeClassifier:
    """决策树分类器（简化版）"""

    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None

    def fit(self, X, y):
        """
        训练决策树模型

        Args:
            X: 特征矩阵
            y: 标签向量

        Returns:
            self: 训练好的模型
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        self.tree = self._build_tree(X, y, depth=0)
        return self

    def _build_tree(self, X, y, depth):
        """递归构建决策树"""
        n_samples, n_features = X.shape
        n_classes = len(np.unique(y))

        # 停止条件
        if (self.max_depth is not None and depth >= self.max_depth) or \
           n_samples < self.min_samples_split or \
           n_classes == 1:
            # 返回叶子节点
            class_counts = np.bincount(y.astype(int))
            return {'type': 'leaf', 'class': np.argmax(class_counts)}

        # 选择最佳特征和阈值
        best_feature, best_threshold = self._find_best_split(X, y)

        # 分割数据
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = X[:, best_feature] > best_threshold

        # 递归构建子树
        left_tree = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_tree = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return {
            'type': 'node',
            'feature': best_feature,
            'threshold': best_threshold,
            'left': left_tree,
            'right': right_tree
        }

    def _find_best_split(self, X, y):
        """找到最佳分割点"""
        best_gini = float('inf')
        best_feature = 0
        best_threshold = 0

        n_features = X.shape[1]
        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = X[:, feature] > threshold

                if len(y[left_mask]) == 0 or len(y[right_mask]) == 0:
                    continue

                gini = self._calculate_gini(y[left_mask], y[right_mask])
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    def _calculate_gini(self, left_y, right_y):
        """计算基尼指数"""
        total = len(left_y) + len(right_y)
        gini = 0

        for y in [left_y, right_y]:
            if len(y) == 0:
                continue
            class_counts = np.bincount(y.astype(int))
            p = class_counts / len(y)
            gini += (1 - np.sum(p ** 2)) * (len(y) / total)

        return gini

    def predict(self, X):
        """
        预测类别

        Args:
            X: 特征矩阵

        Returns:
            np.ndarray: 预测类别
        """
        if not isinstance(X, np.ndarray):
            X = np.array(X)

        predictions = []
        for sample in X:
            predictions.append(self._predict_sample(sample, self.tree))

        return np.array(predictions)

    def _predict_sample(self, sample, tree):
        """预测单个样本"""
        if tree['type'] == 'leaf':
            return tree['class']

        if sample[tree['feature']] <= tree['threshold']:
            return self._predict_sample(sample, tree['left'])
        else:
            return self._predict_sample(sample, tree['right'])
