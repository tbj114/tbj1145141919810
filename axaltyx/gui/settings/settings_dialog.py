#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设置对话框实现
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QWidget
)
from PyQt6.QtCore import Qt
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.i18n import I18nManager
from .general_page import GeneralPage
from .data_page import DataPage
from .output_page import OutputPage
from .chart_page import ChartPage
from .performance_page import PerformancePage


class SettingsDialog(ArcoDialog):
    """设置对话框"""
    
    def __init__(self, parent=None):
        """
        初始化设置对话框
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent, "", 800, 600)
        self.i18n = I18nManager()
        self.set_title(self.i18n.t("settings.title"))
        
        # 初始化设置页面
        self._init_pages()
        
        # 初始化UI
        self._init_ui()
        
        # 初始化底部按钮
        self._init_bottom_buttons()
    
    def _init_pages(self):
        """初始化设置页面"""
        self.general_page = GeneralPage()
        self.data_page = DataPage()
        self.output_page = OutputPage()
        self.chart_page = ChartPage()
        self.performance_page = PerformancePage()
    
    def _init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.general_page, self.i18n.t("settings.general"))
        self.tab_widget.addTab(self.data_page, self.i18n.t("settings.data"))
        self.tab_widget.addTab(self.output_page, self.i18n.t("settings.output"))
        self.tab_widget.addTab(self.chart_page, self.i18n.t("settings.chart"))
        self.tab_widget.addTab(self.performance_page, self.i18n.t("settings.performance"))
        
        main_layout.addWidget(self.tab_widget)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
    
    def _init_bottom_buttons(self):
        """初始化底部按钮"""
        # 移除默认的确定和取消按钮，添加应用、确定、取消按钮
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
            
            # 应用按钮
            apply_button = QPushButton(self.i18n.t("dialogs.common.apply"))
            apply_button.setMinimumWidth(80)
            apply_button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #D1D5DB;
                    border-radius: 4px;
                    padding: 8px 16px;
                    color: #4B5563;
                    font-size: 14px;
                }
                QPushButton:hover {
                    border-color: #9CA3AF;
                }
                QPushButton:pressed {
                    background-color: #F3F4F6;
                }
            """)
            apply_button.clicked.connect(self._on_apply)
            right_layout.addWidget(apply_button)
            
            # 取消按钮
            cancel_button = QPushButton(self.i18n.t("dialogs.common.cancel"))
            cancel_button.setMinimumWidth(80)
            cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #D1D5DB;
                    border-radius: 4px;
                    padding: 8px 16px;
                    color: #4B5563;
                    font-size: 14px;
                }
                QPushButton:hover {
                    border-color: #9CA3AF;
                }
                QPushButton:pressed {
                    background-color: #F3F4F6;
                }
            """)
            cancel_button.clicked.connect(self.reject)
            right_layout.addWidget(cancel_button)
            
            # 确定按钮
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
            ok_button.clicked.connect(self._on_ok)
            right_layout.addWidget(ok_button)
    
    def _on_apply(self):
        """应用按钮点击事件"""
        # 保存所有页面的设置
        self.general_page.save_settings()
        self.data_page.save_settings()
        self.output_page.save_settings()
        self.chart_page.save_settings()
        self.performance_page.save_settings()
        
        # 显示保存成功消息
        from axaltyx.gui.widgets.arco_messagebox import ArcoMessageBox
        ArcoMessageBox.information(self, "成功", "设置已应用")
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 应用设置
        self._on_apply()
        
        # 关闭对话框
        self.accept()
