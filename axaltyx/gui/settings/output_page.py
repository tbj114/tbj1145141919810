#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
输出设置页面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout,
    QLabel, QComboBox, QCheckBox, QSpinBox
)
from axaltyx.i18n import I18nManager
from axaltyx.utils.config import ConfigManager


class OutputPage(QWidget):
    """输出设置页面"""
    
    def __init__(self, parent=None):
        """
        初始化输出设置页面
        
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
        
        # 输出显示设置
        display_group = QGroupBox(self.i18n.t("settings.output_display"))
        display_layout = QVBoxLayout()
        
        # 字体大小
        font_layout = QHBoxLayout()
        font_label = QLabel(self.i18n.t("settings.font_size"))
        font_label.setFixedWidth(100)
        
        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 20)
        self.font_spin.setValue(self.config.get("output_font_size", 12))
        
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_spin)
        font_layout.addStretch()
        display_layout.addLayout(font_layout)
        
        # 显示行号
        self.line_numbers_check = QCheckBox(self.i18n.t("settings.show_line_numbers"))
        self.line_numbers_check.setChecked(self.config.get("show_line_numbers", True))
        display_layout.addWidget(self.line_numbers_check)
        
        # 自动换行
        self.word_wrap_check = QCheckBox(self.i18n.t("settings.word_wrap"))
        self.word_wrap_check.setChecked(self.config.get("word_wrap", True))
        display_layout.addWidget(self.word_wrap_check)
        
        display_group.setLayout(display_layout)
        
        # 输出格式设置
        format_group = QGroupBox(self.i18n.t("settings.output_format"))
        format_layout = QVBoxLayout()
        
        # 表格格式
        table_layout = QHBoxLayout()
        table_label = QLabel(self.i18n.t("settings.table_format"))
        table_label.setFixedWidth(100)
        
        self.table_combo = QComboBox()
        self.table_combo.addItem(self.i18n.t("settings.table_compact"), "compact")
        self.table_combo.addItem(self.i18n.t("settings.table_expanded"), "expanded")
        
        current_table = self.config.get("table_format", "compact")
        index = self.table_combo.findData(current_table)
        if index != -1:
            self.table_combo.setCurrentIndex(index)
        
        table_layout.addWidget(table_label)
        table_layout.addWidget(self.table_combo)
        table_layout.addStretch()
        format_layout.addLayout(table_layout)
        
        # 数字格式
        number_layout = QHBoxLayout()
        number_label = QLabel(self.i18n.t("settings.number_format"))
        number_label.setFixedWidth(100)
        
        self.number_combo = QComboBox()
        self.number_combo.addItem("0.00", "2")
        self.number_combo.addItem("0.000", "3")
        self.number_combo.addItem("0.0000", "4")
        
        current_number = self.config.get("number_format", "2")
        index = self.number_combo.findData(current_number)
        if index != -1:
            self.number_combo.setCurrentIndex(index)
        
        number_layout.addWidget(number_label)
        number_layout.addWidget(self.number_combo)
        number_layout.addStretch()
        format_layout.addLayout(number_layout)
        
        format_group.setLayout(format_layout)
        
        # 输出选项设置
        options_group = QGroupBox(self.i18n.t("settings.output_options"))
        options_layout = QVBoxLayout()
        
        # 自动滚动到新输出
        self.auto_scroll_check = QCheckBox(self.i18n.t("settings.auto_scroll"))
        self.auto_scroll_check.setChecked(self.config.get("auto_scroll", True))
        options_layout.addWidget(self.auto_scroll_check)
        
        # 保留历史输出
        self.keep_history_check = QCheckBox(self.i18n.t("settings.keep_history"))
        self.keep_history_check.setChecked(self.config.get("keep_history", True))
        options_layout.addWidget(self.keep_history_check)
        
        options_group.setLayout(options_layout)
        
        # 添加到主布局
        layout.addWidget(display_group)
        layout.addWidget(format_group)
        layout.addWidget(options_group)
        layout.addStretch()
    
    def save_settings(self):
        """保存设置"""
        # 保存输出显示设置
        self.config.set("output_font_size", self.font_spin.value())
        self.config.set("show_line_numbers", self.line_numbers_check.isChecked())
        self.config.set("word_wrap", self.word_wrap_check.isChecked())
        
        # 保存输出格式设置
        self.config.set("table_format", self.table_combo.currentData())
        self.config.set("number_format", self.number_combo.currentData())
        
        # 保存输出选项设置
        self.config.set("auto_scroll", self.auto_scroll_check.isChecked())
        self.config.set("keep_history", self.keep_history_check.isChecked())
        
        # 保存配置到文件
        self.config.save()
