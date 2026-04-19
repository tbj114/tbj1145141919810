#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本测试输出内容查看器
验证 OutputViewer 和 OutputTab 的文件是否存在，以及基本结构是否正确
"""

import os
import sys

print("测试 OutputViewer 和 OutputTab 的基本结构...")

# 检查文件是否存在
files_to_check = [
    '/workspace/axaltyx/gui/widgets/output_viewer.py',
    '/workspace/axaltyx/gui/tabs/output_tab.py',
    '/workspace/axaltyx/gui/widgets/__init__.py',
    '/workspace/axaltyx/gui/tabs/__init__.py'
]

for file_path in files_to_check:
    print(f"\n检查文件: {file_path}")
    if os.path.exists(file_path):
        print(f"✓ 文件存在")
        # 检查文件是否为空
        if os.path.getsize(file_path) > 0:
            print(f"✓ 文件不为空")
        else:
            print(f"✗ 文件为空")
            sys.exit(1)
    else:
        print(f"✗ 文件不存在")
        sys.exit(1)

# 检查文件内容是否包含关键类和方法
print("\n检查 OutputViewer 关键组件...")
try:
    with open('/workspace/axaltyx/gui/widgets/output_viewer.py', 'r') as f:
        content = f.read()
    
    required_components = [
        'class OutputViewer',
        'add_log',
        'add_title',
        'add_text',
        'add_table',
        'add_chart',
        'add_html',
        'clear_content'
    ]
    
    for component in required_components:
        if component in content:
            print(f"✓ 包含 {component}")
        else:
            print(f"✗ 缺少 {component}")
            sys.exit(1)
            
except Exception as e:
    print(f"✗ 检查 OutputViewer 失败: {e}")
    sys.exit(1)

print("\n检查 OutputTab 关键组件...")
try:
    with open('/workspace/axaltyx/gui/tabs/output_tab.py', 'r') as f:
        content = f.read()
    
    required_components = [
        'class OutputTab',
        'add_output_item',
        'clear_output',
        'OutputTree',
        'OutputViewer'
    ]
    
    for component in required_components:
        if component in content:
            print(f"✓ 包含 {component}")
        else:
            print(f"✗ 缺少 {component}")
            sys.exit(1)
            
except Exception as e:
    print(f"✗ 检查 OutputTab 失败: {e}")
    sys.exit(1)

print("\n检查 __init__.py 导出...")
try:
    with open('/workspace/axaltyx/gui/widgets/__init__.py', 'r') as f:
        content = f.read()
    
    if 'OutputViewer' in content:
        print(f"✓ OutputViewer 在 widgets/__init__.py 中导出")
    else:
        print(f"✗ OutputViewer 不在 widgets/__init__.py 中导出")
        sys.exit(1)
        
    with open('/workspace/axaltyx/gui/tabs/__init__.py', 'r') as f:
        content = f.read()
    
    if 'OutputTab' in content:
        print(f"✓ OutputTab 在 tabs/__init__.py 中导出")
    else:
        print(f"✗ OutputTab 不在 tabs/__init__.py 中导出")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ 检查 __init__.py 失败: {e}")
    sys.exit(1)

print("\n✅ 所有基本测试通过！")
print("输出内容查看器文件结构正确。")