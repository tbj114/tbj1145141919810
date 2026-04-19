#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游程检验对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QComboBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class RunsDialog(ArcoDialog):
    """游程检验对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化游程检验对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title("游程检验")
        self.dataset = dataset
        
        # 初始化选择状态
        self.statistics_options = {
            'runs': True,
            'z_statistic': True,
            'p_value': True
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
        
        # 检验变量选择
        test_frame = QGroupBox("检验变量")
        test_layout = QVBoxLayout()
        self.test_selector = VariableSelector()
        test_layout.addWidget(self.test_selector)
        test_frame.setLayout(test_layout)
        variable_layout.addWidget(test_frame, 1)
        
        # 分组变量选择
        group_frame = QGroupBox("分组变量")
        group_layout = QVBoxLayout()
        self.group_selector = VariableSelector()
        group_layout.addWidget(self.group_selector)
        group_frame.setLayout(group_layout)
        variable_layout.addWidget(group_frame, 1)
        
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
        self.check_runs = QCheckBox("游程数")
        self.check_runs.setChecked(True)
        self.check_runs.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_runs)
        
        self.check_z = QCheckBox("Z统计量")
        self.check_z.setChecked(True)
        self.check_z.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_z)
        
        self.check_p_value = QCheckBox("P值")
        self.check_p_value.setChecked(True)
        self.check_p_value.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_p_value)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def _update_statistics_options(self):
        """更新统计量选项"""
        self.statistics_options['runs'] = self.check_runs.isChecked()
        self.statistics_options['z_statistic'] = self.check_z.isChecked()
        self.statistics_options['p_value'] = self.check_p_value.isChecked()
    
    def _set_demo_data(self):
        """设置演示数据"""
        # 检验变量
        test_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "numeric"),
            ("VAR00003", "numeric")
        ]
        self.test_selector.set_variables(test_variables)
        
        # 分组变量
        group_variables = [
            ("GROUP", "string"),
            ("GENDER", "string"),
            ("CATEGORY", "string")
        ]
        self.group_selector.set_variables(group_variables)
    
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
            'test': self.test_selector.get_selected_variables(),
            'group': self.group_selector.get_selected_variables()
        }
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        # TODO: 实现粘贴功能
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        # 重置变量选择
        self.test_selector.clear()
        self.group_selector.clear()
        self._set_demo_data()
        
        # 重置统计量选项
        self.check_runs.setChecked(True)
        self.check_z.setChecked(True)
        self.check_p_value.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'runs',
            'results': self.analysis_results,
            'statistics_options': self.statistics_options.copy()
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行游程检验"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        test_vars = selected_variables['test']
        group_vars = selected_variables['group']
        
        if not test_vars:
            return
        
        self.analysis_results = []
        
        # 对每个检验变量执行分析
        for var_name, var_type in test_vars:
            # 只对数值变量进行分析
            if var_type != "numeric":
                continue
            
            # 获取变量数据（这里使用模拟数据）
            variable_data = self._get_variable_data(var_name, group_vars)
            
            if variable_data:
                # 执行统计计算
                from axaltyx.core.nonparametric.runs import RunsTest
                
                # 模拟游程检验结果
                result_table = RunsTest.create_result_table(
                    var_name
                )
                
                self.analysis_results.append(result_table)
    
    def _get_variable_data(self, var_name, group_vars):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in var_name)
        random.seed(seed)
        np.random.seed(seed)
        
        # 生成二分类数据
        data = np.random.randint(0, 2, size=100)
        
        # 转换为列表
        return list(data)