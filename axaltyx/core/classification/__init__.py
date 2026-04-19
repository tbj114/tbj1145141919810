#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分类分析模块
"""

from .clustering import KMeans, HierarchicalClustering
from .discriminant import LinearDiscriminantAnalysis

__all__ = [
    'KMeans',
    'HierarchicalClustering',
    'LinearDiscriminantAnalysis'
]
