#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试输出内容查看器
验证 OutputViewer 和 OutputTab 的功能
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from axaltyx.gui.tabs.output_tab import OutputTab

class TestOutputViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("输出内容查看器测试")
        self.setGeometry(100, 100, 1000, 600)
        
        # 创建输出标签页
        self.output_tab = OutputTab(self)
        
        # 设置布局
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.output_tab)
        self.setCentralWidget(central_widget)
        
        # 测试数据
        self._test_outputs()
    
    def _test_outputs(self):
        """测试各种输出类型"""
        # 添加日志
        self.output_tab.add_output_item('log', '分析开始于 2024-01-01 12:00:00')
        
        # 添加标题
        self.output_tab.add_output_item('title', '描述性统计分析')
        
        # 添加文本
        self.output_tab.add_output_item('text', '本分析基于样本数据，包含以下统计量：均值、标准差、方差、全距、最小值、最大值、峰度、偏度、标准误。')
        
        # 添加表格
        headers = ['变量', '均值', '标准差', '方差', '最小值', '最大值']
        rows = [
            ['年龄', '25.4', '3.2', '10.24', '18', '35'],
            ['收入', '5000', '1200', '1440000', '3000', '8000'],
            ['满意度', '4.2', '0.8', '0.64', '1', '5'],
            ['工作年限', '3.5', '1.5', '2.25', '1', '8'],
            ['教育程度', '14.2', '2.1', '4.41', '9', '18']
        ]
        self.output_tab.add_output_item('table', '描述性统计结果', '描述性统计表格', headers, rows)
        
        # 添加图表
        self._add_test_chart()
        
        # 添加日志
        self.output_tab.add_output_item('log', '分析完成于 2024-01-01 12:01:00')
    
    def _add_test_chart(self):
        """添加测试图表"""
        # 创建直方图
        fig, ax = plt.subplots(figsize=(8, 6))
        data = np.random.normal(100, 15, 1000)
        ax.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_title('数据分布直方图')
        ax.set_xlabel('值')
        ax.set_ylabel('频率')
        ax.grid(True, alpha=0.3)
        
        # 添加图表到输出
        self.output_tab.add_output_item('chart', fig, '数据分布直方图')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestOutputViewer()
    window.show()
    sys.exit(app.exec())