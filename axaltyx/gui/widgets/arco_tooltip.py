#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的工具提示
"""

from PyQt6.QtWidgets import QToolTip, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class ArcoToolTip(QWidget):
    """Arco Design 风格的工具提示基类"""
    
    @staticmethod
    def set_style():
        """设置全局 Arco Design 风格的工具提示"""
        QToolTip.setStyleSheet("""
            QToolTip {
                background-color: #272E3B;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 12px;
            }
        """)