#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的分割条
"""

from PyQt6.QtWidgets import QSplitter
from PyQt6.QtCore import Qt


class ArcoSplitter(QSplitter):
    """Arco Design 风格的分割条"""
    
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._apply_style()
    
    def _apply_style(self):
        self.setStyleSheet("""
            QSplitter::handle {
                background-color: #E5E6EB;
                width: 1px;
                height: 1px;
            }
            QSplitter::handle:hover {
                background-color: #C9CDD4;
            }
        """)