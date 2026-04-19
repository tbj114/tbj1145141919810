#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出导航树测试脚本
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit
from PyQt6.QtCore import Qt
from axaltyx.gui.widgets.output_tree import OutputTree


class TestWindow(QMainWindow):
    """测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("输出导航树测试")
        self.resize(800, 600)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建输出树
        self.output_tree = OutputTree()
        self.output_tree.setMinimumWidth(200)
        
        # 创建内容显示区域
        self.content_view = QTextEdit()
        self.content_view.setReadOnly(True)
        
        splitter.addWidget(self.output_tree)
        splitter.addWidget(self.content_view)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        self.setCentralWidget(splitter)
        
        # 连接信号
        self.output_tree.item_selected.connect(self._on_item_selected)
        self.output_tree.item_deleted.connect(self._on_item_deleted)
        self.output_tree.item_exported.connect(self._on_item_exported)
        
        # 添加一些示例数据
        self._add_sample_data()
    
    def _add_sample_data(self):
        """添加示例数据"""
        # 添加日志
        self.output_tree.add_item("分析开始", "log", "log_1")
        self.output_tree.add_item("数据加载成功", "log", "log_2")
        
        # 添加标题
        self.output_tree.add_item("描述性统计", "title", "title_1")
        self.output_tree.add_item("相关性分析", "title", "title_2")
        
        # 添加表格
        self.output_tree.add_item("描述性统计量", "table", "table_1")
        self.output_tree.add_item("相关系数矩阵", "table", "table_2")
        
        # 添加图表
        self.output_tree.add_item("直方图", "chart", "chart_1")
        self.output_tree.add_item("散点图", "chart", "chart_2")
        
        # 添加文本
        self.output_tree.add_item("注释说明", "text", "text_1")
    
    def _on_item_selected(self, content_id):
        """项被选中"""
        content_type = self.output_tree.get_item_content_type(content_id)
        self.content_view.append(f"选中项: {content_id}")
        self.content_view.append(f"类型: {content_type}\n")
    
    def _on_item_deleted(self, content_id):
        """项被删除"""
        self.content_view.append(f"删除项: {content_id}\n")
    
    def _on_item_exported(self, content_id):
        """项被导出"""
        self.content_view.append(f"导出项: {content_id}\n")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
