#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from axaltyx.gui.widgets.data_table import DataTable


class DataEditorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 数据表格
        self.data_table = DataTable()
        layout.addWidget(self.data_table)
