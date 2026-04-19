#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自定义标题栏
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os


class TitleBar(QWidget):
    """标题栏类"""
    
    def __init__(self, parent):
        """初始化标题栏"""
        super().__init__(parent)
        self.parent = parent
        
        # 设置标题栏高度
        self.setFixedHeight(32)
        
        # 初始化布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 0, 8, 0)
        self.layout.setSpacing(8)
        
        # Logo
        self.logo_label = QLabel(self)
        # 这里可以设置实际的 Logo
        self.logo_label.setText("AxaltyX")
        self.logo_label.setStyleSheet("font-weight: 600; font-size: 14px; color: #272E3B;")
        self.layout.addWidget(self.logo_label)
        
        # 标题
        self.title_label = QLabel(self)
        self.title_label.setText("Untitled")
        self.title_label.setStyleSheet("font-size: 14px; color: #4E5969;")
        self.layout.addWidget(self.title_label)
        
        #  spacer
        self.layout.addStretch()
        
        # 最小化按钮
        self.minimize_button = QPushButton(self)
        self.minimize_button.setFixedSize(32, 32)
        self.minimize_button.setStyleSheet(self._get_button_style())
        self.minimize_button.setText("_")
        self.minimize_button.clicked.connect(self._on_minimize)
        self.layout.addWidget(self.minimize_button)
        
        # 最大化/还原按钮
        self.maximize_button = QPushButton(self)
        self.maximize_button.setFixedSize(32, 32)
        self.maximize_button.setStyleSheet(self._get_button_style())
        self.maximize_button.setText("□")
        self.maximize_button.clicked.connect(self._on_maximize)
        self.layout.addWidget(self.maximize_button)
        
        # 关闭按钮
        self.close_button = QPushButton(self)
        self.close_button.setFixedSize(32, 32)
        self.close_button.setStyleSheet(self._get_button_style() + " QPushButton:hover { background-color: #F53F3F; color: white; }")
        self.close_button.setText("×")
        self.close_button.clicked.connect(self._on_close)
        self.layout.addWidget(self.close_button)
        
        # 设置背景
        self.setStyleSheet("background-color: white; border-bottom: 1px solid #E5E6EB;")
    
    def set_title(self, title):
        """设置标题"""
        self.title_label.setText(title)
    
    def _get_button_style(self):
        """获取按钮样式"""
        return ""
    
    def _on_minimize(self):
        """最小化窗口"""
        self.parent.showMinimized()
    
    def _on_maximize(self):
        """最大化/还原窗口"""
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
    
    def _on_close(self):
        """关闭窗口"""
        self.parent.close()

