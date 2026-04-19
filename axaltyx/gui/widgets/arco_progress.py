#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的进度条
"""

from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import Qt


class ArcoProgressBar(QProgressBar):
    """Arco Design 风格的进度条"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()
    
    def _apply_style(self):
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #E5E6EB;
                border-radius: 4px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #165DFF;
                border-radius: 4px;
            }
            QProgressBar::chunk:hover {
                background-color: #4080FF;
            }
        """)