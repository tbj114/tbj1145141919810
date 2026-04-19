#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
二项检验对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QDoubleSpinBox,
                             QLabel, QComboBox, QRadioButton)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class BinomialDialog(ArcoDialog):
    """二项检验对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化二项检验对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 450)
        self.i18n = I18nManager()
        self.set_title("二项检验")
        self.dataset = dataset
        
        # 初始化参数
        self.test_proportion = 0.5
        self.test_type = "two-tailed"  # two-tailed, one-tailed-lower, one-tailed-upper
        self.missing_values_option = "exclude_analysis"
        
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
        self.variable_selector.set_selected_label("检验变量")
        main_layout.addWidget(self.variable_selector, 1)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 检验选项
        test_widget = QWidget()
        test_layout = QVBoxLayout()
        test_layout.setSpacing(12)
        
        # 检验比例设置
        proportion_group = QGroupBox("检验比例")
        proportion_layout = QHBoxLayout()
        proportion_layout.setSpacing(10)
        
        proportion_label = QLabel("检验比例:")
        self.proportion_spin = QDoubleSpinBox()
        self.proportion_spin.setRange(0.001, 0.999)
        self.proportion_spin.setDecimals(3)
        self.proportion_spin.setValue(self.test_proportion)
        self.proportion_spin.valueChanged.connect(self._update_test_proportion)
        proportion_unit = QLabel("")
        
        proportion_layout.addWidget(proportion_label)
        proportion_layout.addWidget(self.proportion_spin)
        proportion_layout.addWidget(proportion_unit)
        proportion_layout.addStretch()
        proportion_group.setLayout(proportion_layout)
        test_layout.addWidget(proportion_group)
        
        # 检验类型选项
        test_type_group = QGroupBox("检验类型")
        test_type_layout = QVBoxLayout()
        
        self.radio_two_tailed = QRadioButton("双侧检验")
        self.radio_two_tailed.setChecked(True)
        self.radio_two_tailed.toggled.connect(self._update_test_type)
        test_type_layout.addWidget(self.radio_two_tailed)
        
        self.radio_one_tailed_lower = QRadioButton("单侧检验（小于）")
        self.radio_one_tailed_lower.toggled.connect(self._update_test_type)
        test_type_layout.addWidget(self.radio_one_tailed_lower)
        
        self.radio_one_tailed_upper = QRadioButton("单侧检验（大于）")
        self.radio_one_tailed_upper.toggled.connect(self._update_test_type)
        test_type_layout.addWidget(self.radio_one_tailed_upper)
        
        test_type_group.setLayout(test_type_layout)
        test_layout.addWidget(test_type_group)
        
        # 缺失值处理选项
        missing_group = QGroupBox("缺失值")
        missing_layout = QVBoxLayout()
        
        self.radio_exclude_analysis = QRadioButton("按分析排除个案")
        self.radio_exclude_analysis.setChecked(True)
        self.radio_exclude_analysis.toggled.connect(self._update_missing_values_option)
        
        self.radio_exclude_listwise = QRadioButton("按列表排除个案")
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
    
    def _update_test_proportion(self, value):
        """更新检验比例"""
        self.test_proportion = value
    
    def _update_test_type(self):
        """更新检验类型"""
        if self.radio_two_tailed.isChecked():
            self.test_type = "two-tailed"
        elif self.radio_one_tailed_lower.isChecked():
            self.test_type = "one-tailed-lower"
        elif self.radio_one_tailed_upper.isChecked():
            self.test_type = "one-tailed-upper"
    
    def _update_missing_values_option(self):
        """更新缺失值处理选项"""
        if self.radio_exclude_analysis.isChecked():
            self.missing_values_option = "exclude_analysis"
        elif self.radio_exclude_listwise.isChecked():
            self.missing_values_option = "exclude_listwise"
    
    def _set_demo_data(self):
        """设置演示数据"""
        demo_variables = [
            ("GENDER", "string"),
            ("GROUP", "numeric"),
            ("TREATMENT", "numeric"),
            ("OUTCOME", "string"),
            ("RESPONSE", "numeric")
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
        
        # 重置检验比例
        self.proportion_spin.setValue(0.5)
        
        # 重置检验类型
        self.radio_two_tailed.setChecked(True)
        
        # 重置缺失值处理选项
        self.radio_exclude_analysis.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'binomial',
            'results': self.analysis_results,
            'test_proportion': self.test_proportion,
            'test_type': self.test_type,
            'missing_values_option': self.missing_values_option
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行二项检验分析"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        
        if not selected_variables:
            return
        
        self.analysis_results = []
        
        # 对每个变量执行分析
        for var_name, var_type in selected_variables:
            # 获取变量数据（这里使用模拟数据）
            variable_data = self._get_variable_data(var_name)
            
            if variable_data:
                # 执行统计计算
                from scipy import stats
                import numpy as np
                
                # 计算成功次数（值为1的次数）
                successes = sum(1 for x in variable_data if x == 1)
                n = len(variable_data)
                
                # 执行二项检验
                p_value = None
                if self.test_type == "two-tailed":
                    # 双侧检验
                    p_value = 2 * min(
                        stats.binom.cdf(successes, n, self.test_proportion),
                        1 - stats.binom.cdf(successes - 1, n, self.test_proportion)
                    )
                elif self.test_type == "one-tailed-lower":
                    # 单侧检验（小于）
                    p_value = stats.binom.cdf(successes, n, self.test_proportion)
                elif self.test_type == "one-tailed-upper":
                    # 单侧检验（大于）
                    p_value = 1 - stats.binom.cdf(successes - 1, n, self.test_proportion)
                
                # 计算观察比例
                observed_proportion = successes / n
                
                # 创建结果
                result = {
                    'variable': var_name,
                    'n': n,
                    'successes': successes,
                    'observed_proportion': observed_proportion,
                    'test_proportion': self.test_proportion,
                    'p_value': p_value,
                    'test_type': self.test_type
                }
                
                self.analysis_results.append(result)
    
    def _get_variable_data(self, var_name):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in var_name)
        random.seed(seed)
        np.random.seed(seed)
        
        # 生成二项分布数据（0或1）
        # 模拟成功率为0.6
        data = np.random.binomial(1, 0.6, size=100)
        
        # 转换为列表
        return list(data)
