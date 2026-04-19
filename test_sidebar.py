#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试侧边栏分析菜单树功能
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from axaltyx.gui.sidebar import SideBar
from axaltyx.gui.styles.theme_arco import ArcoTheme


class TestWindow(QMainWindow):
    """测试窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试侧边栏分析菜单树")
        self.setGeometry(100, 100, 1000, 700)

        # 应用 Arco 主题
        self.theme = ArcoTheme()
        self.theme.apply(self)

        self._init_ui()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 添加侧边栏
        self.sidebar = SideBar()
        self.sidebar.setFixedWidth(220)
        self.sidebar.item_clicked.connect(self._on_item_clicked)

        # 添加状态标签
        self.status_label = QLabel("点击菜单项进行测试...")
        self.status_label.setStyleSheet("padding: 12px; background-color: #F7F8FA;")

        # 简单的布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.status_label)

        layout.addLayout(main_layout)

    def _on_item_clicked(self, command: str):
        """处理菜单项点击事件"""
        self.status_label.setText(f"点击了命令: {command}")
        print(f"菜单命令: {command}")


def main():
    app = QApplication(sys.argv)

    window = TestWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
