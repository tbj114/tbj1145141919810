#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from axaltyx.gui.widgets.output_viewer import OutputViewer


class OutputTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 输出查看器
        self.output_viewer = OutputViewer()
        layout.addWidget(self.output_viewer)
