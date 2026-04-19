#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试主窗口
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from axaltyx.app import create_app
from axaltyx.gui.main_window import MainWindow
from axaltyx.gui.styles.theme_arco import apply_theme


def main():
    app = create_app(sys.argv)
    apply_theme(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
