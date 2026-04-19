#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arco Design 主题常量定义
"""

import os

# 主色调
COLOR_PRIMARY = "#165DFF"
COLOR_PRIMARY_HOVER = "#4080FF"
COLOR_PRIMARY_ACTIVE = "#0E42D2"
COLOR_PRIMARY_LIGHT = "#E8F3FF"

# 中性色
COLOR_GRAY_1 = "#F7F8FA"
COLOR_GRAY_2 = "#F2F3F5"
COLOR_GRAY_3 = "#E5E6EB"
COLOR_GRAY_4 = "#C9CDD4"
COLOR_GRAY_5 = "#A9AEB8"
COLOR_GRAY_6 = "#86909C"
COLOR_GRAY_7 = "#6B7785"
COLOR_GRAY_8 = "#4E5969"
COLOR_GRAY_9 = "#272E3B"
COLOR_GRAY_10 = "#1D2129"

# 功能色
COLOR_SUCCESS = "#00B42A"
COLOR_WARNING = "#FF7D00"
COLOR_DANGER = "#F53F3F"
COLOR_LINK = "#165DFF"

# 数据可视化色板
COLORS_VIZ = [
    "#165DFF", "#F53F3F", "#00B42A", "#3491FA",
    "#F5319D", "#722ED1", "#F77234", "#FADC19",
    "#14C9C9", "#9FDB1D"
]

# 字体
FONT_FAMILY = "'Nunito', 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif"
FONT_SIZE_CAPTION = "12px"
FONT_SIZE_BODY = "14px"
FONT_SIZE_SUBTITLE = "16px"
FONT_SIZE_TITLE = "20px"
FONT_SIZE_LARGE = "24px"
FONT_SIZE_HUGE = "36px"

# 字重
FONT_WEIGHT_REGULAR = "400"
FONT_WEIGHT_MEDIUM = "500"
FONT_WEIGHT_SEMIBOLD = "600"

# 间距
SPACING_MINI = "4px"
SPACING_SMALL = "8px"
SPACING_MEDIUM = "16px"
SPACING_LARGE = "24px"

# 圆角
RADIUS_NONE = "0px"
RADIUS_SMALL = "2px"
RADIUS_MEDIUM = "4px"
RADIUS_LARGE = "8px"
RADIUS_CIRCLE = "50%"

# 阴影
SHADOW_1 = "0 -2px 5px rgba(0,0,0,0.1)"
SHADOW_2 = "0 0 10px rgba(0,0,0,0.1)"
SHADOW_3 = "0 0 20px rgba(0,0,0,0.1)"

# 按钮尺寸
BUTTON_HEIGHT_MINI = "24px"
BUTTON_HEIGHT_SMALL = "28px"
BUTTON_HEIGHT_DEFAULT = "32px"
BUTTON_HEIGHT_LARGE = "36px"


def apply_theme(widget):
    """将 Arco Design 主题应用到控件"""
    from PyQt6.QtWidgets import QApplication
    
    styles_dir = os.path.dirname(os.path.abspath(__file__))
    global_style_path = os.path.join(styles_dir, "global.qss")
    widgets_style_path = os.path.join(styles_dir, "widgets.qss")
    
    stylesheet = ""
    if os.path.exists(global_style_path):
        with open(global_style_path, "r", encoding="utf-8") as f:
            stylesheet += f.read()
    
    if os.path.exists(widgets_style_path):
        with open(widgets_style_path, "r", encoding="utf-8") as f:
            stylesheet += f.read()
    
    QApplication.setStyleSheet(stylesheet)
