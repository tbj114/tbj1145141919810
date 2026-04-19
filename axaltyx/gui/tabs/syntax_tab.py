#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class SyntaxTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 语法编辑器
        self.syntax_editor = QTextEdit()
        self.syntax_editor.setPlaceholderText("在此输入语法...")
        layout.addWidget(self.syntax_editor)
