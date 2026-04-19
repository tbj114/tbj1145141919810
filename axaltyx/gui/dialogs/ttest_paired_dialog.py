#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配对样本T检验对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QDoubleSpinBox,
                             QLabel, QComboBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import pyqtSignal, Qt
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class TTestPairedDialog(ArcoDialog):
    """配对样本T检验对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化配对样本T检验对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 800, 550)
        self.i18n = I18nManager()
        self.set_title("配对样本 T 检验")
        self.dataset = dataset
        
        # 初始化参数
        self.confidence_interval = 95
        self.missing_values_option = "exclude_analysis"
        
        self.analysis_results = []
        self.paired_variables = []  # 存储配对的变量对
        
        # 初始化UI
        self._init_ui()
        self._init_bottom_buttons()
    
    def _init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # 变量配对区域
        pair_section = QWidget()
        pair_layout = QHBoxLayout()
        pair_layout.setSpacing(20)
        
        # 左侧变量选择器
        self.variable_selector = VariableSelector()
        self.variable_selector.set_available_label("可用变量")
        self.variable_selector.set_selected_label("已选变量")
        pair_layout.addWidget(self.variable_selector, 1)
        
        # 中间配对按钮
        button_widget = QWidget()
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        # 添加配对按钮
        self.add_pair_button = QPushButton(">>")
        self.add_pair_button.setMinimumSize(40, 30)
        self.add_pair_button.clicked.connect(self._add_pair)
        button_layout.addWidget(self.add_pair_button)
        
        # 移除配对按钮
        self.remove_pair_button = QPushButton("<<")
        self.remove_pair_button.setMinimumSize(40, 30)
        self.remove_pair_button.clicked.connect(self._remove_pair)
        button_layout.addWidget(self.remove_pair_button)
        
        button_widget.setLayout(button_layout)
        pair_layout.addWidget(button_widget)
        
        # 右侧配对列表
        self.pair_list_widget = QListWidget()
        self.pair_list_widget.setMinimumWidth(300)
        self.pair_list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        pair_layout.addWidget(self.pair_list_widget, 1)
        
        pair_section.setLayout(pair_layout)
        main_layout.addWidget(pair_section, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 检验选项
        test_widget = QWidget()
        test_layout = QVBoxLayout()
        test_layout.setSpacing(12)
        
        # 置信区间设置
        ci_group = QGroupBox("置信区间百分比")
        ci_layout = QHBoxLayout()
        ci_layout.setSpacing(10)
        
        ci_label = QLabel("置信区间:")
        self.ci_spin = QSpinBox()
        self.ci_spin.setRange(50, 99)
        self.ci_spin.setValue(self.confidence_interval)
        self.ci_spin.valueChanged.connect(self._update_confidence_interval)
        ci_unit = QLabel("%")
        
        ci_layout.addWidget(ci_label)
        ci_layout.addWidget(self.ci_spin)
        ci_layout.addWidget(ci_unit)
        ci_layout.addStretch()
        ci_group.setLayout(ci_layout)
        test_layout.addWidget(ci_group)
        
        # 缺失值处理选项
        missing_group = QGroupBox("缺失值")
        missing_layout = QVBoxLayout()
        
        self.radio_exclude_analysis = QCheckBox("按分析排除个案")
        self.radio_exclude_analysis.setChecked(True)
        self.radio_exclude_analysis.toggled.connect(self._update_missing_values_option)
        
        self.radio_exclude_listwise = QCheckBox("按列表排除个案")
        self.radio_exclude_listwise.setChecked(False)
        self.radio_exclude_listwise.toggled.connect(self._update_missing_values_option)
        
        missing_layout.addWidget(self.radio_exclude_analysis)
        missing_layout.addWidget(self.radio_exclude_listwise)
        missing_group.setLayout(missing_layout)
        test_layout.addWidget(missing_group)
        
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
    
    def _update_confidence_interval(self, value):
        """更新置信区间"""
        self.confidence_interval = value
    
    def _update_missing_values_option(self):
        """更新缺失值处理选项"""
        if self.radio_exclude_analysis.isChecked():
            self.missing_values_option = "exclude_analysis"
        elif self.radio_exclude_listwise.isChecked():
            self.missing_values_option = "exclude_listwise"
    
    def _add_pair(self):
        """添加配对变量"""
        selected_variables = self.variable_selector.get_selected_variables()
        if len(selected_variables) >= 2:
            # 取前两个变量作为一对
            var1 = selected_variables[0]
            var2 = selected_variables[1]
            pair = (var1, var2)
            
            # 检查是否已经存在
            if pair not in self.paired_variables:
                self.paired_variables.append(pair)
                item = QListWidgetItem(f"{var1[0]} ↔ {var2[0]}")
                self.pair_list_widget.addItem(item)
    
    def _remove_pair(self):
        """移除配对变量"""
        selected_item = self.pair_list_widget.currentItem()
        if selected_item:
            index = self.pair_list_widget.row(selected_item)
            if 0 <= index < len(self.paired_variables):
                self.paired_variables.pop(index)
                self.pair_list_widget.takeItem(index)
    
    def _set_demo_data(self):
        """设置演示数据"""
        demo_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "numeric"),
            ("VAR00003", "numeric"),
            ("VAR00004", "numeric"),
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
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        # TODO: 实现粘贴功能
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        # 重置变量选择
        self.variable_selector.clear()
        self._set_demo_data()
        
        # 重置配对列表
        self.paired_variables.clear()
        self.pair_list_widget.clear()
        
        # 重置置信区间
        self.ci_spin.setValue(95)
        
        # 重置缺失值处理选项
        self.radio_exclude_analysis.setChecked(True)
        self.radio_exclude_listwise.setChecked(False)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'ttest_paired',
            'results': self.analysis_results,
            'confidence_interval': self.confidence_interval,
            'missing_values_option': self.missing_values_option,
            'paired_variables': self.paired_variables
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行配对样本T检验分析"""
        # 检查是否有配对变量
        if not self.paired_variables:
            return
        
        self.analysis_results = []
        
        # 对每对变量执行分析
        for pair in self.paired_variables:
            var1, var2 = pair
            var1_name, var1_type = var1
            var2_name, var2_type = var2
            
            # 只对数值变量进行分析
            if var1_type != "numeric" or var2_type != "numeric":
                continue
            
            # 获取变量数据（这里使用模拟数据）
            data1, data2 = self._get_variable_data(var1_name, var2_name)
            
            if data1 and data2:
                # 执行统计计算
                from scipy import stats
                import numpy as np
                
                # 执行配对T检验
                t_stat, p_value = stats.ttest_rel(data1, data2)
                
                # 计算差异
                differences = np.array(data1) - np.array(data2)
                mean_diff = np.mean(differences)
                std_diff = np.std(differences, ddof=1)
                sem = std_diff / np.sqrt(len(differences))
                
                # 计算置信区间
                ci = stats.t.interval(
                    alpha=self.confidence_interval/100,
                    df=len(differences)-1,
                    loc=mean_diff,
                    scale=sem
                )
                
                # 创建结果
                result = {
                    'variable1': var1_name,
                    'variable2': var2_name,
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'df': len(differences) - 1,
                    'mean_diff': mean_diff,
                    'std_diff': std_diff,
                    'std_error': sem,
                    'confidence_interval': ci
                }
                
                self.analysis_results.append(result)
    
    def _get_variable_data(self, var1_name, var2_name):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in var1_name + var2_name)
        random.seed(seed)
        np.random.seed(seed)
        
        # 生成相关的正态分布数据
        mean1 = 50 + (seed % 20)
        mean2 = mean1 + 2  # 配对变量有一定差异
        std = 10 + (seed % 5)
        
        # 生成相关数据
        data1 = np.random.normal(mean1, std, size=100)
        # 生成与data1相关的data2
        data2 = data1 + np.random.normal(mean2 - mean1, std * 0.5, size=100)
        
        # 转换为列表
        return list(data1), list(data2)
