#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt, QSize
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.i18n import I18nManager


class AboutDialog(ArcoDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "", 500, 400)
        self.i18n = I18nManager()
        self.set_title(self.i18n.t("app.app_name"))
        self._init_ui()
        self._init_bottom_buttons()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # Logo和标题
        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        app_name = QLabel(self.i18n.t("app.app_name"))
        app_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #1D2129;")
        
        version_label = QLabel("版本 1.0.0")
        version_label.setStyleSheet("font-size: 14px; color: #86909C;")
        
        title_layout.addWidget(app_name)
        title_layout.addWidget(version_label)
        
        main_layout.addLayout(title_layout)
        
        # 描述
        desc_label = QLabel(self.i18n.t("app.app_description"))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 14px; color: #4E5969;")
        main_layout.addWidget(desc_label)
        
        # 版权信息
        copyright_label = QLabel("© 2025 AxaltyX Team. All rights reserved.")
        copyright_label.setStyleSheet("font-size: 12px; color: #86909C;")
        main_layout.addWidget(copyright_label)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
    
    def _init_bottom_buttons(self):
        # 移除默认的确定和取消按钮，只添加确定按钮
        right_layout = None
        for i in range(self.button_bar.layout().count()):
            item = self.button_bar.layout().itemAt(i)
            if item and item.layout():
                layout = item.layout()
                right_layout = layout
                break
        
        if right_layout:
            while right_layout.count():
                item = right_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            ok_button = QPushButton(self.i18n.t("dialogs.common.ok"))
            ok_button.setMinimumWidth(80)
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: #165DFF;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #3B82F6;
                }
                QPushButton:pressed {
                    background-color: #1E40AF;
                }
            """)
            ok_button.clicked.connect(self.accept)
            right_layout.addWidget(ok_button)
