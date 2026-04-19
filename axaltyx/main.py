#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AxaltyX 应用入口
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from axaltyx.app import create_app
from axaltyx.gui.splash_screen import SplashScreen
from axaltyx.gui.main_window import MainWindow
from axaltyx.gui.styles.theme_arco import apply_theme
from axaltyx.i18n import I18nManager

__version__ = "1.0.0"


def main():
    """应用主函数"""
    # 添加项目根目录到路径
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 的情况
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_path)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
    
    app = create_app(sys.argv)
    apply_theme(app)
    i18n = I18nManager()

    splash = SplashScreen()
    splash.show()
    splash.update_progress(25, i18n.t("app.splash_init"))

    def show_main_window():
        splash.update_progress(50, i18n.t("app.splash_load_components"))
        QTimer.singleShot(100, lambda: splash.update_progress(75, i18n.t("app.splash_init_ui")))
        
        try:
            main_window = MainWindow()
            splash.update_progress(100, i18n.t("app.splash_ready"))
            
            def close_and_show():
                splash.close()
                main_window.show()
                main_window.raise_()
                main_window.activateWindow()
            
            QTimer.singleShot(300, close_and_show)
        except Exception as e:
            print(f"启动错误: {e}")
            splash.close()
            # 显示错误提示
            from PyQt6.QtWidgets import QMessageBox
            error_app = QApplication(sys.argv)
            QMessageBox.critical(None, "启动错误", f"程序启动失败: {str(e)}")
            sys.exit(1)

    QTimer.singleShot(500, show_main_window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
