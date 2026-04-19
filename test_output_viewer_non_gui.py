#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
非 GUI 测试输出内容查看器
验证 OutputViewer 和 OutputTab 的代码是否正确
"""

import sys
import matplotlib.pyplot as plt
import numpy as np

# 测试导入
print("测试导入 OutputViewer 和 OutputTab...")
try:
    from axaltyx.gui.widgets.output_viewer import OutputViewer
    from axaltyx.gui.tabs.output_tab import OutputTab
    print("✓ 导入成功")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

# 测试 OutputViewer 类
print("\n测试 OutputViewer 类...")
try:
    # 不显示 GUI，只测试初始化
    viewer = OutputViewer(parent=None)
    print("✓ OutputViewer 初始化成功")
    
    # 测试方法
    print("  测试 clear_content 方法...")
    viewer.clear_content()
    print("  ✓ clear_content 方法执行成功")
    
    print("  测试 add_log 方法...")
    viewer.add_log("测试日志")
    print("  ✓ add_log 方法执行成功")
    
    print("  测试 add_title 方法...")
    viewer.add_title("测试标题")
    print("  ✓ add_title 方法执行成功")
    
    print("  测试 add_text 方法...")
    viewer.add_text("测试文本")
    print("  ✓ add_text 方法执行成功")
    
    print("  测试 add_table 方法...")
    headers = ['变量', '值']
    rows = [['测试', '123']]
    viewer.add_table(headers, rows)
    print("  ✓ add_table 方法执行成功")
    
    print("  测试 add_chart 方法...")
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    viewer.add_chart(fig)
    print("  ✓ add_chart 方法执行成功")
    
    print("  测试 add_html 方法...")
    viewer.add_html("<p>测试 HTML</p>")
    print("  ✓ add_html 方法执行成功")
    
except Exception as e:
    print(f"✗ OutputViewer 测试失败: {e}")
    sys.exit(1)

# 测试 OutputTab 类
print("\n测试 OutputTab 类...")
try:
    # 不显示 GUI，只测试初始化
    tab = OutputTab(parent=None)
    print("✓ OutputTab 初始化成功")
    
    # 测试方法
    print("  测试 clear_output 方法...")
    tab.clear_output()
    print("  ✓ clear_output 方法执行成功")
    
    print("  测试 add_output_item 方法...")
    # 添加日志
    item1 = tab.add_output_item('log', '测试日志')
    print("  ✓ add_output_item (log) 执行成功")
    
    # 添加标题
    item2 = tab.add_output_item('title', '测试标题')
    print("  ✓ add_output_item (title) 执行成功")
    
    # 添加文本
    item3 = tab.add_output_item('text', '测试文本')
    print("  ✓ add_output_item (text) 执行成功")
    
    # 添加表格
    headers = ['变量', '值']
    rows = [['测试', '123']]
    item4 = tab.add_output_item('table', '测试表格', '测试表格标题', headers, rows)
    print("  ✓ add_output_item (table) 执行成功")
    
    # 添加图表
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    item5 = tab.add_output_item('chart', fig, '测试图表')
    print("  ✓ add_output_item (chart) 执行成功")
    
except Exception as e:
    print(f"✗ OutputTab 测试失败: {e}")
    sys.exit(1)

print("\n✅ 所有测试通过！")
print("输出内容查看器功能正常。")