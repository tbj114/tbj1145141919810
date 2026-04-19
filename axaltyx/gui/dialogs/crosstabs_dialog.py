#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交叉表与卡方检验对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QDoubleSpinBox,
                             QLabel, QComboBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class CrosstabsDialog(ArcoDialog):
    """交叉表与卡方检验对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化交叉表与卡方检验对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 800, 550)
        self.i18n = I18nManager()
        self.set_title("交叉表")
        self.dataset = dataset
        
        # 初始化参数
        self.confidence_interval = 95
        self.missing_values_option = "exclude_analysis"
        
        self.analysis_results = []
        
        # 初始化UI
        self._init_ui()
        self._init_bottom_buttons()
    
    def _init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # 变量选择区域
        variable_section = QWidget()
        variable_layout = QHBoxLayout()
        variable_layout.setSpacing(20)
        
        # 行变量选择器
        self.row_selector = VariableSelector()
        self.row_selector.set_available_label("行变量")
        self.row_selector.set_selected_label("行变量")
        variable_layout.addWidget(self.row_selector, 1)
        
        # 列变量选择器
        self.column_selector = VariableSelector()
        self.column_selector.set_available_label("列变量")
        self.column_selector.set_selected_label("列变量")
        variable_layout.addWidget(self.column_selector, 1)
        
        # 层变量选择器
        self.layer_selector = VariableSelector()
        self.layer_selector.set_available_label("层变量")
        self.layer_selector.set_selected_label("层变量")
        variable_layout.addWidget(self.layer_selector, 1)
        
        variable_section.setLayout(variable_layout)
        main_layout.addWidget(variable_section, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 统计选项
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(12)
        
        # 统计量选项
        stats_options_group = QGroupBox("统计量")
        stats_options_layout = QVBoxLayout()
        
        self.check_chi_square = QCheckBox("卡方检验")
        self.check_chi_square.setChecked(True)
        stats_options_layout.addWidget(self.check_chi_square)
        
        self.check_cramer_v = QCheckBox("Cramer's V (效应量)")
        self.check_cramer_v.setChecked(True)
        stats_options_layout.addWidget(self.check_cramer_v)
        
        self.check_phi = QCheckBox("Phi 系数")
        self.check_phi.setChecked(False)
        stats_options_layout.addWidget(self.check_phi)
        
        stats_options_group.setLayout(stats_options_layout)
        stats_layout.addWidget(stats_options_group)
        
        # 单元格选项
        cell_group = QGroupBox("单元格显示")
        cell_layout = QVBoxLayout()
        
        self.check_observed = QCheckBox("观察值")
        self.check_observed.setChecked(True)
        cell_layout.addWidget(self.check_observed)
        
        self.check_expected = QCheckBox("期望值")
        self.check_expected.setChecked(True)
        cell_layout.addWidget(self.check_expected)
        
        self.check_row_percentages = QCheckBox("行百分比")
        self.check_row_percentages.setChecked(False)
        cell_layout.addWidget(self.check_row_percentages)
        
        self.check_column_percentages = QCheckBox("列百分比")
        self.check_column_percentages.setChecked(False)
        cell_layout.addWidget(self.check_column_percentages)
        
        self.check_total_percentages = QCheckBox("总百分比")
        self.check_total_percentages.setChecked(False)
        cell_layout.addWidget(self.check_total_percentages)
        
        cell_group.setLayout(cell_layout)
        stats_layout.addWidget(cell_group)
        
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
        stats_layout.addWidget(missing_group)
        
        stats_widget.setLayout(stats_layout)
        options_tabs.addTab(stats_widget, "统计选项")
        
        main_layout.addWidget(options_tabs, 1)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
        
        # 设置测试数据（如果没有数据集）
        if self.dataset:
            self._set_variables_from_dataset()
        else:
            self._set_demo_data()
    
    def _update_missing_values_option(self):
        """更新缺失值处理选项"""
        if self.radio_exclude_analysis.isChecked():
            self.missing_values_option = "exclude_analysis"
        elif self.radio_exclude_listwise.isChecked():
            self.missing_values_option = "exclude_listwise"
    
    def _set_demo_data(self):
        """设置演示数据"""
        # 分类变量
        categorical_variables = [
            ("GENDER", "string"),
            ("GROUP", "numeric"),
            ("TREATMENT", "numeric"),
            ("OUTCOME", "string"),
            ("EDUCATION", "numeric")
        ]
        
        self.row_selector.set_variables(categorical_variables)
        self.column_selector.set_variables(categorical_variables)
        self.layer_selector.set_variables(categorical_variables)
    
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
    
    def get_selected_row_variables(self):
        """获取选中的行变量列表"""
        return self.row_selector.get_selected_variables()
    
    def get_selected_column_variables(self):
        """获取选中的列变量列表"""
        return self.column_selector.get_selected_variables()
    
    def get_selected_layer_variables(self):
        """获取选中的层变量列表"""
        return self.layer_selector.get_selected_variables()
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        # TODO: 实现粘贴功能
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        # 重置变量选择
        self.row_selector.clear()
        self.column_selector.clear()
        self.layer_selector.clear()
        self._set_demo_data()
        
        # 重置统计量选项
        self.check_chi_square.setChecked(True)
        self.check_cramer_v.setChecked(True)
        self.check_phi.setChecked(False)
        
        # 重置单元格选项
        self.check_observed.setChecked(True)
        self.check_expected.setChecked(True)
        self.check_row_percentages.setChecked(False)
        self.check_column_percentages.setChecked(False)
        self.check_total_percentages.setChecked(False)
        
        # 重置缺失值处理选项
        self.radio_exclude_analysis.setChecked(True)
        self.radio_exclude_listwise.setChecked(False)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'crosstabs',
            'results': self.analysis_results,
            'missing_values_option': self.missing_values_option,
            'chi_square': self.check_chi_square.isChecked(),
            'cramer_v': self.check_cramer_v.isChecked(),
            'phi': self.check_phi.isChecked(),
            'observed': self.check_observed.isChecked(),
            'expected': self.check_expected.isChecked(),
            'row_percentages': self.check_row_percentages.isChecked(),
            'column_percentages': self.check_column_percentages.isChecked(),
            'total_percentages': self.check_total_percentages.isChecked()
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行交叉表与卡方检验分析"""
        # 获取选中的变量
        row_variables = self.get_selected_row_variables()
        column_variables = self.get_selected_column_variables()
        layer_variables = self.get_selected_layer_variables()
        
        if not row_variables or not column_variables:
            return
        
        self.analysis_results = []
        
        # 对每个行变量和列变量组合执行分析
        for row_var_name, row_var_type in row_variables:
            for col_var_name, col_var_type in column_variables:
                # 获取变量数据（这里使用模拟数据）
                row_data, col_data = self._get_variable_data(row_var_name, col_var_name)
                
                if row_data and col_data:
                    # 执行统计计算
                    from scipy import stats
                    import numpy as np
                    from collections import Counter
                    
                    # 创建交叉表
                    contingency_table = np.array([
                        [50, 30],
                        [20, 40]
                    ])
                    
                    # 执行卡方检验
                    chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                    
                    # 计算Cramer's V
                    n = contingency_table.sum()
                    min_dim = min(contingency_table.shape) - 1
                    cramer_v = np.sqrt(chi2_stat / (n * min_dim))
                    
                    # 计算Phi系数（仅适用于2x2表格）
                    phi = None
                    if contingency_table.shape == (2, 2):
                        phi = np.sqrt(chi2_stat / n)
                    
                    # 创建结果
                    result = {
                        'row_variable': row_var_name,
                        'column_variable': col_var_name,
                        'contingency_table': contingency_table.tolist(),
                        'chi_square': {
                            'statistic': chi2_stat,
                            'p_value': p_value,
                            'df': dof,
                            'expected': expected.tolist()
                        },
                        'effect_size': {
                            'cramer_v': cramer_v,
                            'phi': phi
                        }
                    }
                    
                    self.analysis_results.append(result)
    
    def _get_variable_data(self, row_var_name, col_var_name):
        """获取变量数据（模拟数据）"""
        import random
        import numpy as np
        
        # 根据变量名生成不同的模拟数据
        seed = sum(ord(c) for c in row_var_name + col_var_name)
        random.seed(seed)
        np.random.seed(seed)
        
        # 生成分类数据
        row_data = np.random.randint(1, 3, size=100)
        col_data = np.random.randint(1, 3, size=100)
        
        # 引入一些关联性
        for i in range(len(row_data)):
            if random.random() < 0.7:
                col_data[i] = row_data[i]
        
        # 转换为列表
        return list(row_data), list(col_data)
