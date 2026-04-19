#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
频数分析对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class FrequenciesDialog(ArcoDialog):
    """频数分析对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化频数分析对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title("频数分析")
        self.dataset = dataset
        
        # 初始化选择状态
        self.statistics_options = {
            'frequencies': True,
            'percentages': True,
            'cumulative_percentages': True,
            'valid_percentages': True
        }
        
        self.chart_options = {
            'bar_chart': False,
            'pie_chart': False
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
        self.variable_selector.set_available_label("变量")
        self.variable_selector.set_selected_label("分析变量")
        main_layout.addWidget(self.variable_selector, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 统计量选项
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(12)
        self._create_statistics_checkboxes(stats_layout)
        stats_widget.setLayout(stats_layout)
        options_tabs.addTab(stats_widget, "统计量")
        
        # 图表选项
        chart_widget = QWidget()
        chart_layout = QVBoxLayout()
        chart_layout.setSpacing(12)
        self._create_chart_checkboxes(chart_layout)
        chart_widget.setLayout(chart_layout)
        options_tabs.addTab(chart_widget, "图表")
        
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
        group = QGroupBox("显示")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        # 创建复选框
        self.check_frequencies = QCheckBox("频数")
        self.check_frequencies.setChecked(True)
        self.check_frequencies.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_frequencies)
        
        self.check_percentages = QCheckBox("百分比")
        self.check_percentages.setChecked(True)
        self.check_percentages.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_percentages)
        
        self.check_cumulative_percentages = QCheckBox("累计百分比")
        self.check_cumulative_percentages.setChecked(True)
        self.check_cumulative_percentages.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_cumulative_percentages)
        
        self.check_valid_percentages = QCheckBox("有效百分比")
        self.check_valid_percentages.setChecked(True)
        self.check_valid_percentages.toggled.connect(self._update_statistics_options)
        group_layout.addWidget(self.check_valid_percentages)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def _create_chart_checkboxes(self, parent_layout):
        """创建图表复选框"""
        group = QGroupBox("图表")
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        
        self.check_bar_chart = QCheckBox("条形图")
        self.check_bar_chart.toggled.connect(self._update_chart_options)
        group_layout.addWidget(self.check_bar_chart)
        
        self.check_pie_chart = QCheckBox("饼图")
        self.check_pie_chart.toggled.connect(self._update_chart_options)
        group_layout.addWidget(self.check_pie_chart)
        
        group.setLayout(group_layout)
        parent_layout.addWidget(group)
    
    def _update_statistics_options(self):
        """更新统计量选项"""
        self.statistics_options['frequencies'] = self.check_frequencies.isChecked()
        self.statistics_options['percentages'] = self.check_percentages.isChecked()
        self.statistics_options['cumulative_percentages'] = self.check_cumulative_percentages.isChecked()
        self.statistics_options['valid_percentages'] = self.check_valid_percentages.isChecked()
    
    def _update_chart_options(self):
        """更新图表选项"""
        self.chart_options['bar_chart'] = self.check_bar_chart.isChecked()
        self.chart_options['pie_chart'] = self.check_pie_chart.isChecked()
    
    def _set_demo_data(self):
        """设置演示数据"""
        demo_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "numeric"),
            ("VAR00003", "string"),
            ("VAR00004", "numeric"),
            ("VAR00005", "string")
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
        self.check_frequencies.setChecked(True)
        self.check_percentages.setChecked(True)
        self.check_cumulative_percentages.setChecked(True)
        self.check_valid_percentages.setChecked(True)
        
        # 重置图表选项
        self.check_bar_chart.setChecked(False)
        self.check_pie_chart.setChecked(False)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'frequencies',
            'results': self.analysis_results,
            'statistics_options': self.statistics_options.copy(),
            'chart_options': self.chart_options.copy()
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行频数分析"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        
        if not selected_variables:
            return
        
        self.analysis_results = []
        
        # 对每个变量执行分析
        for var_name, var_type in selected_variables:
            # 获取变量数据（这里使用模拟数据）
            variable_data = self._get_variable_data(var_name, var_type)
            
            if variable_data:
                # 计算频数
                from collections import Counter
                freq_counter = Counter(variable_data)
                
                # 计算总观测数
                total_count = len(variable_data)
                
                # 创建频数表
                frequency_table = []
                cumulative_count = 0
                
                for value, count in sorted(freq_counter.items()):
                    cumulative_count += count
                    percentage = (count / total_count) * 100
                    cumulative_percentage = (cumulative_count / total_count) * 100
                    
                    frequency_table.append({
                        'value': value,
                        'frequency': count,
                        'percentage': percentage,
                        'cumulative_percentage': cumulative_percentage
                    })
                
                # 创建结果
                result = {
                    'variable': var_name,
                    'variable_type': var_type,
                    'frequency_table': frequency_table,
                    'total_count': total_count
                }
                
                self.analysis_results.append(result)
    
    def _get_variable_data(self, var_name, var_type):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in var_name)
        random.seed(seed)
        np.random.seed(seed)
        
        if var_type == "string":
            # 生成分类数据
            categories = ["A", "B", "C", "D", "E"]
            data = [random.choice(categories) for _ in range(100)]
        else:
            # 生成离散数值数据
            data = np.random.randint(1, 6, size=100).tolist()
        
        return data