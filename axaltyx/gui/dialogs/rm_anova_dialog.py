#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
重复测量方差分析对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QComboBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class RMAnovaDialog(ArcoDialog):
    """重复测量方差分析对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化重复测量方差分析对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title("重复测量方差分析")
        self.dataset = dataset
        
        # 初始化选择状态
        self.statistics_options = {
            'mean': True,
            'std_dev': True,
            'variance': True,
            'count': True,
            'standard_error': True
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
        variable_layout = QHBoxLayout()
        
        # 因变量选择
        dependent_frame = QGroupBox("因变量")
        dependent_layout = QVBoxLayout()
        self.dependent_selector = VariableSelector()
        dependent_layout.addWidget(self.dependent_selector)
        dependent_frame.setLayout(dependent_layout)
        variable_layout.addWidget(dependent_frame, 1)
        
        # 被试变量选择
        subject_frame = QGroupBox("被试变量")
        subject_layout = QVBoxLayout()
        self.subject_selector = VariableSelector()
        subject_layout.addWidget(self.subject_selector)
        subject_frame.setLayout(subject_layout)
        variable_layout.addWidget(subject_frame, 1)
        
        # 时间/条件变量选择
        within_frame = QGroupBox("时间/条件变量")
        within_layout = QVBoxLayout()
        self.within_selector = VariableSelector()
        within_layout.addWidget(self.within_selector)
        within_frame.setLayout(within_layout)
        variable_layout.addWidget(within_frame, 1)
        
        main_layout.addLayout(variable_layout, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 统计量选项
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(12)
        self._create_statistics_checkboxes(stats_layout)
        stats_widget.setLayout(stats_layout)
        options_tabs.addTab(stats_widget, self.i18n.t("dialogs.common.statistics"))
        
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
        group = QGroupBox("统计量")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        # 创建复选框
        self.check_mean = QCheckBox("均值")
        self.check_mean.setChecked(True)
        self.check_mean.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_mean)
        
        self.check_std_dev = QCheckBox("标准差")
        self.check_std_dev.setChecked(True)
        self.check_std_dev.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_std_dev)
        
        self.check_variance = QCheckBox("方差")
        self.check_variance.setChecked(True)
        self.check_variance.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_variance)
        
        self.check_count = QCheckBox("计数")
        self.check_count.setChecked(True)
        self.check_count.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_count)
        
        self.check_standard_error = QCheckBox("标准误")
        self.check_standard_error.setChecked(True)
        self.check_standard_error.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_standard_error)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def _update_statistics_options(self):
        """更新统计量选项"""
        self.statistics_options['mean'] = self.check_mean.isChecked()
        self.statistics_options['std_dev'] = self.check_std_dev.isChecked()
        self.statistics_options['variance'] = self.check_variance.isChecked()
        self.statistics_options['count'] = self.check_count.isChecked()
        self.statistics_options['standard_error'] = self.check_standard_error.isChecked()
    
    def _set_demo_data(self):
        """设置演示数据"""
        # 因变量
        dependent_variables = [
            ("PRE_TEST", "numeric"),
            ("POST_TEST", "numeric"),
            ("FOLLOW_UP", "numeric")
        ]
        self.dependent_selector.set_variables(dependent_variables)
        
        # 被试变量
        subject_variables = [
            ("SUBJECT_ID", "string"),
            ("PARTICIPANT", "string")
        ]
        self.subject_selector.set_variables(subject_variables)
        
        # 时间/条件变量
        within_variables = [
            ("TIME", "string"),
            ("CONDITION", "string")
        ]
        self.within_selector.set_variables(within_variables)
    
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
        return {
            'dependent': self.dependent_selector.get_selected_variables(),
            'subject': self.subject_selector.get_selected_variables(),
            'within': self.within_selector.get_selected_variables()
        }
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        # TODO: 实现粘贴功能
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        # 重置变量选择
        self.dependent_selector.clear()
        self.subject_selector.clear()
        self.within_selector.clear()
        self._set_demo_data()
        
        # 重置统计量选项
        self.check_mean.setChecked(True)
        self.check_std_dev.setChecked(True)
        self.check_variance.setChecked(True)
        self.check_count.setChecked(True)
        self.check_standard_error.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'rm_anova',
            'results': self.analysis_results,
            'statistics_options': self.statistics_options.copy()
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行重复测量方差分析"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        dependent_vars = selected_variables['dependent']
        subject_vars = selected_variables['subject']
        within_vars = selected_variables['within']
        
        if not dependent_vars or not subject_vars:
            return
        
        self.analysis_results = []
        
        # 对每个因变量执行分析
        for var_name, var_type in dependent_vars:
            # 只对数值变量进行分析
            if var_type != "numeric":
                continue
            
            # 获取变量数据（这里使用模拟数据）
            variable_data = self._get_variable_data(var_name, subject_vars, within_vars)
            
            if variable_data:
                # 执行统计计算
                from axaltyx.core.anova.rm_anova import RMAnova
                
                # 模拟重复测量方差分析结果
                result_table = RMAnova.create_result_table(
                    var_name, subject_vars[0][0] if subject_vars else "", 
                    within_vars[0][0] if within_vars else ""
                )
                
                self.analysis_results.append(result_table)
    
    def _get_variable_data(self, var_name, subject_vars, within_vars):
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
        
        # 添加时间效应
        if within_vars:
            # 为不同时间点添加不同的均值偏移
            data[:33] += 5  # 时间1
            data[33:66] += 10  # 时间2
            data[66:] += 15  # 时间3
        
        # 转换为列表
        return list(data)