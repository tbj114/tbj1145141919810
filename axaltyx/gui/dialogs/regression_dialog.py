#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
回归分析对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QComboBox, QLabel,
                             QRadioButton, QButtonGroup)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class RegressionDialog(ArcoDialog):
    """回归分析对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化回归分析对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title("回归分析")
        self.dataset = dataset
        
        # 初始化参数
        self.regression_type = "linear"  # linear, multiple, logistic
        self.dependent_variable = None
        self.independent_variables = []
        self.include_constant = True
        self.confidence_interval = 95
        
        self.analysis_results = []
        
        # 初始化UI
        self._init_ui()
        self._init_bottom_buttons()
    
    def _init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # 变量选择区域
        var_layout = QHBoxLayout()
        var_layout.setSpacing(20)
        
        # 因变量选择
        dep_group = QGroupBox("因变量")
        dep_layout = QVBoxLayout()
        self.dep_selector = VariableSelector()
        self.dep_selector.set_available_label("可用变量")
        self.dep_selector.set_selected_label("因变量")
        self.dep_selector.set_max_selected(1)  # 只允许选择一个因变量
        dep_layout.addWidget(self.dep_selector)
        dep_group.setLayout(dep_layout)
        var_layout.addWidget(dep_group, 1)
        
        # 自变量选择
        indep_group = QGroupBox("自变量")
        indep_layout = QVBoxLayout()
        self.indep_selector = VariableSelector()
        self.indep_selector.set_available_label("可用变量")
        self.indep_selector.set_selected_label("自变量")
        indep_layout.addWidget(self.indep_selector)
        indep_group.setLayout(indep_layout)
        var_layout.addWidget(indep_group, 1)
        
        main_layout.addLayout(var_layout, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 回归类型选项
        type_widget = QWidget()
        type_layout = QVBoxLayout()
        type_layout.setSpacing(12)
        
        # 回归类型选择
        type_group = QGroupBox("回归类型")
        type_button_group = QButtonGroup()
        type_button_layout = QVBoxLayout()
        
        self.radio_linear = QRadioButton("线性回归")
        self.radio_linear.setChecked(True)
        self.radio_multiple = QRadioButton("多元线性回归")
        self.radio_logistic = QRadioButton("Logistic回归")
        
        type_button_group.addButton(self.radio_linear)
        type_button_group.addButton(self.radio_multiple)
        type_button_group.addButton(self.radio_logistic)
        
        type_button_layout.addWidget(self.radio_linear)
        type_button_layout.addWidget(self.radio_multiple)
        type_button_layout.addWidget(self.radio_logistic)
        
        type_group.setLayout(type_button_layout)
        type_layout.addWidget(type_group)
        
        # 模型选项
        model_group = QGroupBox("模型选项")
        model_layout = QVBoxLayout()
        
        self.check_constant = QCheckBox("包含常数项")
        self.check_constant.setChecked(True)
        self.check_constant.toggled.connect(self._update_include_constant)
        model_layout.addWidget(self.check_constant)
        
        model_group.setLayout(model_layout)
        type_layout.addWidget(model_group)
        
        type_widget.setLayout(type_layout)
        options_tabs.addTab(type_widget, "回归类型")
        
        # 统计量选项
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(12)
        
        stats_group = QGroupBox("统计量")
        stats_check_layout = QVBoxLayout()
        
        self.check_descriptives = QCheckBox("描述性统计")
        self.check_descriptives.setChecked(True)
        self.check_anova = QCheckBox("方差分析")
        self.check_anova.setChecked(True)
        self.check_coefficients = QCheckBox("回归系数")
        self.check_coefficients.setChecked(True)
        self.check_model_summary = QCheckBox("模型摘要")
        self.check_model_summary.setChecked(True)
        
        stats_check_layout.addWidget(self.check_descriptives)
        stats_check_layout.addWidget(self.check_anova)
        stats_check_layout.addWidget(self.check_coefficients)
        stats_check_layout.addWidget(self.check_model_summary)
        
        stats_group.setLayout(stats_check_layout)
        stats_layout.addWidget(stats_group)
        
        stats_widget.setLayout(stats_layout)
        options_tabs.addTab(stats_widget, "统计量")
        
        main_layout.addWidget(options_tabs, 1)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
        
        # 设置测试数据（如果没有数据集）
        if self.dataset:
            self._set_variables_from_dataset()
        else:
            self._set_demo_data()
    
    def _update_include_constant(self, checked):
        """更新是否包含常数项"""
        self.include_constant = checked
    
    def _set_demo_data(self):
        """设置演示数据"""
        demo_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "numeric"),
            ("VAR00003", "numeric"),
            ("VAR00004", "numeric"),
            ("VAR00005", "numeric")
        ]
        self.dep_selector.set_variables(demo_variables)
        self.indep_selector.set_variables(demo_variables)
    
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
        self.dep_selector.clear()
        self.indep_selector.clear()
        self._set_demo_data()
        
        # 重置回归类型
        self.radio_linear.setChecked(True)
        
        # 重置模型选项
        self.check_constant.setChecked(True)
        
        # 重置统计量选项
        self.check_descriptives.setChecked(True)
        self.check_anova.setChecked(True)
        self.check_coefficients.setChecked(True)
        self.check_model_summary.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'regression',
            'results': self.analysis_results,
            'regression_type': self._get_selected_regression_type(),
            'dependent_variable': self._get_dependent_variable(),
            'independent_variables': self._get_independent_variables(),
            'include_constant': self.include_constant
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _get_selected_regression_type(self):
        """获取选中的回归类型"""
        if self.radio_linear.isChecked():
            return "linear"
        elif self.radio_multiple.isChecked():
            return "multiple"
        else:
            return "logistic"
    
    def _get_dependent_variable(self):
        """获取因变量"""
        dep_vars = self.dep_selector.get_selected_variables()
        return dep_vars[0][0] if dep_vars else None
    
    def _get_independent_variables(self):
        """获取自变量列表"""
        indep_vars = self.indep_selector.get_selected_variables()
        return [var[0] for var in indep_vars]
    
    def _perform_analysis(self):
        """执行回归分析"""
        # 获取因变量和自变量
        dep_var = self._get_dependent_variable()
        indep_vars = self._get_independent_variables()
        
        if not dep_var or not indep_vars:
            return
        
        self.analysis_results = []
        
        # 生成模拟数据
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import LinearRegression, LogisticRegression
        from sklearn.metrics import r2_score
        
        # 生成自变量数据
        n_samples = 100
        X = np.zeros((n_samples, len(indep_vars)))
        for i, var_name in enumerate(indep_vars):
            seed = sum(ord(c) for c in var_name)
            np.random.seed(seed)
            X[:, i] = np.random.normal(50 + (seed % 20), 10 + (seed % 5), size=n_samples)
        
        # 生成因变量数据
        seed = sum(ord(c) for c in dep_var)
        np.random.seed(seed)
        
        if self._get_selected_regression_type() == "logistic":
            # Logistic回归数据
            coefficients = np.random.normal(0.1, 0.05, size=len(indep_vars))
            intercept = np.random.normal(0, 1)
            linear_combination = np.dot(X, coefficients) + intercept
            y = 1 / (1 + np.exp(-linear_combination))
            y = (y > 0.5).astype(int)
        else:
            # 线性回归数据
            coefficients = np.random.normal(0.5, 0.2, size=len(indep_vars))
            intercept = np.random.normal(10, 5)
            y = np.dot(X, coefficients) + intercept + np.random.normal(0, 5, size=n_samples)
        
        # 执行回归
        if self._get_selected_regression_type() == "logistic":
            model = LogisticRegression()
            model.fit(X, y)
            y_pred = model.predict(X)
            accuracy = (y_pred == y).mean()
            coefficients = model.coef_[0]
            intercept = model.intercept_[0]
        else:
            model = LinearRegression(fit_intercept=self.include_constant)
            model.fit(X, y)
            y_pred = model.predict(X)
            r2 = r2_score(y, y_pred)
            coefficients = model.coef_
            intercept = model.intercept_ if self.include_constant else 0
        
        # 创建结果
        regression_result = {
            'dependent_variable': dep_var,
            'independent_variables': indep_vars,
            'regression_type': self._get_selected_regression_type(),
            'coefficients': coefficients.tolist(),
            'intercept': intercept,
            'sample_size': n_samples
        }
        
        if self._get_selected_regression_type() != "logistic":
            regression_result['r_squared'] = r2
        else:
            regression_result['accuracy'] = accuracy
        
        self.analysis_results.append(regression_result)