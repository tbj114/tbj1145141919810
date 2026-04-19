#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方差分析模块
"""

from axaltyx.core.anova.oneway import OneWayANOVA
from axaltyx.core.anova.manova import MANOVA
from axaltyx.core.anova.ancova import ANCOVA
from axaltyx.core.anova.rm_anova import RMANOVA

__all__ = [
    'OneWayANOVA',
    'MANOVA',
    'ANCOVA',
    'RMANOVA'
]
