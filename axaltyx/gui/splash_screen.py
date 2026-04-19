#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
启动页面
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QFont
import os


class SplashScreen(QWidget):
    """启动页面类"""
    
    def __init__(self):
        """初始化启动页面"""
        super().__init__()
        
        # 设置无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 设置窗口大小
        self.setFixedSize(600, 400)
        
        # 居中显示
        self._center()
        
        # 初始化布局
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        
        # Logo
        self.logo_label = QLabel(self)
        # 这里可以设置实际的 Logo SVG
        self.logo_label.setText("AxaltyX")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("font-size: 48px; font-weight: 600; color: #165DFF;")
        self.layout.addWidget(self.logo_label)
        
        # 版本号
        self.version_label = QLabel(self)
        self.version_label.setText("v1.0.0 (Build 1)")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("font-size: 12px; color: #86909C;")
        self.layout.addWidget(self.version_label)
        
        # 进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedWidth(400)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        # 设置 Arco Blue 渐变样式
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 2px;
                background-color: #E8F3FF;
            }
            QProgressBar::chunk {
                border-radius: 2px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #165DFF, stop:1 #4080FF);
            }
        """)
        self.layout.addWidget(self.progress_bar)
        
        # 版权文字
        self.copyright_label = QLabel(self)
        self.copyright_label.setText("Copyright TBJ114. All rights reserved.")
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setStyleSheet("font-size: 12px; color: #86909C;")
        self.layout.addWidget(self.copyright_label)
        
        # 进度更新定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_progress)
        self.progress = 0
    
    def show(self):
        """显示启动页面并开始动画"""
        super().show()
        self.timer.start(15)  # 15ms 间隔，1.5秒完成 100% 进度
    
    def _center(self):
        """居中显示窗口"""
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)
    
    def _update_progress(self):
        """更新进度条"""
        self.progress += 1
        if self.progress <= 100:
            self.progress_bar.setValue(self.progress)
        else:
            self.timer.stop()
            self.close()
    
    def set_progress(self, value):
        """设置进度（外部调用）"""
        if 0 <= value <= 100:
            self.progress = value
            self.progress_bar.setValue(value)
            if value >= 100:
                self.timer.stop()
                self.close()
    
    def update_progress(self, value, message=None):
        """更新进度（外部调用，带消息）"""
        if 0 <= value <= 100:
            self.progress = value
            self.progress_bar.setValue(value)
            if value >= 100:
                self.timer.stop()
                self.close()

