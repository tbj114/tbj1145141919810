#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
相关分析对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QComboBox, QLabel)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class CorrelationDialog(ArcoDialog):
    """相关分析对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化相关分析对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title(self.i18n.t("dialogs.correlation.title"))
        self.dataset = dataset
        
        # 初始化参数
        self.correlation_type = "pearson"  # pearson, kendall, spearman
        self.test_significance = True
        self.flag_significance = True
        
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
        self.variable_selector.set_available_label(self.i18n.t("dialogs.correlation.variables"))
        self.variable_selector.set_selected_label(self.i18n.t("dialogs.correlation.correlation_variables"))
        main_layout.addWidget(self.variable_selector, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 相关系数选项
        corr_widget = QWidget()
        corr_layout = QVBoxLayout()
        corr_layout.setSpacing(12)
        
        # 相关系数类型
        corr_type_group = QGroupBox(self.i18n.t("dialogs.correlation.correlation_coefficient"))
        corr_type_layout = QVBoxLayout()
        
        self.corr_type_combo = QComboBox()
        self.corr_type_combo.addItems([
            self.i18n.t("dialogs.correlation.pearson"),
            self.i18n.t("dialogs.correlation.kendall"),
            self.i18n.t("dialogs.correlation.spearman")
        ])
        self.corr_type_combo.currentIndexChanged.connect(self._update_correlation_type)
        corr_type_layout.addWidget(self.corr_type_combo)
        corr_type_group.setLayout(corr_type_layout)
        corr_layout.addWidget(corr_type_group)
        
        # 显著性检验选项
        test_group = QGroupBox(self.i18n.t("dialogs.correlation.significance_test"))
        test_layout = QVBoxLayout()
        
        self.check_test_significance = QCheckBox(self.i18n.t("dialogs.correlation.perform_significance_test"))
        self.check_test_significance.setChecked(True)
        self.check_test_significance.toggled.connect(self._update_test_significance)
        test_layout.addWidget(self.check_test_significance)
        
        self.check_flag_significance = QCheckBox(self.i18n.t("dialogs.correlation.flag_significant_correlations"))
        self.check_flag_significance.setChecked(True)
        self.check_flag_significance.toggled.connect(self._update_flag_significance)
        test_layout.addWidget(self.check_flag_significance)
        
        test_group.setLayout(test_layout)
        corr_layout.addWidget(test_group)
        
        corr_widget.setLayout(corr_layout)
        options_tabs.addTab(corr_widget, self.i18n.t("dialogs.correlation.correlation_options"))
        
        main_layout.addWidget(options_tabs, 1)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
        
        # 设置测试数据（如果没有数据集）
        if self.dataset:
            self._set_variables_from_dataset()
        else:
            self._set_demo_data()
    
    def _update_correlation_type(self, index):
        """更新相关系数类型"""
        types = ["pearson", "kendall", "spearman"]
        self.correlation_type = types[index]
    
    def _update_test_significance(self, checked):
        """更新显著性检验选项"""
        self.test_significance = checked
    
    def _update_flag_significance(self, checked):
        """更新显著性标记选项"""
        self.flag_significance = checked
    
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
        
        # 重置相关系数类型
        self.corr_type_combo.setCurrentIndex(0)
        
        # 重置显著性检验选项
        self.check_test_significance.setChecked(True)
        self.check_flag_significance.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'correlation',
            'results': self.analysis_results,
            'correlation_type': self.correlation_type,
            'test_significance': self.test_significance,
            'flag_significance': self.flag_significance
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行相关分析"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        
        if len(selected_variables) < 2:
            return
        
        self.analysis_results = []
        
        # 提取变量名和类型
        var_names = [var[0] for var in selected_variables if var[1] == "numeric"]
        
        if len(var_names) < 2:
            return
        
        # 生成模拟数据
        data_matrix = []
        for var_name in var_names:
            data = self._get_variable_data(var_name)
            data_matrix.append(data)
        
        # 计算相关矩阵
        import numpy as np
        from scipy import stats
        
        # 转置数据矩阵，使每行是一个观测，每列是一个变量
        data_matrix = np.array(data_matrix).T
        
        # 计算相关系数矩阵
        if self.correlation_type == "pearson":
            corr_matrix, p_matrix = stats.pearsonr(data_matrix[:, 0], data_matrix[:, 1])
            # 对于多个变量，使用numpy的corrcoef
            corr_matrix = np.corrcoef(data_matrix, rowvar=False)
            # 计算p值矩阵（简化版）
            p_matrix = np.zeros_like(corr_matrix)
            for i in range(len(var_names)):
                for j in range(len(var_names)):
                    if i != j:
                        _, p = stats.pearsonr(data_matrix[:, i], data_matrix[:, j])
                        p_matrix[i, j] = p
        elif self.correlation_type == "kendall":
            corr_matrix, p_matrix = stats.kendalltau(data_matrix[:, 0], data_matrix[:, 1])
            # 对于多个变量，使用scipy的kendalltau
            corr_matrix = np.zeros((len(var_names), len(var_names)))
            p_matrix = np.zeros_like(corr_matrix)
            for i in range(len(var_names)):
                corr_matrix[i, i] = 1.0
                for j in range(i+1, len(var_names)):
                    corr, p = stats.kendalltau(data_matrix[:, i], data_matrix[:, j])
                    corr_matrix[i, j] = corr
                    corr_matrix[j, i] = corr
                    p_matrix[i, j] = p
                    p_matrix[j, i] = p
        else:  # spearman
            corr_matrix, p_matrix = stats.spearmanr(data_matrix[:, 0], data_matrix[:, 1])
            # 对于多个变量，使用scipy的spearmanr
            corr_matrix, p_matrix = stats.spearmanr(data_matrix, axis=0)
        
        # 创建相关矩阵结果
        correlation_result = {
            'variables': var_names,
            'correlation_matrix': corr_matrix.tolist(),
            'p_value_matrix': p_matrix.tolist(),
            'correlation_type': self.correlation_type
        }
        
        self.analysis_results.append(correlation_result)
    
    def _get_variable_data(self, var_name):
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
        
        # 转换为列表
        return list(data)