#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
非参数检验模块
"""

from .wilcoxon import WilcoxonSignedRank
from .mannwhitney import MannWhitneyU
from .kruskal import KruskalWallis
from .friedman import FriedmanTest
from .sign import SignTest
from .runs import RunsTest

__all__ = [
    'WilcoxonSignedRank',
    'MannWhitneyU',
    'KruskalWallis',
    'FriedmanTest',
    'SignTest',
    'RunsTest'
]
