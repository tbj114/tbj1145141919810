#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据设置页面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout,
    QLabel, QComboBox, QCheckBox, QSpinBox
)
from axaltyx.i18n import I18nManager
from axaltyx.utils.config import ConfigManager


class DataPage(QWidget):
    """数据设置页面"""
    
    def __init__(self, parent=None):
        """
        初始化数据设置页面
        
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
        
        # 数据导入设置
        import_group = QGroupBox(self.i18n.t("settings.data_import"))
        import_layout = QVBoxLayout()
        
        # 缺失值处理
        missing_layout = QHBoxLayout()
        missing_label = QLabel(self.i18n.t("settings.missing_values"))
        missing_label.setFixedWidth(120)
        
        self.missing_combo = QComboBox()
        self.missing_combo.addItem(self.i18n.t("settings.missing_as_na"), "na")
        self.missing_combo.addItem(self.i18n.t("settings.missing_as_zero"), "zero")
        self.missing_combo.addItem(self.i18n.t("settings.missing_ignore"), "ignore")
        
        current_missing = self.config.get("missing_values", "na")
        index = self.missing_combo.findData(current_missing)
        if index != -1:
            self.missing_combo.setCurrentIndex(index)
        
        missing_layout.addWidget(missing_label)
        missing_layout.addWidget(self.missing_combo)
        missing_layout.addStretch()
        import_layout.addLayout(missing_layout)
        
        # 自动检测数据类型
        self.dtype_check = QCheckBox(self.i18n.t("settings.auto_detect_dtype"))
        self.dtype_check.setChecked(self.config.get("auto_detect_dtype", True))
        import_layout.addWidget(self.dtype_check)
        
        import_group.setLayout(import_layout)
        
        # 数据导出设置
        export_group = QGroupBox(self.i18n.t("settings.data_export"))
        export_layout = QVBoxLayout()
        
        # 导出格式设置
        format_layout = QHBoxLayout()
        format_label = QLabel(self.i18n.t("settings.export_format"))
        format_label.setFixedWidth(120)
        
        self.format_combo = QComboBox()
        self.format_combo.addItem("CSV", "csv")
        self.format_combo.addItem("Excel", "xlsx")
        self.format_combo.addItem("SPSS", "sav")
        
        current_format = self.config.get("export_format", "csv")
        index = self.format_combo.findData(current_format)
        if index != -1:
            self.format_combo.setCurrentIndex(index)
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        export_layout.addLayout(format_layout)
        
        # 导出时包含变量标签
        self.labels_check = QCheckBox(self.i18n.t("settings.include_labels"))
        self.labels_check.setChecked(self.config.get("include_labels", True))
        export_layout.addWidget(self.labels_check)
        
        export_group.setLayout(export_layout)
        
        # 数据显示设置
        display_group = QGroupBox(self.i18n.t("settings.data_display"))
        display_layout = QVBoxLayout()
        
        # 每页显示行数
        rows_layout = QHBoxLayout()
        rows_label = QLabel(self.i18n.t("settings.rows_per_page"))
        rows_label.setFixedWidth(120)
        
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(10, 100)
        self.rows_spin.setValue(self.config.get("rows_per_page", 50))
        
        rows_layout.addWidget(rows_label)
        rows_layout.addWidget(self.rows_spin)
        rows_layout.addStretch()
        display_layout.addLayout(rows_layout)
        
        # 显示网格线
        self.grid_check = QCheckBox(self.i18n.t("settings.show_grid"))
        self.grid_check.setChecked(self.config.get("show_grid", True))
        display_layout.addWidget(self.grid_check)
        
        display_group.setLayout(display_layout)
        
        # 添加到主布局
        layout.addWidget(import_group)
        layout.addWidget(export_group)
        layout.addWidget(display_group)
        layout.addStretch()
    
    def save_settings(self):
        """保存设置"""
        # 保存数据导入设置
        self.config.set("missing_values", self.missing_combo.currentData())
        self.config.set("auto_detect_dtype", self.dtype_check.isChecked())
        
        # 保存数据导出设置
        self.config.set("export_format", self.format_combo.currentData())
        self.config.set("include_labels", self.labels_check.isChecked())
        
        # 保存数据显示设置
        self.config.set("rows_per_page", self.rows_spin.value())
        self.config.set("show_grid", self.grid_check.isChecked())
        
        # 保存配置到文件
        self.config.save()
