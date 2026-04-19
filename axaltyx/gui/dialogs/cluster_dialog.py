#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
聚类分析对话框实现
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QCheckBox, QGroupBox,
                             QDialog, QTabWidget, QComboBox, QLabel,
                             QRadioButton, QButtonGroup, QSpinBox)
from PyQt6.QtCore import pyqtSignal
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.i18n import I18nManager


class ClusterDialog(ArcoDialog):
    """聚类分析对话框"""
    
    analysis_completed = pyqtSignal(dict)  # 分析完成信号
    
    def __init__(self, parent=None, dataset=None):
        """
        初始化聚类分析对话框
        
        Args:
            parent: 父窗口
            dataset: 数据集对象
        """
        super().__init__(parent, "", 700, 550)
        self.i18n = I18nManager()
        self.set_title("聚类分析")
        self.dataset = dataset
        
        # 初始化参数
        self.cluster_method = "kmeans"  # kmeans, hierarchical, dbscan
        self.cluster_count = 3
        self.distance_method = "euclidean"  # euclidean, manhattan, cosine
        self.standardize_variables = True
        
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
        self.variable_selector.set_selected_label("聚类变量")
        main_layout.addWidget(self.variable_selector, 2)
        
        # 选项标签页
        options_tabs = QTabWidget()
        
        # 聚类方法选项
        method_widget = QWidget()
        method_layout = QVBoxLayout()
        method_layout.setSpacing(12)
        
        # 聚类方法
        method_group = QGroupBox("聚类方法")
        method_button_group = QButtonGroup()
        method_button_layout = QVBoxLayout()
        
        self.radio_kmeans = QRadioButton("K-均值聚类")
        self.radio_kmeans.setChecked(True)
        self.radio_hierarchical = QRadioButton("层次聚类")
        self.radio_dbscan = QRadioButton("DBSCAN聚类")
        
        method_button_group.addButton(self.radio_kmeans)
        method_button_group.addButton(self.radio_hierarchical)
        method_button_group.addButton(self.radio_dbscan)
        
        method_button_layout.addWidget(self.radio_kmeans)
        method_button_layout.addWidget(self.radio_hierarchical)
        method_button_layout.addWidget(self.radio_dbscan)
        
        method_group.setLayout(method_button_layout)
        method_layout.addWidget(method_group)
        
        # 聚类数量
        cluster_count_group = QGroupBox("聚类数量")
        cluster_count_layout = QHBoxLayout()
        
        cluster_count_label = QLabel("聚类数:")
        self.cluster_count_spin = QSpinBox()
        self.cluster_count_spin.setRange(2, 10)
        self.cluster_count_spin.setValue(self.cluster_count)
        self.cluster_count_spin.valueChanged.connect(self._update_cluster_count)
        
        cluster_count_layout.addWidget(cluster_count_label)
        cluster_count_layout.addWidget(self.cluster_count_spin)
        cluster_count_layout.addStretch()
        cluster_count_group.setLayout(cluster_count_layout)
        method_layout.addWidget(cluster_count_group)
        
        method_widget.setLayout(method_layout)
        options_tabs.addTab(method_widget, "聚类方法")
        
        # 距离和标准化选项
        distance_widget = QWidget()
        distance_layout = QVBoxLayout()
        distance_layout.setSpacing(12)
        
        # 距离方法
        distance_group = QGroupBox("距离方法")
        distance_combo_layout = QVBoxLayout()
        
        self.distance_combo = QComboBox()
        self.distance_combo.addItems(["欧几里得距离", "曼哈顿距离", "余弦距离"])
        self.distance_combo.currentIndexChanged.connect(self._update_distance_method)
        distance_combo_layout.addWidget(self.distance_combo)
        
        distance_group.setLayout(distance_combo_layout)
        distance_layout.addWidget(distance_group)
        
        # 标准化选项
        standardize_group = QGroupBox("数据处理")
        standardize_layout = QVBoxLayout()
        
        self.check_standardize = QCheckBox("标准化变量")
        self.check_standardize.setChecked(True)
        self.check_standardize.toggled.connect(self._update_standardize)
        standardize_layout.addWidget(self.check_standardize)
        
        standardize_group.setLayout(standardize_layout)
        distance_layout.addWidget(standardize_group)
        
        distance_widget.setLayout(distance_layout)
        options_tabs.addTab(distance_widget, "距离和标准化")
        
        main_layout.addWidget(options_tabs, 1)
        
        # 设置内容布局
        self.set_content_layout(main_layout)
        
        # 设置测试数据（如果没有数据集）
        if self.dataset:
            self._set_variables_from_dataset()
        else:
            self._set_demo_data()
    
    def _update_cluster_count(self, value):
        """更新聚类数量"""
        self.cluster_count = value
    
    def _update_distance_method(self, index):
        """更新距离方法"""
        methods = ["euclidean", "manhattan", "cosine"]
        self.distance_method = methods[index]
    
    def _update_standardize(self, checked):
        """更新是否标准化变量"""
        self.standardize_variables = checked
    
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
        
        # 重置聚类方法
        self.radio_kmeans.setChecked(True)
        
        # 重置聚类数量
        self.cluster_count_spin.setValue(3)
        
        # 重置距离方法
        self.distance_combo.setCurrentIndex(0)
        
        # 重置标准化选项
        self.check_standardize.setChecked(True)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        # 执行分析
        self._perform_analysis()
        
        # 发送分析完成信号
        result_data = {
            'analysis_type': 'cluster',
            'results': self.analysis_results,
            'cluster_method': self._get_selected_cluster_method(),
            'cluster_count': self.cluster_count,
            'distance_method': self.distance_method,
            'standardize_variables': self.standardize_variables
        }
        self.analysis_completed.emit(result_data)
        
        # 关闭对话框
        self.accept()
    
    def _get_selected_cluster_method(self):
        """获取选中的聚类方法"""
        if self.radio_kmeans.isChecked():
            return "kmeans"
        elif self.radio_hierarchical.isChecked():
            return "hierarchical"
        else:
            return "dbscan"
    
    def _perform_analysis(self):
        """执行聚类分析"""
        # 获取选中的变量
        selected_variables = self.get_selected_variables()
        
        if len(selected_variables) < 2:
            return
        
        self.analysis_results = []
        
        # 提取变量名和数据
        var_names = [var[0] for var in selected_variables if var[1] == "numeric"]
        
        if len(var_names) < 2:
            return
        
        # 生成模拟数据
        import numpy as np
        from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
        from sklearn.preprocessing import StandardScaler
        
        # 生成聚类数据
        n_samples = 100
        n_features = len(var_names)
        
        # 创建具有明显聚类结构的数据
        np.random.seed(42)
        
        # 生成3个聚类中心
        centers = np.array([
            [20, 30, 40, 50, 60][:n_features],
            [50, 50, 50, 50, 50][:n_features],
            [80, 70, 60, 50, 40][:n_features]
        ])
        
        # 生成数据
        X = []
        for i in range(3):
            cluster_data = centers[i] + np.random.normal(0, 10, size=(n_samples//3, n_features))
            X.append(cluster_data)
        X = np.vstack(X)
        
        # 标准化数据
        if self.standardize_variables:
            scaler = StandardScaler()
            X = scaler.fit_transform(X)
        
        # 执行聚类
        cluster_method = self._get_selected_cluster_method()
        
        if cluster_method == "kmeans":
            model = KMeans(n_clusters=self.cluster_count, random_state=42)
            labels = model.fit_predict(X)
            centers = model.cluster_centers_
        elif cluster_method == "hierarchical":
            model = AgglomerativeClustering(n_clusters=self.cluster_count)
            labels = model.fit_predict(X)
            centers = None
        else:  # dbscan
            model = DBSCAN(eps=0.5, min_samples=5)
            labels = model.fit_predict(X)
            centers = None
        
        # 计算聚类统计信息
        cluster_stats = {}
        for i in range(len(set(labels))):
            cluster_data = X[labels == i]
            cluster_stats[i] = {
                'size': len(cluster_data),
                'mean': cluster_data.mean(axis=0).tolist(),
                'std': cluster_data.std(axis=0).tolist()
            }
        
        # 创建结果
        cluster_result = {
            'variables': var_names,
            'cluster_method': cluster_method,
            'cluster_count': len(set(labels)),
            'labels': labels.tolist(),
            'cluster_stats': cluster_stats,
            'centers': centers.tolist() if centers is not None else None
        }
        
        self.analysis_results.append(cluster_result)