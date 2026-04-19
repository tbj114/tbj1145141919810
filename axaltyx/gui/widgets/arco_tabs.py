#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的标签页控件
"""

from PyQt6.QtWidgets import QTabWidget, QTabBar, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from axaltyx.i18n import I18nManager


class ArcoTabBar(QTabBar):
    """Arco Design 风格的标签栏"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()
    
    def _apply_style(self):
        self.setStyleSheet("""
            QTabBar::tab {
                background-color: transparent;
                color: #4E5969;
                padding: 12px 24px;
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 14px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                color: #165DFF;
                border-bottom: 2px solid #165DFF;
            }
            QTabBar::tab:hover:!selected {
                color: #165DFF;
            }
            QTabBar::tab:disabled {
                color: #A9AEB8;
            }
        """)


class ArcoTabWidget(QTabWidget):
    """Arco Design 风格的标签页控件"""
    
    tab_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()
    
    def _init_ui(self):
        self.setTabBar(ArcoTabBar())
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                border-top: 1px solid #E5E6EB;
            }
        """)
        self.currentChanged.connect(self._on_tab_changed)
    
    def _on_tab_changed(self, index):
        self.tab_changed.emit(index)