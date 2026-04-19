#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的按钮
"""

from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from axaltyx.gui.styles.theme_arco import COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_PRIMARY_ACTIVE, COLOR_PRIMARY_LIGHT


class ArcoButton(QPushButton):
    """Arco Design 风格按钮"""

    # 按钮类型
    TYPE_DEFAULT = "default"
    TYPE_PRIMARY = "primary"
    TYPE_SUCCESS = "success"
    TYPE_WARNING = "warning"
    TYPE_DANGER = "danger"
    TYPE_LINK = "link"

    # 按钮尺寸
    SIZE_LARGE = "large"
    SIZE_DEFAULT = "default"
    SIZE_SMALL = "small"
    SIZE_MINI = "mini"

    def __init__(self, text="", parent=None, button_type=TYPE_DEFAULT, button_size=SIZE_DEFAULT, rounded=False):
        super().__init__(text, parent)
        self.button_type = button_type
        self.button_size = button_size
        self.rounded = rounded
        self._apply_style()

    def _apply_style(self):
        """应用样式"""
        colors = self._get_colors()
        size = self._get_size()

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors["bg"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: { "20px" if self.rounded else "4px" };
                padding: {size["padding"]};
                font-size: {size["font_size"]};
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors["bg_hover"]};
                border-color: {colors["border_hover"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["bg_active"]};
                border-color: {colors["border_active"]};
            }}
            QPushButton:disabled {{
                background-color: #F7F8FA;
                color: #A9AEB8;
                border-color: #E5E6EB;
            }}
        """)

    def _get_colors(self):
        """获取颜色配置"""
        if self.button_type == self.TYPE_PRIMARY:
            return {
                "bg": COLOR_PRIMARY,
                "bg_hover": COLOR_PRIMARY_HOVER,
                "bg_active": COLOR_PRIMARY_ACTIVE,
                "border": COLOR_PRIMARY,
                "border_hover": COLOR_PRIMARY_HOVER,
                "border_active": COLOR_PRIMARY_ACTIVE,
                "text": "#FFFFFF"
            }
        elif self.button_type == self.TYPE_SUCCESS:
            return {
                "bg": "#00B42A",
                "bg_hover": "#23C343",
                "bg_active": "#009A29",
                "border": "#00B42A",
                "border_hover": "#23C343",
                "border_active": "#009A29",
                "text": "#FFFFFF"
            }
        elif self.button_type == self.TYPE_WARNING:
            return {
                "bg": "#FF7D00",
                "bg_hover": "#FF9A2E",
                "bg_active": "#D16500",
                "border": "#FF7D00",
                "border_hover": "#FF9A2E",
                "border_active": "#D16500",
                "text": "#FFFFFF"
            }
        elif self.button_type == self.TYPE_DANGER:
            return {
                "bg": "#F53F3F",
                "bg_hover": "#F76560",
                "bg_active": "#CB2636",
                "border": "#F53F3F",
                "border_hover": "#F76560",
                "border_active": "#CB2636",
                "text": "#FFFFFF"
            }
        elif self.button_type == self.TYPE_LINK:
            return {
                "bg": "transparent",
                "bg_hover": COLOR_PRIMARY_LIGHT,
                "bg_active": "#E8F3FF",
                "border": "transparent",
                "border_hover": "transparent",
                "border_active": "transparent",
                "text": COLOR_PRIMARY
            }
        else:  # default
            return {
                "bg": "#FFFFFF",
                "bg_hover": COLOR_PRIMARY_LIGHT,
                "bg_active": "#E8F3FF",
                "border": "#C9CDD4",
                "border_hover": COLOR_PRIMARY,
                "border_active": COLOR_PRIMARY_ACTIVE,
                "text": "#4E5969"
            }

    def _get_size(self):
        """获取尺寸配置"""
        if self.button_size == self.SIZE_LARGE:
            return {"padding": "12px 20px", "font_size": "16px"}
        elif self.button_size == self.SIZE_SMALL:
            return {"padding": "6px 12px", "font_size": "12px"}
        elif self.button_size == self.SIZE_MINI:
            return {"padding": "4px 8px", "font_size": "12px"}
        else:  # default
            return {"padding": "8px 16px", "font_size": "14px"}

    def set_button_type(self, button_type):
        """设置按钮类型"""
        self.button_type = button_type
        self._apply_style()

    def set_button_size(self, button_size):
        """设置按钮尺寸"""
        self.button_size = button_size
        self._apply_style()

    def set_rounded(self, rounded):
        """设置圆角按钮"""
        self.rounded = rounded
        self._apply_style()
