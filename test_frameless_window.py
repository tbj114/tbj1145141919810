#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试无边框窗口
"""

import sys
from PyQt6.QtWidgets import QApplication
from axaltyx.gui.frameless_window import FramelessWindow


class TestWindow(FramelessWindow):
    """测试窗口"""
    
    def __init__(self):
        """初始化测试窗口"""
        super().__init__()
        self.set_title("Test Window - AxaltyX")
        
        # 设置窗口大小
        self.resize(800, 600)
        
        # 设置窗口位置
        self.move(100, 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
