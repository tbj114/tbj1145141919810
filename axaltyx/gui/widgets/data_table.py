#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据表格组件
提供数据编辑和显示功能
"""

from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QMenu,
    QHeaderView, QWidget, QVBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from axaltyx.i18n import I18nManager


class DataTable(QWidget):
    """数据表格组件"""
    
    # 信号定义
    cell_changed = pyqtSignal(int, int, str)  # 行, 列, 值
    selection_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setRowCount(100)
        
        # 设置表头
        headers = [f'V{i+1}' for i in range(10)]
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
    
    def _on_cell_changed(self, row, column):
        """单元格内容变化事件"""
        item = self.table.item(row, column)
        if item:
            value = item.text()
            self.cell_changed.emit(row, column, value)
    
    def _on_selection_changed(self):
        """选择变化事件"""
        self.selection_changed.emit()
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 添加行
        add_row_above = QAction(self.i18n.t('data_table.add_row_above'), self)
        add_row_above.triggered.connect(self._add_row_above)
        menu.addAction(add_row_above)
        
        add_row_below = QAction(self.i18n.t('data_table.add_row_below'), self)
        add_row_below.triggered.connect(self._add_row_below)
        menu.addAction(add_row_below)
        
        menu.addSeparator()
        
        # 添加列
        add_col_left = QAction(self.i18n.t('data_table.add_col_left'), self)
        add_col_left.triggered.connect(self._add_col_left)
        menu.addAction(add_col_left)
        
        add_col_right = QAction(self.i18n.t('data_table.add_col_right'), self)
        add_col_right.triggered.connect(self._add_col_right)
        menu.addAction(add_col_right)
        
        menu.addSeparator()
        
        # 删除行/列
        delete_rows = QAction(self.i18n.t('data_table.delete_rows'), self)
        delete_rows.triggered.connect(self._delete_selected_rows)
        menu.addAction(delete_rows)
        
        delete_cols = QAction(self.i18n.t('data_table.delete_cols'), self)
        delete_cols.triggered.connect(self._delete_selected_cols)
        menu.addAction(delete_cols)
        
        menu.addSeparator()
        
        # 复制粘贴
        copy_action = QAction(self.i18n.t('data_table.copy'), self)
        copy_action.triggered.connect(self._copy_selection)
        menu.addAction(copy_action)
        
        paste_action = QAction(self.i18n.t('data_table.paste'), self)
        paste_action.triggered.connect(self._paste_selection)
        menu.addAction(paste_action)
        
        menu.exec(self.table.mapToGlobal(pos))
    
    def _add_row_above(self):
        """在当前选中行上方添加新行"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.insertRow(current_row)
        else:
            self.table.insertRow(0)
    
    def _add_row_below(self):
        """在当前选中行下方添加新行"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.insertRow(current_row + 1)
        else:
            self.table.insertRow(self.table.rowCount())
    
    def _add_col_left(self):
        """在当前选中列左侧添加新列"""
        current_col = self.table.currentColumn()
        if current_col >= 0:
            self.table.insertColumn(current_col)
        else:
            self.table.insertColumn(0)
        # 更新列标题
        self._update_column_headers()
    
    def _add_col_right(self):
        """在当前选中列右侧添加新列"""
        current_col = self.table.currentColumn()
        if current_col >= 0:
            self.table.insertColumn(current_col + 1)
        else:
            self.table.insertColumn(self.table.columnCount())
        self._update_column_headers()
    
    def _delete_selected_rows(self):
        """删除选中的行"""
        selected_ranges = self.table.selectedRanges()
        rows_to_delete = []
        for range_ in selected_ranges:
            for row in range(range_.topRow(), range_.bottomRow() + 1):
                if row not in rows_to_delete:
                    rows_to_delete.append(row)
        # 从后往前删除，避免索引问题
        for row in sorted(rows_to_delete, reverse=True):
            self.table.removeRow(row)
    
    def _delete_selected_cols(self):
        """删除选中的列"""
        selected_ranges = self.table.selectedRanges()
        cols_to_delete = []
        for range_ in selected_ranges:
            for col in range(range_.leftColumn(), range_.rightColumn() + 1):
                if col not in cols_to_delete:
                    cols_to_delete.append(col)
        # 从后往前删除
        for col in sorted(cols_to_delete, reverse=True):
            self.table.removeColumn(col)
        self._update_column_headers()
    
    def _update_column_headers(self):
        """更新列标题"""
        headers = [f'V{i+1}' for i in range(self.table.columnCount())]
        self.table.setHorizontalHeaderLabels(headers)
    
    def _copy_selection(self):
        """复制选中内容"""
        selection = self.table.selectedRanges()
        if not selection:
            return
        # 获取选中区域
        top = min(r.topRow() for r in selection)
        bottom = max(r.bottomRow() for r in selection)
        left = min(r.leftColumn() for r in selection)
        right = max(r.rightColumn() for r in selection)
        # 构建文本
        text = ''
        for row in range(top, bottom + 1):
            row_text = []
            for col in range(left, right + 1):
                item = self.table.item(row, col)
                row_text.append(item.text() if item else '')
            text += '\t'.join(row_text) + '\n'
        # 复制到剪贴板
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(text)
    
    def _paste_selection(self):
        """粘贴内容到表格"""
        from PyQt6.QtWidgets import QApplication
        text = QApplication.clipboard().text()
        if not text:
            return
        # 解析文本
        rows = text.split('\n')
        current_row = self.table.currentRow()
        current_col = self.table.currentColumn()
        if current_row < 0:
            current_row = 0
        if current_col < 0:
            current_col = 0
        # 填充数据
        for i, row_text in enumerate(rows):
            if not row_text.strip():
                continue
            cells = row_text.split('\t')
            for j, cell_text in enumerate(cells):
                target_row = current_row + i
                target_col = current_col + j
                # 确保表格足够大
                while target_row >= self.table.rowCount():
                    self.table.insertRow(self.table.rowCount())
                while target_col >= self.table.columnCount():
                    self.table.insertColumn(self.table.columnCount())
                    self._update_column_headers()
                # 设置单元格内容
                item = QTableWidgetItem(cell_text)
                self.table.setItem(target_row, target_col, item)
    
    def set_data(self, data):
        """设置表格数据"""
        if not data:
            return
        # data 应该是二维列表
        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self._update_column_headers()
        for i in range(rows):
            for j in range(cols):
                if j < len(data[i]):
                    item = QTableWidgetItem(str(data[i][j]))
                    self.table.setItem(i, j, item)
    
    def get_data(self):
        """获取表格数据"""
        data = []
        for i in range(self.table.rowCount()):
            row_data = []
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                row_data.append(item.text() if item else '')
            data.append(row_data)
        return data
    
    def clear(self):
        """清空表格"""
        self.table.setRowCount(0)
        self.table.setColumnCount(10)
        self._update_column_headers()
