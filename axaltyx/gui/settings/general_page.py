#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
通用设置页面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout,
    QLabel, QComboBox, QCheckBox
)
from axaltyx.i18n import I18nManager
from axaltyx.utils.config import ConfigManager


class GeneralPage(QWidget):
    """通用设置页面"""
    
    def __init__(self, parent=None):
        """
        初始化通用设置页面
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.i18n = I18nManager()
        self.config = ConfigManager()
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 语言设置
        language_group = QGroupBox(self.i18n.t("settings.language"))
        language_layout = QHBoxLayout()
        language_layout.setSpacing(10)
        
        language_label = QLabel(self.i18n.t("settings.language_select"))
        language_label.setFixedWidth(100)
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("中文", "zh_CN")
        self.language_combo.addItem("English", "en_US")
        self.language_combo.addItem("日本語", "ja_JP")
        
        # 从配置中加载当前语言
        current_language = self.config.get("language", "zh_CN")
        index = self.language_combo.findData(current_language)
        if index != -1:
            self.language_combo.setCurrentIndex(index)
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        language_group.setLayout(language_layout)
        
        # 界面设置
        interface_group = QGroupBox(self.i18n.t("settings.interface"))
        interface_layout = QVBoxLayout()
        
        # 启动时显示欢迎屏幕
        self.welcome_check = QCheckBox(self.i18n.t("settings.show_welcome"))
        self.welcome_check.setChecked(self.config.get("show_welcome", True))
        interface_layout.addWidget(self.welcome_check)
        
        # 自动保存
        self.auto_save_check = QCheckBox(self.i18n.t("settings.auto_save"))
        self.auto_save_check.setChecked(self.config.get("auto_save", False))
        interface_layout.addWidget(self.auto_save_check)
        
        interface_group.setLayout(interface_layout)
        
        # 数据设置
        data_group = QGroupBox(self.i18n.t("settings.data"))
        data_layout = QVBoxLayout()
        
        # 记住最近打开的文件
        self.recent_files_check = QCheckBox(self.i18n.t("settings.remember_recent_files"))
        self.recent_files_check.setChecked(self.config.get("remember_recent_files", True))
        data_layout.addWidget(self.recent_files_check)
        
        data_group.setLayout(data_layout)
        
        # 添加到主布局
        layout.addWidget(language_group)
        layout.addWidget(interface_group)
        layout.addWidget(data_group)
        layout.addStretch()
    
    def save_settings(self):
        """保存设置"""
        # 保存语言设置
        language = self.language_combo.currentData()
        self.config.set("language", language)
        
        # 保存界面设置
        self.config.set("show_welcome", self.welcome_check.isChecked())
        self.config.set("auto_save", self.auto_save_check.isChecked())
        
        # 保存数据设置
        self.config.set("remember_recent_files", self.recent_files_check.isChecked())
        
        # 保存配置到文件
        self.config.save()
