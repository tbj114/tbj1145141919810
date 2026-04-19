#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T 检验模块
"""

from axaltyx.core.means.ttest_one import TTestOne
from axaltyx.core.means.ttest_independent import TTestIndependent
from axaltyx.core.means.ttest_paired import TTestPaired

__all__ = [
    'TTestOne',
    'TTestIndependent',
    'TTestPaired'
]
