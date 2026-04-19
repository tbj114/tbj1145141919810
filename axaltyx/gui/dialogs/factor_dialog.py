#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
因子分析对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QComboBox, QLabel,
                             QRadioButton, QButtonGroup, QSpinBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class FactorDialog(ArcoDialog):
    """因子分析对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化因子分析对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title(self.i18n.t("dialogs.factor.title"))
        self.dataset = dataset
        
        # 初始化参数
        self.rotation_method = "varimax"  # varimax, quartimax, oblimin, promax
        self.extraction_method = "principal_components"  # principal_components, principal_axis, maximum_likelihood
        self.factor_count = 3
        self.display_loadings = True
        self.display_communalities = True
        self.display_eigenvalues = True
        
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
        self.variable_selector.set_available_label(self.i18n.t("dialogs.factor.variables"))
        self.variable_selector.set_selected_label(self.i18n.t("dialogs.factor.analysis_variables"))
        main_layout.addWidget(self.variable_selector, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 提取方法选项
        extraction_widget = QWidget()
        extraction_layout = QVBoxLayout()
        extraction_layout.setSpacing(12)
        
        # 提取方法
        extraction_group = QGroupBox(self.i18n.t("dialogs.factor.extraction_method"))
        extraction_layout_inner = QVBoxLayout()
        
        self.extraction_combo = QComboBox()
        self.extraction_combo.addItems([
            self.i18n.t("dialogs.factor.principal_components"),
            self.i18n.t("dialogs.factor.principal_axis"),
            self.i18n.t("dialogs.factor.maximum_likelihood")
        ])
        self.extraction_combo.currentIndexChanged.connect(self._update_extraction_method)
        extraction_layout_inner.addWidget(self.extraction_combo)
        
        # 因子数量
        factor_count_group = QGroupBox(self.i18n.t("dialogs.factor.factor_count"))
        factor_count_layout = QHBoxLayout()
        
        factor_count_label = QLabel(self.i18n.t("dialogs.factor.number_of_factors") + ":")
        self.factor_count_spin = QSpinBox()
        self.factor_count_spin.setRange(1, 10)
        self.factor_count_spin.setValue(self.factor_count)
        self.factor_count_spin.valueChanged.connect(self._update_factor_count)
        
        factor_count_layout.addWidget(factor_count_label)
        factor_count_layout.addWidget(self.factor_count_spin)
        factor_count_layout.addStretch()
        factor_count_group.setLayout(factor_count_layout)
        extraction_layout_inner.addWidget(factor_count_group)
        
        extraction_group.setLayout(extraction_layout_inner)
        extraction_layout.addWidget(extraction_group)
        
        extraction_widget.setLayout(extraction_layout)
        options_tabs.addTab(extraction_widget, self.i18n.t("dialogs.factor.extraction"))
        
        # 旋转方法选项
        rotation_widget = QWidget()
        rotation_layout = QVBoxLayout()
        rotation_layout.setSpacing(12)
        
        rotation_group = QGroupBox(self.i18n.t("dialogs.factor.rotation_method"))
        rotation_layout_inner = QVBoxLayout()
        
        self.rotation_combo = QComboBox()
        self.rotation_combo.addItems([
            self.i18n.t("dialogs.factor.varimax"),
            self.i18n.t("dialogs.factor.quartimax"),
            self.i18n.t("dialogs.factor.oblimin"),
            self.i18n.t("dialogs.factor.promax")
        ])
        self.rotation_combo.currentIndexChanged.connect(self._update_rotation_method)
        rotation_layout_inner.addWidget(self.rotation_combo)
        
        rotation_group.setLayout(rotation_layout_inner)
        rotation_layout.addWidget(rotation_group)
        
        rotation_widget.setLayout(rotation_layout)
        options_tabs.addTab(rotation_widget, self.i18n.t("dialogs.factor.rotation"))
        
        # 输出选项
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_layout.setSpacing(12)
        
        output_group = QGroupBox(self.i18n.t("dialogs.factor.output"))
        output_check_layout = QVBoxLayout()
        
        self.check_loadings = QCheckBox(self.i18n.t("dialogs.factor.show_factor_loadings"))
        self.check_loadings.setChecked(True)
        self.check_loadings.toggled.connect(self._update_display_loadings)
        
        self.check_communalities = QCheckBox(self.i18n.t("dialogs.factor.show_communalities"))
        self.check_communalities.setChecked(True)
        self.check_communalities.toggled.connect(self._update_display_communalities)
        
        self.check_eigenvalues = QCheckBox(self.i18n.t("dialogs.factor.show_eigenvalues"))
        self.check_eigenvalues.setChecked(True)
        self.check_eigenvalues.toggled.connect(self._update_display_eigenvalues)
        
        output_check_layout.addWidget(self.check_loadings)
        output_check_layout.addWidget(self.check_communalities)
        output_check_layout.addWidget(self.check_eigenvalues)
        
        output_group.setLayout(output_check_layout)
        output_layout.addWidget(output_group)
        
        output_widget.setLayout(output_layout)
        options_tabs.addTab(output_widget, self.i18n.t("dialogs.factor.output"))
        
        main_layout.addWidget(options_tabs, 1)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
        
        # 设置测试数据（如果没有数据集）
        if self.dataset:
            self._set_variables_from_dataset()
        else:
            self._set_demo_data()
    
    def _update_extraction_method(self, index):
        """更新提取方法"""
        methods = ["principal_components", "principal_axis", "maximum_likelihood"]
        self.extraction_method = methods[index]
    
    def _update_rotation_method(self, index):
        """更新旋转方法"""
        methods = ["varimax", "quartimax", "oblimin", "promax"]
        self.rotation_method = methods[index]
    
    def _update_factor_count(self, value):
        """更新因子数量"""
        self.factor_count = value
    
    def _update_display_loadings(self, checked):
        """更新是否显示因子载荷"""
        self.display_loadings = checked
    
    def _update_display_communalities(self, checked):
        """更新是否显示公因子方差"""
        self.display_communalities = checked
    
    def _update_display_eigenvalues(self, checked):
        """更新是否显示特征值"""
        self.display_eigenvalues = checked
    
    def _set_demo_data(self):
        """设置演示数据"""
        demo_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "numeric"),
            ("VAR00003", "numeric"),
            ("VAR00004", "numeric"),
            ("VAR00005", "numeric"),
            ("VAR00006", "numeric"),
            ("VAR00007", "numeric"),
            ("VAR00008", "numeric")
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
        
        # 重置提取方法
        self.extraction_combo.setCurrentIndex(0)
        
        # 重置旋转方法
        self.rotation_combo.setCurrentIndex(0)
        
        # 重置因子数量
        self.factor_count_spin.setValue(3)
        
        # 重置输出选项
        self.check_loadings.setChecked(True)
        self.check_communalities.setChecked(True)
        self.check_eigenvalues.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'factor',
            'results': self.analysis_results,
            'extraction_method': self.extraction_method,
            'rotation_method': self.rotation_method,
            'factor_count': self.factor_count,
            'display_loadings': self.display_loadings,
            'display_communalities': self.display_communalities,
            'display_eigenvalues': self.display_eigenvalues
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _perform_analysis(self):
        """执行因子分析"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        
        if len(selected_variables) < 3:
            return
        
        self.analysis_results = []
        
        # 提取变量名
        var_names = [var[0] for var in selected_variables if var[1] == "numeric"]
        
        if len(var_names) < 3:
            return
        
        # 生成模拟数据
        import numpy as np
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        
        # 生成相关数据
        n_samples = 100
        n_features = len(var_names)
        
        # 创建具有潜在因子结构的数据
        np.random.seed(42)
        
        # 生成3个潜在因子
        factors = np.random.normal(0, 1, size=(n_samples, 3))
        
        # 创建因子载荷矩阵
        loadings = np.random.normal(0, 0.8, size=(n_features, 3))
        
        # 生成观测数据
        X = np.dot(factors, loadings.T) + np.random.normal(0, 0.2, size=(n_samples, n_features))
        
        # 标准化数据
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 执行主成分分析
        pca = PCA(n_components=self.factor_count)
        principal_components = pca.fit_transform(X_scaled)
        
        # 计算因子载荷
        loadings_matrix = pca.components_.T
        
        # 计算特征值
        eigenvalues = pca.explained_variance_
        explained_variance_ratio = pca.explained_variance_ratio_
        
        # 计算公因子方差
        communalities = np.sum(loadings_matrix ** 2, axis=1)
        
        # 创建结果
        factor_result = {
            'variables': var_names,
            'loadings': loadings_matrix.tolist(),
            'eigenvalues': eigenvalues.tolist(),
            'explained_variance_ratio': explained_variance_ratio.tolist(),
            'communalities': communalities.tolist(),
            'factor_count': self.factor_count
        }
        
        self.analysis_results.append(factor_result)