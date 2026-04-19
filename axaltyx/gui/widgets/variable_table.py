#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
变量表格组件
用于定义和管理变量属性
"""

from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QMenu,
    QHeaderView, QWidget, QVBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from axaltyx.i18n import I18nManager


class VariableTable(QWidget):
    """变量表格组件"""
    
    # 信号定义
    variable_changed = pyqtSignal(int, str, str)  # 索引, 属性, 值
    selection_changed = pyqtSignal()
    
    # 变量类型选项
    VARIABLE_TYPES = [
        'Numeric',
        'String',
        'Date',
        'Boolean',
        'Factor'
    ]
    
    # 测量级别选项
    MEASUREMENT_LEVELS = [
        'Scale',
        'Ordinal',
        'Nominal'
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.dataset = None
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setRowCount(10)
        
        # 设置表头
        headers = [
            self.i18n.t('variable_table.name'),
            self.i18n.t('variable_table.type'),
            self.i18n.t('variable_table.label'),
            self.i18n.t('variable_table.values'),
            self.i18n.t('variable_table.missing'),
            self.i18n.t('variable_table.measurement')
        ]
        self.table.setHorizontalHeaderLabels(headers)
        
        # 设置属性
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QTableWidget.SelectionMode.ContiguousSelection)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # 连接信号
        self.table.cellChanged.connect(self._on_cell_changed)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        
        # 初始化默认数据
        self._init_default_data()
        
        # 设置样式
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E5E6EB;
                border: none;
            }
            QTableWidget::item {
                padding: 4px 8px;
            }
            QTableWidget::item:selected {
                background-color: #E8F3FF;
                color: #165DFF;
            }
            QHeaderView::section {
                background-color: #F7F8FA;
                color: #4E5969;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #E5E6EB;
                font-weight: 500;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #F7F8FA;
                border: none;
                border-bottom: 1px solid #E5E6EB;
            }
        """)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def _init_default_data(self):
        """初始化默认数据"""
        for i in range(10):
            # 变量名称
            name_item = QTableWidgetItem(f'V{i+1}')
            self.table.setItem(i, 0, name_item)
            
            # 类型下拉框
            type_combo = QComboBox()
            type_combo.addItems(self.VARIABLE_TYPES)
            type_combo.setCurrentIndex(0)
            type_combo.currentTextChanged.connect(lambda text, idx=i: self._on_type_changed(idx, text))
            self.table.setCellWidget(i, 1, type_combo)
            
            # 标签
            label_item = QTableWidgetItem('')
            self.table.setItem(i, 2, label_item)
            
            # 值标签
            values_item = QTableWidgetItem('')
            self.table.setItem(i, 3, values_item)
            
            # 缺失值
            missing_item = QTableWidgetItem('')
            self.table.setItem(i, 4, missing_item)
            
            # 测量级别下拉框
            measure_combo = QComboBox()
            measure_combo.addItems(self.MEASUREMENT_LEVELS)
            measure_combo.setCurrentIndex(0)
            measure_combo.currentTextChanged.connect(lambda text, idx=i: self._on_measure_changed(idx, text))
            self.table.setCellWidget(i, 5, measure_combo)
    
    def _on_cell_changed(self, row, column):
        """单元格内容变化事件"""
        headers = ['name', 'type', 'label', 'values', 'missing', 'measurement']
        attr = headers[column] if column < len(headers) else ''
        item = self.table.item(row, column)
        if item and attr:
            value = item.text()
            self.variable_changed.emit(row, attr, value)
    
    def _on_type_changed(self, row, value):
        """类型变化事件"""
        self.variable_changed.emit(row, 'type', value)
    
    def _on_measure_changed(self, row, value):
        """测量级别变化事件"""
        self.variable_changed.emit(row, 'measurement', value)
    
    def _on_selection_changed(self):
        """选择变化事件"""
        self.selection_changed.emit()
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 添加变量
        add_var_above = QAction(self.i18n.t('variable_table.add_above'), self)
        add_var_above.triggered.connect(self._add_variable_above)
        menu.addAction(add_var_above)
        
        add_var_below = QAction(self.i18n.t('variable_table.add_below'), self)
        add_var_below.triggered.connect(self._add_variable_below)
        menu.addAction(add_var_below)
        
        menu.addSeparator()
        
        # 删除变量
        delete_var = QAction(self.i18n.t('variable_table.delete'), self)
        delete_var.triggered.connect(self._delete_selected_variables)
        menu.addAction(delete_var)
        
        menu.exec(self.table.mapToGlobal(pos))
    
    def _add_variable_above(self):
        """在当前选中行上方添加新变量"""
        current_row = self.table.currentRow()
        insert_row = current_row if current_row >= 0 else 0
        self.table.insertRow(insert_row)
        self._init_row(insert_row)
        self._rename_variables()
    
    def _add_variable_below(self):
        """在当前选中行下方添加新变量"""
        current_row = self.table.currentRow()
        insert_row = current_row + 1 if current_row >= 0 else self.table.rowCount()
        self.table.insertRow(insert_row)
        self._init_row(insert_row)
        self._rename_variables()
    
    def _init_row(self, row):
        """初始化一行数据"""
        # 变量名称
        name_item = QTableWidgetItem(f'V{row+1}')
        self.table.setItem(row, 0, name_item)
        
        # 类型下拉框
        type_combo = QComboBox()
        type_combo.addItems(self.VARIABLE_TYPES)
        type_combo.setCurrentIndex(0)
        type_combo.currentTextChanged.connect(lambda text, idx=row: self._on_type_changed(idx, text))
        self.table.setCellWidget(row, 1, type_combo)
        
        # 标签
        label_item = QTableWidgetItem('')
        self.table.setItem(row, 2, label_item)
        
        # 值标签
        values_item = QTableWidgetItem('')
        self.table.setItem(row, 3, values_item)
        
        # 缺失值
        missing_item = QTableWidgetItem('')
        self.table.setItem(row, 4, missing_item)
        
        # 测量级别下拉框
        measure_combo = QComboBox()
        measure_combo.addItems(self.MEASUREMENT_LEVELS)
        measure_combo.setCurrentIndex(0)
        measure_combo.currentTextChanged.connect(lambda text, idx=row: self._on_measure_changed(idx, text))
        self.table.setCellWidget(row, 5, measure_combo)
    
    def _delete_selected_variables(self):
        """删除选中的变量"""
        selected_ranges = self.table.selectedRanges()
        rows_to_delete = []
        for range_ in selected_ranges:
            for row in range(range_.topRow(), range_.bottomRow() + 1):
                if row not in rows_to_delete:
                    rows_to_delete.append(row)
        # 从后往前删除，避免索引问题
        for row in sorted(rows_to_delete, reverse=True):
            self.table.removeRow(row)
        self._rename_variables()
    
    def _rename_variables(self):
        """重新命名变量"""
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item:
                item.setText(f'V{i+1}')
    
    def set_variables(self, variables):
        """设置变量列表"""
        if not variables:
            return
        self.table.setRowCount(len(variables))
        for i, var in enumerate(variables):
            self._init_row(i)
            if 'name' in var:
                item = self.table.item(i, 0)
                if item:
                    item.setText(var['name'])
            if 'type' in var and var['type'] in self.VARIABLE_TYPES:
                combo = self.table.cellWidget(i, 1)
                if combo:
                    combo.setCurrentText(var['type'])
            if 'label' in var:
                item = self.table.item(i, 2)
                if item:
                    item.setText(var['label'])
            if 'values' in var:
                item = self.table.item(i, 3)
                if item:
                    item.setText(str(var['values']))
            if 'missing' in var:
                item = self.table.item(i, 4)
                if item:
                    item.setText(str(var['missing']))
            if 'measurement' in var and var['measurement'] in self.MEASUREMENT_LEVELS:
                combo = self.table.cellWidget(i, 5)
                if combo:
                    combo.setCurrentText(var['measurement'])
    
    def get_variables(self):
        """获取变量列表"""
        variables = []
        for i in range(self.table.rowCount()):
            var = {}
            # 名称
            name_item = self.table.item(i, 0)
            var['name'] = name_item.text() if name_item else f'V{i+1}'
            # 类型
            type_combo = self.table.cellWidget(i, 1)
            var['type'] = type_combo.currentText() if type_combo else 'Numeric'
            # 标签
            label_item = self.table.item(i, 2)
            var['label'] = label_item.text() if label_item else ''
            # 值
            values_item = self.table.item(i, 3)
            var['values'] = values_item.text() if values_item else ''
            # 缺失值
            missing_item = self.table.item(i, 4)
            var['missing'] = missing_item.text() if missing_item else ''
            # 测量级别
            measure_combo = self.table.cellWidget(i, 5)
            var['measurement'] = measure_combo.currentText() if measure_combo else 'Scale'
            variables.append(var)
        return variables
    
    def clear(self):
        """清空表格"""
        self.table.setRowCount(0)
        self.table.setRowCount(10)
        self._init_default_data()
    
    def set_dataset(self, dataset):
        """设置数据集"""
        self.dataset = dataset
        if not dataset:
            return
        
        # 设置行数
        self.table.setRowCount(len(dataset.variables))
        
        # 初始化每一行
        for i, var in enumerate(dataset.variables):
            self._init_row(i)
            
            # 设置变量名称
            name_item = self.table.item(i, 0)
            if name_item:
                name_item.setText(var.name)
            
            # 设置变量类型
            type_combo = self.table.cellWidget(i, 1)
            if type_combo:
                # 转换为我们的类型名称
                var_type = var.type
                type_map = {
                    'numeric': 'Numeric',
                    'string': 'String',
                    'date': 'Date'
                }
                type_combo.setCurrentText(type_map.get(var_type, 'Numeric'))
            
            # 设置标签
            label_item = self.table.item(i, 2)
            if label_item:
                label_item.setText(var.label)
            
            # 设置值标签
            values_item = self.table.item(i, 3)
            if values_item:
                values_str = ', '.join([f'{k}: {v}' for k, v in var.value_labels.items()])
                values_item.setText(values_str)
            
            # 设置测量级别
            measure_combo = self.table.cellWidget(i, 5)
            if measure_combo:
                measure_map = {
                    'scale': 'Scale',
                    'ordinal': 'Ordinal',
                    'nominal': 'Nominal'
                }
                measure_combo.setCurrentText(measure_map.get(var.measure, 'Scale'))
    
    def update_dataset_from_table(self):
        """将表格数据更新回数据集"""
        if not self.dataset:
            return
        
        for i in range(self.table.rowCount()):
            if i >= len(self.dataset.variables):
                continue
            
            var = self.dataset.variables[i]
            
            # 更新名称
            name_item = self.table.item(i, 0)
            if name_item:
                var.name = name_item.text()
            
            # 更新类型
            type_combo = self.table.cellWidget(i, 1)
            if type_combo:
                type_map = {
                    'Numeric': 'numeric',
                    'String': 'string',
                    'Date': 'date',
                    'Boolean': 'numeric',
                    'Factor': 'string'
                }
                var.type = type_map.get(type_combo.currentText(), 'numeric')
            
            # 更新标签
            label_item = self.table.item(i, 2)
            if label_item:
                var.label = label_item.text()
            
            # 更新测量级别
            measure_combo = self.table.cellWidget(i, 5)
            if measure_combo:
                measure_map = {
                    'Scale': 'scale',
                    'Ordinal': 'ordinal',
                    'Nominal': 'nominal'
                }
                var.measure = measure_map.get(measure_combo.currentText(), 'scale')
