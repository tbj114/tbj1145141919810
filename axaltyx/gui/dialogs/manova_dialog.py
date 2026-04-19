#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多因素方差分析对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QSpinBox, QDoubleSpinBox,
                             QLabel, QComboBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class MANOVADialog(ArcoDialog):
    """多因素方差分析对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化多因素方差分析对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 800, 600)
        self.i18n = I18nManager()
        self.set_title("多因素方差分析")
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
        
        # 因变量选择器
        self.dependent_selector = VariableSelector()
        self.dependent_selector.set_available_label("因变量")
        self.dependent_selector.set_selected_label("分析变量")
        variable_layout.addWidget(self.dependent_selector, 2)
        
        # 因子变量选择器
        self.factor_selector = VariableSelector()
        self.factor_selector.set_available_label("因子变量")
        self.factor_selector.set_selected_label("因子变量")
        variable_layout.addWidget(self.factor_selector, 1)
        
        variable_section.setLayout(variable_layout)
        main_layout.addWidget(variable_section, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 统计选项
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(12)
        
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
        stats_layout.addWidget(ci_group)
        
        # 统计量选项
        stats_options_group = QGroupBox("统计量")
        stats_options_layout = QVBoxLayout()
        
        self.check_descriptives = QCheckBox("描述性统计")
        self.check_descriptives.setChecked(True)
        stats_options_layout.addWidget(self.check_descriptives)
        
        self.check_homogeneity = QCheckBox("方差齐性检验")
        self.check_homogeneity.setChecked(True)
        stats_options_layout.addWidget(self.check_homogeneity)
        
        self.check_effect_size = QCheckBox("效应量")
        self.check_effect_size.setChecked(True)
        stats_options_layout.addWidget(self.check_effect_size)
        
        stats_options_group.setLayout(stats_options_layout)
        stats_layout.addWidget(stats_options_group)
        
        # 模型选项
        model_group = QGroupBox("模型选项")
        model_layout = QVBoxLayout()
        
        self.check_main_effects = QCheckBox("主效应")
        self.check_main_effects.setChecked(True)
        model_layout.addWidget(self.check_main_effects)
        
        self.check_interactions = QCheckBox("交互效应")
        self.check_interactions.setChecked(True)
        model_layout.addWidget(self.check_interactions)
        
        model_group.setLayout(model_layout)
        stats_layout.addWidget(model_group)
        
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
    
    def _update_confidence_interval(self, value):
        """更新置信区间"""
        self.confidence_interval = value
    
    def _update_missing_values_option(self):
        """更新缺失值处理选项"""
        if self.radio_exclude_analysis.isChecked():
            self.missing_values_option = "exclude_analysis"
        elif self.radio_exclude_listwise.isChecked():
            self.missing_values_option = "exclude_listwise"
    
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
            ("GROUP", "numeric"),
            ("GENDER", "string"),
            ("TREATMENT", "numeric")
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
    
    def get_selected_dependent_variables(self):
        """获取选中的因变量列表"""
        return self.dependent_selector.get_selected_variables()
    
    def get_selected_factor_variables(self):
        """获取选中的因子变量列表"""
        return self.factor_selector.get_selected_variables()
    
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
        
        # 重置置信区间
        self.ci_spin.setValue(95)
        
        # 重置统计量选项
        self.check_descriptives.setChecked(True)
        self.check_homogeneity.setChecked(True)
        self.check_effect_size.setChecked(True)
        
        # 重置模型选项
        self.check_main_effects.setChecked(True)
        self.check_interactions.setChecked(True)
        
        # 重置缺失值处理选项
        self.radio_exclude_analysis.setChecked(True)
        self.radio_exclude_listwise.setChecked(False)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'manova',
            'results': self.analysis_results,
            'confidence_interval': self.confidence_interval,
            'missing_values_option': self.missing_values_option,
            'descriptives': self.check_descriptives.isChecked(),
            'homogeneity_test': self.check_homogeneity.isChecked(),
            'effect_size': self.check_effect_size.isChecked(),
            'main_effects': self.check_main_effects.isChecked(),
            'interactions': self.check_interactions.isChecked()
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行多因素方差分析"""
        # 获取选中的变量
        dependent_variables = self.get_selected_dependent_variables()
        factor_variables = self.get_selected_factor_variables()
        
        if not dependent_variables or not factor_variables:
            return
        
        self.analysis_results = []
        
        # 模拟多因素方差分析结果
        for dep_var_name, dep_var_type in dependent_variables:
            if dep_var_type != "numeric":
                continue
            
            # 生成模拟结果
            result = {
                'dependent_variable': dep_var_name,
                'factor_variables': [f[0] for f in factor_variables],
                'model_summary': {
                    'f_statistic': 3.25,
                    'p_value': 0.021,
                    'df_model': len(factor_variables),
                    'df_error': 95
                },
                'effects': {
                    'main_effects': [],
                    'interactions': []
                }
            }
            
            # 添加主效应
            if self.check_main_effects.isChecked():
                for factor in factor_variables:
                    result['effects']['main_effects'].append({
                        'factor': factor[0],
                        'f_statistic': 2.89,
                        'p_value': 0.034,
                        'df': 1
                    })
            
            # 添加交互效应
            if self.check_interactions.isChecked() and len(factor_variables) >= 2:
                result['effects']['interactions'].append({
                    'interaction': f"{factor_variables[0][0]} * {factor_variables[1][0]}",
                    'f_statistic': 1.98,
                    'p_value': 0.142,
                    'df': 1
                })
            
            self.analysis_results.append(result)
