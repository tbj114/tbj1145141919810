#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AxaltyX 应用入口
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from .app import create_app
from .gui.splash_screen import SplashScreen
from .gui.main_window import MainWindow
from .gui.styles.theme_arco import apply_theme
from axaltyx.i18n import I18nManager

__version__ = "1.0.0"


def main():
    """应用主函数"""
    app = create_app(sys.argv)
    apply_theme(app)
    i18n = I18nManager()

    splash = SplashScreen()
    splash.show()

    def show_main_window():
        splash.update_progress(100, i18n.t("app.splash_ready"))
        time.sleep(0.5)
        splash.close()
        
        main_window = MainWindow()
        main_window.show()

    QTimer.singleShot(500, lambda: splash.update_progress(25, i18n.t("app.splash_init")))
    QTimer.singleShot(1000, lambda: splash.update_progress(50, i18n.t("app.splash_load_components")))
    QTimer.singleShot(1500, lambda: splash.update_progress(75, i18n.t("app.splash_init_ui")))
    QTimer.singleShot(2000, show_main_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
