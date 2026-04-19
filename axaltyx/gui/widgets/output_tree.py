#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出导航树组件
提供输出结果的树形导航功能
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QMenu, QTreeWidgetItem,
    QApplication, QLabel, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction

from axaltyx.gui.widgets.arco_tree import ArcoTree, ArcoTreeItem
from axaltyx.i18n import I18nManager


class OutputTreeItem(ArcoTreeItem):
    """输出树项"""
    
    def __init__(self, parent=None, title="", content_type="", content_id="", icon_key=None):
        super().__init__(parent, icon_key)
        self.setText(title)
        self.content_type = content_type
        self.content_id = content_id
        self.title = title


class OutputTree(QWidget):
    """输出导航树组件"""
    
    # 信号定义
    item_selected = pyqtSignal(str)  # 内容ID
    item_deleted = pyqtSignal(str)   # 内容ID
    item_exported = pyqtSignal(str)  # 内容ID
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        
        # 初始化UI
        self._init_ui()
        
        # 根节点
        self.root_items = {}
        self._create_root_nodes()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题标签
        title_label = QLabel(self.i18n.t("output.output_viewer"))
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #1D2129;
                padding: 8px 16px;
                border-bottom: 1px solid #E5E6EB;
                background-color: white;
            }
        """)
        layout.addWidget(title_label)
        
        # 树形控件
        self.tree = ArcoTree()
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        layout.addWidget(self.tree)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            OutputTree {
                background-color: white;
                border-right: 1px solid #E5E6EB;
            }
        """)
    
    def _create_root_nodes(self):
        """创建根节点"""
        # 日志节点
        log_node = OutputTreeItem(
            title=self.i18n.t("output.log"),
            content_type="log",
            icon_key="log"
        )
        self.root_items["log"] = log_node
        self.tree.addTopLevelItem(log_node)
        
        # 标题节点
        title_node = OutputTreeItem(
            title=self.i18n.t("output.title"),
            content_type="title",
            icon_key="title"
        )
        self.root_items["title"] = title_node
        self.tree.addTopLevelItem(title_node)
        
        # 表格节点
        table_node = OutputTreeItem(
            title=self.i18n.t("output.tables"),
            content_type="table",
            icon_key="table"
        )
        self.root_items["table"] = table_node
        self.tree.addTopLevelItem(table_node)
        
        # 图表节点
        chart_node = OutputTreeItem(
            title=self.i18n.t("output.charts"),
            content_type="chart",
            icon_key="chart"
        )
        self.root_items["chart"] = chart_node
        self.tree.addTopLevelItem(chart_node)
        
        # 文本输出节点
        text_node = OutputTreeItem(
            title=self.i18n.t("output.text_output"),
            content_type="text",
            icon_key="text"
        )
        self.root_items["text"] = text_node
        self.tree.addTopLevelItem(text_node)
        
        # 默认展开所有根节点
        self.tree.expandAll()
    
    def add_item(self, title, content_type, content_id, parent_type=None):
        """
        添加输出项
        
        Args:
            title: 标题
            content_type: 内容类型 (log, title, table, chart, text)
            content_id: 内容唯一标识符
            parent_type: 父节点类型 (可选，默认为同类型)
        """
        # 确定父节点
        if parent_type is None:
            parent_type = content_type
        
        if parent_type not in self.root_items:
            return None
        
        parent_node = self.root_items[parent_type]
        
        # 创建子节点
        item = OutputTreeItem(
            parent=parent_node,
            title=title,
            content_type=content_type,
            content_id=content_id
        )
        
        parent_node.addChild(item)
        parent_node.setExpanded(True)
        
        return item
    
    def remove_item(self, content_id):
        """
        移除输出项
        
        Args:
            content_id: 内容唯一标识符
        """
        def find_item(node):
            """递归查找项"""
            for i in range(node.childCount()):
                child = node.child(i)
                if hasattr(child, "content_id") and child.content_id == content_id:
                    node.removeChild(child)
                    return True
                if find_item(child):
                    return True
            return False
        
        # 在所有根节点下查找
        for root in self.root_items.values():
            if find_item(root):
                break
    
    def clear_all(self):
        """清空所有内容"""
        for root in self.root_items.values():
            root.takeChildren()
    
    def select_item(self, content_id):
        """
        选中指定的项
        
        Args:
            content_id: 内容唯一标识符
        """
        def find_item(node):
            """递归查找项"""
            for i in range(node.childCount()):
                child = node.child(i)
                if hasattr(child, "content_id") and child.content_id == content_id:
                    self.tree.clearSelection()
                    child.setSelected(True)
                    self.tree.scrollToItem(child)
                    return True
                if find_item(child):
                    return True
            return False
        
        # 在所有根节点下查找
        for root in self.root_items.values():
            if find_item(root):
                break
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.tree.itemAt(pos)
        if not item or not hasattr(item, "content_id") or not item.content_id:
            return
        
        menu = QMenu(self)
        
        # 导出项
        export_action = QAction(self.i18n.t("dialogs.common.export"), self)
        export_action.triggered.connect(lambda: self._on_export(item))
        menu.addAction(export_action)
        
        # 删除项
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(lambda: self._on_delete(item))
        menu.addAction(delete_action)
        
        menu.exec(self.tree.mapToGlobal(pos))
    
    def _on_item_clicked(self, item, column):
        """项点击事件"""
        if hasattr(item, "content_id") and item.content_id:
            self.item_selected.emit(item.content_id)
    
    def _on_item_double_clicked(self, item, column):
        """项双击事件"""
        if hasattr(item, "content_id") and item.content_id:
            self.item_selected.emit(item.content_id)
    
    def _on_export(self, item):
        """导出项"""
        if hasattr(item, "content_id") and item.content_id:
            self.item_exported.emit(item.content_id)
    
    def _on_delete(self, item):
        """删除项"""
        if hasattr(item, "content_id") and item.content_id:
            self.item_deleted.emit(item.content_id)
            self.remove_item(item.content_id)
    
    def get_item_content_type(self, content_id):
        """
        获取项的内容类型
        
        Args:
            content_id: 内容唯一标识符
            
        Returns:
            内容类型，找不到返回 None
        """
        def find_item(node):
            """递归查找项"""
            for i in range(node.childCount()):
                child = node.child(i)
                if hasattr(child, "content_id") and child.content_id == content_id:
                    return child.content_type
                result = find_item(child)
                if result is not None:
                    return result
            return None
        
        # 在所有根节点下查找
        for root in self.root_items.values():
            result = find_item(root)
            if result is not None:
                return result
        return None
