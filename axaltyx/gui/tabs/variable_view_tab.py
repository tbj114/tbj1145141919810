#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from axaltyx.gui.widgets.variable_table import VariableTable


class VariableViewTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 变量表格
        self.variable_table = VariableTable()
        layout.addWidget(self.variable_table)
