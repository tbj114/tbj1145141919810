#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回归分析模块
"""

from axaltyx.core.regression.linear import SimpleLinearRegression
from axaltyx.core.regression.multiple import MultipleLinearRegression
from axaltyx.core.regression.logistic import LogisticRegression

__all__ = [
    'SimpleLinearRegression',
    'MultipleLinearRegression',
    'LogisticRegression'
]
