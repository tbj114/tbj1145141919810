#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
两个相关样本检验对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QComboBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class TwoRelatedDialog(ArcoDialog):
    """两个相关样本检验对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化两个相关样本检验对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title("两个相关样本检验")
        self.dataset = dataset
        
        # 初始化选择状态
        self.statistics_options = {
            'mean_difference': True,
            'std_error': True,
            't_statistic': True,
            'df': True,
            'p_value': True
        }
        
        self.test_type = "paired-t"  # 默认检验类型
        
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
        
        # 前测变量选择
        pre_frame = QGroupBox("前测变量")
        pre_layout = QVBoxLayout()
        self.pre_selector = VariableSelector()
        pre_layout.addWidget(self.pre_selector)
        pre_frame.setLayout(pre_layout)
        variable_layout.addWidget(pre_frame, 1)
        
        # 后测变量选择
        post_frame = QGroupBox("后测变量")
        post_layout = QVBoxLayout()
        self.post_selector = VariableSelector()
        post_layout.addWidget(self.post_selector)
        post_frame.setLayout(post_layout)
        variable_layout.addWidget(post_frame, 1)
        
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
        self.test_type_combo.addItems(["配对样本t检验", "Wilcoxon符号秩检验"])
        self.test_type_combo.currentIndexChanged.connect(self._update_test_type)
        test_type_layout.addWidget(self.test_type_combo)
        
        test_type_group.setLayout(test_type_layout)
        test_layout.addWidget(test_type_group)
        
        # 统计量选项
        stats_group = QGroupBox("统计量")
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(10)
        
        self.check_mean_diff = QCheckBox("均值差异")
        self.check_mean_diff.setChecked(True)
        self.check_mean_diff.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_mean_diff)
        
        self.check_std_error = QCheckBox("标准误")
        self.check_std_error.setChecked(True)
        self.check_std_error.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_std_error)
        
        self.check_t_stat = QCheckBox("t统计量")
        self.check_t_stat.setChecked(True)
        self.check_t_stat.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_t_stat)
        
        self.check_df = QCheckBox("自由度")
        self.check_df.setChecked(True)
        self.check_df.toggled.connect(self._update_statistics_options)
        stats_layout.addWidget(self.check_df)
        
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
        test_types = ["paired-t", "wilcoxon"]
        self.test_type = test_types[index]
    
    def _update_statistics_options(self):
        """更新统计量选项"""
        self.statistics_options['mean_difference'] = self.check_mean_diff.isChecked()
        self.statistics_options['std_error'] = self.check_std_error.isChecked()
        self.statistics_options['t_statistic'] = self.check_t_stat.isChecked()
        self.statistics_options['df'] = self.check_df.isChecked()
        self.statistics_options['p_value'] = self.check_p_value.isChecked()
    
    def _set_demo_data(self):
        """设置演示数据"""
        # 前测变量
        pre_variables = [
            ("PRE_TEST1", "numeric"),
            ("PRE_TEST2", "numeric"),
            ("PRE_TEST3", "numeric")
        ]
        self.pre_selector.set_variables(pre_variables)
        
        # 后测变量
        post_variables = [
            ("POST_TEST1", "numeric"),
            ("POST_TEST2", "numeric"),
            ("POST_TEST3", "numeric")
        ]
        self.post_selector.set_variables(post_variables)
    
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
            'pre': self.pre_selector.get_selected_variables(),
            'post': self.post_selector.get_selected_variables(),
            'test_type': self.test_type
        }
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        # TODO: 实现粘贴功能
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        # 重置变量选择
        self.pre_selector.clear()
        self.post_selector.clear()
        self._set_demo_data()
        
        # 重置检验类型
        self.test_type_combo.setCurrentIndex(0)
        
        # 重置统计量选项
        self.check_mean_diff.setChecked(True)
        self.check_std_error.setChecked(True)
        self.check_t_stat.setChecked(True)
        self.check_df.setChecked(True)
        self.check_p_value.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'two_related',
            'results': self.analysis_results,
            'statistics_options': self.statistics_options.copy(),
            'test_type': self.test_type
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行两个相关样本检验"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        pre_vars = selected_variables['pre']
        post_vars = selected_variables['post']
        test_type = selected_variables['test_type']
        
        if not pre_vars or not post_vars:
            return
        
        self.analysis_results = []
        
        # 对每个变量对执行分析
        for var1_name, var1_type in pre_vars:
            for var2_name, var2_type in post_vars:
                # 只对数值变量进行分析
                if var1_type != "numeric" or var2_type != "numeric":
                    continue
                
                # 获取变量数据（这里使用模拟数据）
                pre_data, post_data = self._get_variable_data(var1_name, var2_name)
                
                if pre_data and post_data:
                    # 执行统计计算
                    if test_type == "paired-t":
                        from axaltyx.core.means.ttest_paired import PairedTTest
                        result_table = PairedTTest.create_result_table(
                            var1_name, var2_name
                        )
                    else:
                        from axaltyx.core.nonparametric.wilcoxon import WilcoxonTest
                        result_table = WilcoxonTest.create_result_table(
                            var1_name, var2_name
                        )
                    
                    self.analysis_results.append(result_table)
    
    def _get_variable_data(self, var1_name, var2_name):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in var1_name + var2_name)
        random.seed(seed)
        np.random.seed(seed)
        
        # 生成前测数据
        pre_data = np.random.normal(50, 10, size=50)
        
        # 生成后测数据（与前测数据相关）
        post_data = pre_data + np.random.normal(5, 5, size=50)
        
        # 转换为列表
        return list(pre_data), list(post_data)