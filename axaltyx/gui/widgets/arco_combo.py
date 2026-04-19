#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的组合框
"""

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt
from axaltyx.i18n import I18nManager


class ArcoComboBox(QComboBox):
    """Arco Design 风格的组合框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._apply_style()
    
    def _apply_style(self):
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #272E3B;
                border: 1px solid #C9CDD4;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                min-height: 32px;
            }
            QComboBox:hover {
                border-color: #86909C;
            }
            QComboBox:focus {
                border-color: #165DFF;
                background-color: #E8F3FF;
            }
            QComboBox:disabled {
                background-color: #F7F8FA;
                color: #A9AEB8;
                border-color: #E5E6EB;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #4E5969;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #E5E6EB;
                selection-background-color: #E8F3FF;
                selection-color: #165DFF;
                padding: 4px;
            }
        """)