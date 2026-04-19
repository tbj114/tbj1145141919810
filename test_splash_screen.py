#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试启动页面
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from axaltyx.gui.splash_screen import SplashScreen
from axaltyx.gui.frameless_window import FramelessWindow


class TestWindow(FramelessWindow):
    """测试窗口"""
    
    def __init__(self):
        """初始化测试窗口"""
        super().__init__()
        self.set_title("AxaltyX - 个人学术科研专用统计软件")
        
        # 设置窗口大小
        self.resize(1024, 768)
        
        # 设置窗口位置
        self.move(100, 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 显示启动页面
    splash = SplashScreen()
    splash.show()
    
    # 启动页面结束后显示主窗口
    def show_main_window():
        window = TestWindow()
        window.show()
    
    # 1.5秒后显示主窗口
    QTimer.singleShot(1500, show_main_window)
    
    sys.exit(app.exec())
