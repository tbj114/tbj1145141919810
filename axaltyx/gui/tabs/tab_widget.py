#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签页组件
用于管理多个标签页
"""

from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from axaltyx.i18n import I18nManager


class TabWidget(QTabWidget):
    """标签页组件"""
    
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setTabsClosable(True)
        self.setMovable(True)