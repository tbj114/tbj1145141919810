#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
样式包
包含主题和样式定义
"""

from .theme_arco import (
    apply_theme,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_PRIMARY_ACTIVE,
    COLOR_PRIMARY_LIGHT,
)

__all__ = [
    "apply_theme",
    "COLOR_PRIMARY",
    "COLOR_PRIMARY_HOVER",
    "COLOR_PRIMARY_ACTIVE",
    "COLOR_PRIMARY_LIGHT",
]
