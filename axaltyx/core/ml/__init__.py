#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习模块
"""

from .classification import LogisticRegression, KNearestNeighbors, DecisionTreeClassifier
from .regression import LinearRegression, RidgeRegression, KNeighborsRegressor

__all__ = [
    'LogisticRegression',
    'KNearestNeighbors',
    'DecisionTreeClassifier',
    'LinearRegression',
    'RidgeRegression',
    'KNeighborsRegressor'
]
