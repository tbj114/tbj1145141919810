#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AxaltyX 应用入口
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from .app import create_app
from .gui.splash_screen import SplashScreen
from .gui.main_window import MainWindow
from .gui.styles.theme_arco import apply_theme

__version__ = "1.0.0"


def main():
    """应用主函数"""
    app = create_app(sys.argv)
    apply_theme(app)

    splash = SplashScreen()
    splash.show()

    def show_main_window():
        splash.update_progress(100, splash.i18n.t("app.splash_ready"))
        time.sleep(0.5)
        splash.close()
        
        main_window = MainWindow()
        main_window.show()

    QTimer.singleShot(500, lambda: splash.update_progress(25, splash.i18n.t("app.splash_init")))
    QTimer.singleShot(1000, lambda: splash.update_progress(50, "加载组件..."))
    QTimer.singleShot(1500, lambda: splash.update_progress(75, "初始化界面..."))
    QTimer.singleShot(2000, show_main_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
