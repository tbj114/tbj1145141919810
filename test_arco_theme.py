#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 Arco Design 主题
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QComboBox, QCheckBox, QRadioButton,
    QTabWidget, QWidget, QLabel, QFrame
)


class ThemeTestWindow(QMainWindow):
    """主题测试窗口"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Arco Design 主题测试")
        self.setMinimumSize(800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)
        
        # 添加标题
        title_label = QLabel("Arco Design QSS 主题系统测试")
        title_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #1D2129;")
        main_layout.addWidget(title_label)
        
        # 分割线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(separator)
        
        # 按钮测试区域
        button_section = QLabel("按钮样式测试")
        button_section.setStyleSheet("font-size: 16px; font-weight: 500; color: #272E3B; margin-top: 8px;")
        main_layout.addWidget(button_section)
        
        # 按钮布局 - 按类型分组
        button_types_layout = QVBoxLayout()
        
        # Primary 按钮
        primary_layout = QHBoxLayout()
        primary_label = QLabel("Primary:")
        primary_layout.addWidget(primary_label)
        
        primary_mini = QPushButton("Mini")
        primary_mini.setProperty("class", "primary")
        primary_mini.setProperty("size", "mini")
        primary_layout.addWidget(primary_mini)
        
        primary_small = QPushButton("Small")
        primary_small.setProperty("class", "primary")
        primary_small.setProperty("size", "small")
        primary_layout.addWidget(primary_small)
        
        primary_default = QPushButton("Default")
        primary_default.setProperty("class", "primary")
        primary_default.setProperty("size", "default")
        primary_layout.addWidget(primary_default)
        
        primary_large = QPushButton("Large")
        primary_large.setProperty("class", "primary")
        primary_large.setProperty("size", "large")
        primary_layout.addWidget(primary_large)
        
        primary_layout.addStretch()
        button_types_layout.addLayout(primary_layout)
        
        # Secondary 按钮
        secondary_layout = QHBoxLayout()
        secondary_label = QLabel("Secondary:")
        secondary_layout.addWidget(secondary_label)
        
        secondary_mini = QPushButton("Mini")
        secondary_mini.setProperty("class", "secondary")
        secondary_mini.setProperty("size", "mini")
        secondary_layout.addWidget(secondary_mini)
        
        secondary_small = QPushButton("Small")
        secondary_small.setProperty("class", "secondary")
        secondary_small.setProperty("size", "small")
        secondary_layout.addWidget(secondary_small)
        
        secondary_default = QPushButton("Default")
        secondary_default.setProperty("class", "secondary")
        secondary_default.setProperty("size", "default")
        secondary_layout.addWidget(secondary_default)
        
        secondary_large = QPushButton("Large")
        secondary_large.setProperty("class", "secondary")
        secondary_large.setProperty("size", "large")
        secondary_layout.addWidget(secondary_large)
        
        secondary_layout.addStretch()
        button_types_layout.addLayout(secondary_layout)
        
        # Outline 按钮
        outline_layout = QHBoxLayout()
        outline_label = QLabel("Outline:")
        outline_layout.addWidget(outline_label)
        
        outline_mini = QPushButton("Mini")
        outline_mini.setProperty("class", "outline")
        outline_mini.setProperty("size", "mini")
        outline_layout.addWidget(outline_mini)
        
        outline_small = QPushButton("Small")
        outline_small.setProperty("class", "outline")
        outline_small.setProperty("size", "small")
        outline_layout.addWidget(outline_small)
        
        outline_default = QPushButton("Default")
        outline_default.setProperty("class", "outline")
        outline_default.setProperty("size", "default")
        outline_layout.addWidget(outline_default)
        
        outline_large = QPushButton("Large")
        outline_large.setProperty("class", "outline")
        outline_large.setProperty("size", "large")
        outline_layout.addWidget(outline_large)
        
        outline_layout.addStretch()
        button_types_layout.addLayout(outline_layout)
        
        # Text 按钮
        text_layout = QHBoxLayout()
        text_label = QLabel("Text:")
        text_layout.addWidget(text_label)
        
        text_mini = QPushButton("Mini")
        text_mini.setProperty("class", "text")
        text_mini.setProperty("size", "mini")
        text_layout.addWidget(text_mini)
        
        text_small = QPushButton("Small")
        text_small.setProperty("class", "text")
        text_small.setProperty("size", "small")
        text_layout.addWidget(text_small)
        
        text_default = QPushButton("Default")
        text_default.setProperty("class", "text")
        text_default.setProperty("size", "default")
        text_layout.addWidget(text_default)
        
        text_large = QPushButton("Large")
        text_large.setProperty("class", "text")
        text_large.setProperty("size", "large")
        text_layout.addWidget(text_large)
        
        text_layout.addStretch()
        button_types_layout.addLayout(text_layout)
        
        main_layout.addLayout(button_types_layout)
        
        # 输入框测试区域
        input_section = QLabel("输入框测试")
        input_section.setStyleSheet("font-size: 16px; font-weight: 500; color: #272E3B; margin-top: 16px;")
        main_layout.addWidget(input_section)
        
        input_layout = QHBoxLayout()
        
        normal_input = QLineEdit()
        normal_input.setPlaceholderText("正常输入框")
        input_layout.addWidget(normal_input)
        
        disabled_input = QLineEdit()
        disabled_input.setPlaceholderText("禁用输入框")
        disabled_input.setEnabled(False)
        input_layout.addWidget(disabled_input)
        
        main_layout.addLayout(input_layout)
        
        # 下拉框测试区域
        combo_section = QLabel("下拉框测试")
        combo_section.setStyleSheet("font-size: 16px; font-weight: 500; color: #272E3B; margin-top: 16px;")
        main_layout.addWidget(combo_section)
        
        combo_layout = QHBoxLayout()
        
        normal_combo = QComboBox()
        normal_combo.addItems(["选项1", "选项2", "选项3"])
        combo_layout.addWidget(normal_combo)
        
        disabled_combo = QComboBox()
        disabled_combo.addItems(["选项1", "选项2", "选项3"])
        disabled_combo.setEnabled(False)
        combo_layout.addWidget(disabled_combo)
        
        main_layout.addLayout(combo_layout)
        
        # 复选框和单选框测试
        check_section = QLabel("复选框和单选框测试")
        check_section.setStyleSheet("font-size: 16px; font-weight: 500; color: #272E3B; margin-top: 16px;")
        main_layout.addWidget(check_section)
        
        check_layout = QHBoxLayout()
        
        check1 = QCheckBox("复选框1")
        check_layout.addWidget(check1)
        
        check2 = QCheckBox("复选框2")
        check2.setChecked(True)
        check_layout.addWidget(check2)
        
        check3 = QCheckBox("禁用复选框")
        check3.setEnabled(False)
        check_layout.addWidget(check3)
        
        radio1 = QRadioButton("单选框1")
        check_layout.addWidget(radio1)
        
        radio2 = QRadioButton("单选框2")
        radio2.setChecked(True)
        check_layout.addWidget(radio2)
        
        radio3 = QRadioButton("禁用单选框")
        radio3.setEnabled(False)
        check_layout.addWidget(radio3)
        
        check_layout.addStretch()
        main_layout.addLayout(check_layout)
        
        # 标签页测试
        tab_section = QLabel("标签页测试")
        tab_section.setStyleSheet("font-size: 16px; font-weight: 500; color: #272E3B; margin-top: 16px;")
        main_layout.addWidget(tab_section)
        
        tab_widget = QTabWidget()
        
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("这是标签页1的内容"))
        tab_widget.addTab(tab1, "标签页1")
        
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(QLabel("这是标签页2的内容"))
        tab_widget.addTab(tab2, "标签页2")
        
        tab3 = QWidget()
        tab3_layout = QVBoxLayout(tab3)
        tab3_layout.addWidget(QLabel("这是标签页3的内容"))
        tab_widget.addTab(tab3, "标签页3")
        
        main_layout.addWidget(tab_widget)
        
        # 添加弹性空间
        main_layout.addStretch()


def apply_stylesheet(app):
    """应用主题样式"""
    # 加载全局样式
    global_style = ""
    widgets_style = ""
    
    try:
        with open("axaltyx/gui/styles/global.qss", "r", encoding="utf-8") as f:
            global_style = f.read()
    except FileNotFoundError:
        print("警告: global.qss 文件未找到")
    
    try:
        with open("axaltyx/gui/styles/widgets.qss", "r", encoding="utf-8") as f:
            widgets_style = f.read()
    except FileNotFoundError:
        print("警告: widgets.qss 文件未找到")
    
    # 应用样式
    app.setStyleSheet(global_style + widgets_style)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 应用主题
    apply_stylesheet(app)
    
    # 创建并显示测试窗口
    window = ThemeTestWindow()
    window.show()
    
    sys.exit(app.exec())
