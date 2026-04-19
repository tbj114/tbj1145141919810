#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多个独立样本检验对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QComboBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class KIndependentDialog(ArcoDialog):
    """多个独立样本检验对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化多个独立样本检验对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title("多个独立样本检验")
        self.dataset = dataset
        
        # 初始化选择状态
        self.statistics_options = {
            'f_statistic': True,
            'df_between': True,
            'df_within': True,
            'df_total': True,
            'p_value': True
        }
        
        self.test_type = "anova"  # 默认检验类型
        
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
        
        # 因子变量选择
        factor_frame = QGroupBox("因子变量")
        factor_layout = QVBoxLayout()
        self.factor_selector = VariableSelector()
        factor_layout.addWidget(self.factor_selector)
        factor_frame.setLayout(factor_layout)
        variable_layout.addWidget(factor_frame, 1)
        
        main_layout.addLayout(variable_layout, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 检验选项
        test_widget = QWidget()
        test_layout = QVBoxLayout()
        test_layout.setSpacing(12)
        
        # 检验类型选择
        test_type_group = QGroupBox("检验类型")
        test_type_layout = QVBoxLayout()
        
        self.test_type_combo = QComboBox()
        self.test_type_combo.addItems(["单因素方差分析", "Kruskal-Wallis检验"])
        self.test_type_combo.currentIndexChanged.connect(self._update_test_type)
        test_type_layout.addWidget(self.test_type_combo)
        
        test_type_group.setLayout(test_type_layout)
        test_layout.addWidget(test_type_group)
        
        # 统计量选项
        stats_group = QGroupBox("统计量")
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(10)
        
        self.check_f_stat = QCheckBox("F统计量")
        self.check_f_stat.setChecked(True)
        self.check_f_stat.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_f_stat)
        
        self.check_df_between = QCheckBox("组间自由度")
        self.check_df_between.setChecked(True)
        self.check_df_between.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_df_between)
        
        self.check_df_within = QCheckBox("组内自由度")
        self.check_df_within.setChecked(True)
        self.check_df_within.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_df_within)
        
        self.check_df_total = QCheckBox("总自由度")
        self.check_df_total.setChecked(True)
        self.check_df_total.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_df_total)
        
        self.check_p_value = QCheckBox("P值")
        self.check_p_value.setChecked(True)
        self.check_p_value.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_p_value)
        
        stats_group.setLayout(stats_layout)
        test_layout.addWidget(stats_group)
        
        test_widget.setLayout(test_layout)
        options_tabs.addTab(test_widget, "检验选项")
        
        main_layout.addWidget(options_tabs, 1)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
        
        # 设置测试数据（如果没有数据集）
        if self.dataset:
            self._set_variables_from_dataset()
        else:
            self._set_demo_data()
    
    def _update_test_type(self, index):
        """更新检验类型"""
        test_types = ["anova", "kruskal-wallis"]
        self.test_type = test_types[index]
    
    def _update_statistics_options(self):
        """更新统计量选项"""
        self.statistics_options['f_statistic'] = self.check_f_stat.isChecked()
        self.statistics_options['df_between'] = self.check_df_between.isChecked()
        self.statistics_options['df_within'] = self.check_df_within.isChecked()
        self.statistics_options['df_total'] = self.check_df_total.isChecked()
        self.statistics_options['p_value'] = self.check_p_value.isChecked()
    
    def _set_demo_data(self):
        """设置演示数据"""
        # 因变量
        dependent_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "numeric"),
            ("VAR00003", "numeric")
        ]
        self.dependent_selector.set_variables(dependent_variables)
        
        # 因子变量
        factor_variables = [
            ("GROUP", "string"),
            ("GENDER", "string"),
            ("AGE_GROUP", "string")
        ]
        self.factor_selector.set_variables(factor_variables)
    
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
            'factor': self.factor_selector.get_selected_variables(),
            'test_type': self.test_type
        }
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        # TODO: 实现粘贴功能
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        # 重置变量选择
        self.dependent_selector.clear()
        self.factor_selector.clear()
        self._set_demo_data()
        
        # 重置检验类型
        self.test_type_combo.setCurrentIndex(0)
        
        # 重置统计量选项
        self.check_f_stat.setChecked(True)
        self.check_df_between.setChecked(True)
        self.check_df_within.setChecked(True)
        self.check_df_total.setChecked(True)
        self.check_p_value.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'k_independent',
            'results': self.analysis_results,
            'statistics_options': self.statistics_options.copy(),
            'test_type': self.test_type
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行多个独立样本检验"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        dependent_vars = selected_variables['dependent']
        factor_vars = selected_variables['factor']
        test_type = selected_variables['test_type']
        
        if not dependent_vars or not factor_vars:
            return
        
        self.analysis_results = []
        
        # 对每个因变量执行分析
        for var_name, var_type in dependent_vars:
            # 只对数值变量进行分析
            if var_type != "numeric":
                continue
            
            # 获取变量数据（这里使用模拟数据）
            variable_data = self._get_variable_data(var_name, factor_vars)
            
            if variable_data:
                # 执行统计计算
                if test_type == "anova":
                    from axaltyx.core.anova.oneway import OneWayANOVA
                    result_table = OneWayANOVA.create_result_table(
                        var_name, factor_vars[0][0] if factor_vars else ""
                    )
                else:
                    from axaltyx.core.nonparametric.kruskal import KruskalTest
                    result_table = KruskalTest.create_result_table(
                        var_name, factor_vars[0][0] if factor_vars else ""
                    )
                
                self.analysis_results.append(result_table)
    
    def _get_variable_data(self, var_name, factor_vars):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in var_name)
        random.seed(seed)
        np.random.seed(seed)
        
        # 生成三组正态分布数据，有不同的均值
        group1 = np.random.normal(50, 10, size=30)
        group2 = np.random.normal(55, 10, size=30)
        group3 = np.random.normal(60, 10, size=30)
        
        # 合并数据
        data = np.concatenate([group1, group2, group3])
        
        # 转换为列表
        return list(data)