#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的输入框
"""

from PyQt6.QtWidgets import QLineEdit, QWidget
from PyQt6.QtCore import Qt
from axaltyx.gui.styles.theme_arco import COLOR_PRIMARY, COLOR_PRIMARY_LIGHT


class ArcoInput(QLineEdit):
    """Arco Design 风格输入框"""

    # 尺寸
    SIZE_LARGE = "large"
    SIZE_DEFAULT = "default"
    SIZE_SMALL = "small"

    def __init__(self, parent=None, placeholder="", button_size=SIZE_DEFAULT):
        super().__init__(parent)
        self.placeholder = placeholder
        self.button_size = button_size
        self._apply_style()
        self.setPlaceholderText(placeholder)

    def _apply_style(self):
        """应用样式"""
        size = self._get_size()

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: #FFFFFF;
                color: #272E3B;
                border: 1px solid #C9CDD4;
                border-radius: 4px;
                padding: {size["padding"]};
                font-size: {size["font_size"]};
            }}
            QLineEdit:hover {{
                border-color: {COLOR_PRIMARY};
            }}
            QLineEdit:focus {{
                border-color: {COLOR_PRIMARY};
                background-color: {COLOR_PRIMARY_LIGHT};
            }}
            QLineEdit:disabled {{
                background-color: #F7F8FA;
                color: #A9AEB8;
                border-color: #E5E6EB;
            }}
        """)

    def _get_size(self):
        """获取尺寸配置"""
        if self.button_size == self.SIZE_LARGE:
            return {"padding": "12px 16px", "font_size": "16px"}
        elif self.button_size == self.SIZE_SMALL:
            return {"padding": "6px 12px", "font_size": "12px"}
        else:  # default
            return {"padding": "8px 12px", "font_size": "14px"}
