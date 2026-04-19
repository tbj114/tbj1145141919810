#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
描述性统计对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class DescriptivesDialog(ArcoDialog):
    """描述性统计对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化描述性统计对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title(self.i18n.t("dialogs.descriptives.title"))
        self.dataset = dataset
        
        # 初始化选择状态
        self.statistics_options = {
            'mean': True,
            'std_dev': True,
            'variance': True,
            'range': True,
            'min': True,
            'max': True,
            'kurtosis': True,
            'skewness': True,
            'standard_error': True
        }
        
        self.chart_options = {
            'histogram': False,
            'stem_leaf': False
        }
        
        self.analysis_results = []
        
        # 初始化UI
        self._init_ui()
        self._init_bottom_buttons()
    
    def _init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # 变量选择器
        self.variable_selector = VariableSelector()
        main_layout.addWidget(self.variable_selector, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 统计量选项
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(12)
        self._create_statistics_checkboxes(stats_layout)
        stats_widget.setLayout(stats_layout)
        options_tabs.addTab(stats_widget, self.i18n.t("dialogs.common.statistics"))
        
        # 图表选项
        chart_widget = QWidget()
        chart_layout = QVBoxLayout()
        chart_layout.setSpacing(12)
        self._create_chart_checkboxes(chart_layout)
        chart_widget.setLayout(chart_layout)
        options_tabs.addTab(chart_widget, self.i18n.t("dialogs.common.charts"))
        
        main_layout.addWidget(options_tabs, 1)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
        
        # 设置测试数据（如果没有数据集）
        if self.dataset:
            self._set_variables_from_dataset()
        else:
            self._set_demo_data()
    
    def _create_statistics_checkboxes(self, parent_layout):
        """创建统计量复选框"""
        group = QGroupBox(self.i18n.t("dialogs.descriptives.statistics_dialog_title"))
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        # 创建复选框
        self.check_mean = QCheckBox(self.i18n.t("dialogs.descriptives.mean"))
        self.check_mean.setChecked(True)
        self.check_mean.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_mean)
        
        self.check_std_dev = QCheckBox(self.i18n.t("dialogs.descriptives.std_dev"))
        self.check_std_dev.setChecked(True)
        self.check_std_dev.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_std_dev)
        
        self.check_variance = QCheckBox(self.i18n.t("dialogs.descriptives.variance"))
        self.check_variance.setChecked(True)
        self.check_variance.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_variance)
        
        self.check_range = QCheckBox(self.i18n.t("dialogs.descriptives.range"))
        self.check_range.setChecked(True)
        self.check_range.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_range)
        
        self.check_min = QCheckBox(self.i18n.t("dialogs.descriptives.minimum"))
        self.check_min.setChecked(True)
        self.check_min.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_min)
        
        self.check_max = QCheckBox(self.i18n.t("dialogs.descriptives.maximum"))
        self.check_max.setChecked(True)
        self.check_max.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_max)
        
        self.check_kurtosis = QCheckBox(self.i18n.t("dialogs.descriptives.kurtosis"))
        self.check_kurtosis.setChecked(True)
        self.check_kurtosis.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_kurtosis)
        
        self.check_skewness = QCheckBox(self.i18n.t("dialogs.descriptives.skewness"))
        self.check_skewness.setChecked(True)
        self.check_skewness.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_skewness)
        
        self.check_standard_error = QCheckBox(self.i18n.t("dialogs.descriptives.stderr"))
        self.check_standard_error.setChecked(True)
        self.check_standard_error.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_standard_error)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def _create_chart_checkboxes(self, parent_layout):
        """创建图表复选框"""
        group = QGroupBox(self.i18n.t("dialogs.common.charts"))
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        self.check_histogram = QCheckBox(self.i18n.t("dialogs.descriptives.histogram"))
        self.check_histogram.toggled.connect(self._update_chart_options)
        group_layout.addWidget(self.check_histogram)
        
        self.check_stem_leaf = QCheckBox(self.i18n.t("dialogs.descriptives.stem_leaf"))
        self.check_stem_leaf.toggled.connect(self._update_chart_options)
        group_layout.addWidget(self.check_stem_leaf)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def _update_statistics_options(self):
        """更新统计量选项"""
        self.statistics_options['mean'] = self.check_mean.isChecked()
        self.statistics_options['std_dev'] = self.check_std_dev.isChecked()
        self.statistics_options['variance'] = self.check_variance.isChecked()
        self.statistics_options['range'] = self.check_range.isChecked()
        self.statistics_options['min'] = self.check_min.isChecked()
        self.statistics_options['max'] = self.check_max.isChecked()
        self.statistics_options['kurtosis'] = self.check_kurtosis.isChecked()
        self.statistics_options['skewness'] = self.check_skewness.isChecked()
        self.statistics_options['standard_error'] = self.check_standard_error.isChecked()
    
    def _update_chart_options(self):
        """更新图表选项"""
        self.chart_options['histogram'] = self.check_histogram.isChecked()
        self.chart_options['stem_leaf'] = self.check_stem_leaf.isChecked()
    
    def _set_demo_data(self):
        """设置演示数据"""
        demo_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "numeric"),
            ("VAR00003", "numeric"),
            ("VAR00004", "string"),
            ("VAR00005", "numeric")
        ]
        self.variable_selector.set_variables(demo_variables)
    
    def _set_variables_from_dataset(self):
        """从数据集设置变量"""
        if not self.dataset:
            return
        
        # TODO: 实现从真实数据集获取变量
        self._set_demo_data()
    
    def _init_bottom_buttons(self):
        """初始化底部按钮"""
        # 移除默认的确定和取消按钮，添加粘贴、重置、确定、取消
        # 我们需要在正确的位置添加按钮
        # 获取右布局
        right_layout = None
        for i in range(self.button_bar.layout().count()):
            item = self.button_bar.layout().itemAt(i)
            if item and item.layout():
                # 查找右布局
                layout = item.layout()
                right_layout = layout
                break
        
        if right_layout:
            # 清空现有按钮并添加新按钮
            while right_layout.count():
                item = right_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # 粘贴按钮
            paste_button = QPushButton(self.i18n.t("dialogs.common.paste"))
            paste_button.setMinimumWidth(80)
            paste_button.setStyleSheet("""
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
            paste_button.clicked.connect(self._on_paste)
            right_layout.addWidget(paste_button)
            
            # 重置按钮
            reset_button = QPushButton(self.i18n.t("dialogs.common.reset"))
            reset_button.setMinimumWidth(80)
            reset_button.setStyleSheet("""
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
            reset_button.clicked.connect(self._on_reset)
            right_layout.addWidget(reset_button)
            
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
            self.ok_button = QPushButton(self.i18n.t("dialogs.common.ok"))
            self.ok_button.setMinimumWidth(80)
            self.ok_button.setStyleSheet("""
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
            self.ok_button.clicked.connect(self._on_ok)
            right_layout.addWidget(self.ok_button)
    
    def get_selected_variables(self):
        """获取选中的变量列表"""
        return self.variable_selector.get_selected_variables()
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        # TODO: 实现粘贴功能
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        # 重置变量选择
        self.variable_selector.clear()
        self._set_demo_data()
        
        # 重置统计量选项
        self.check_mean.setChecked(True)
        self.check_std_dev.setChecked(True)
        self.check_variance.setChecked(True)
        self.check_range.setChecked(True)
        self.check_min.setChecked(True)
        self.check_max.setChecked(True)
        self.check_kurtosis.setChecked(True)
        self.check_skewness.setChecked(True)
        self.check_standard_error.setChecked(True)
        
        # 重置图表选项
        self.check_histogram.setChecked(False)
        self.check_stem_leaf.setChecked(False)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'descriptives',
            'results': self.analysis_results,
            'statistics_options': self.statistics_options.copy(),
            'chart_options': self.chart_options.copy()
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行描述性统计分析"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        
        if not selected_variables:
            return
        
        self.analysis_results = []
        
        # 对每个变量执行分析
        for var_name, var_type in selected_variables:
            # 只对数值变量进行分析
            if var_type != "numeric":
                continue
            
            # 获取变量数据（这里使用模拟数据）
            variable_data = self._get_variable_data(var_name)
            
            if variable_data:
                # 执行统计计算
                from axaltyx.core.descriptive.descriptives import DescriptiveStats
                stats_result = DescriptiveStats.calculate_statistics(
                    variable_data, self.statistics_options
                )
                
                # 创建结果表格
                result_table = DescriptiveStats.create_result_table(
                    var_name, stats_result
                )
                
                self.analysis_results.append(result_table)
    
    def _get_variable_data(self, var_name):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in var_name)
        random.seed(seed)
        np.random.seed(seed)
        
        # 生成正态分布数据
        mean = 50 + (seed % 20)
        std = 10 + (seed % 5)
        data = np.random.normal(mean, std, size=100)
        
        # 转换为列表
        return list(data)
