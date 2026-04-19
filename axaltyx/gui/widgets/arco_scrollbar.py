#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的滚动条
"""

from PyQt6.QtWidgets import QScrollBar
from PyQt6.QtCore import Qt


class ArcoScrollBar(QScrollBar):
    """Arco Design 风格的滚动条"""
    
    def __init__(self, orientation=Qt.Orientation.Vertical, parent=None):
        super().__init__(orientation, parent)
        self._apply_style()
    
    def _apply_style(self):
        self.setStyleSheet("""
            QScrollBar:vertical {
                background-color: #F7F8FA;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #C9CDD4;
                min-height: 24px;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #86909C;
            }
            QScrollBar::handle:vertical:pressed {
                background-color: #4E5969;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background-color: #F7F8FA;
                height: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background-color: #C9CDD4;
                min-width: 24px;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #86909C;
            }
            QScrollBar::handle:horizontal:pressed {
                background-color: #4E5969;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)