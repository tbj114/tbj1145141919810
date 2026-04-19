#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语法测试输出内容查看器
验证 OutputViewer 和 OutputTab 的代码语法是否正确
"""

import sys

print("测试 OutputViewer 和 OutputTab 的代码语法...")

# 测试代码语法
print("\n1. 测试 OutputViewer 代码...")
try:
    with open('/workspace/axaltyx/gui/widgets/output_viewer.py', 'r') as f:
        content = f.read()
    exec(content)
    print("✓ OutputViewer 代码语法正确")
except Exception as e:
    print(f"✗ OutputViewer 代码语法错误: {e}")
    sys.exit(1)

print("\n2. 测试 OutputTab 代码...")
try:
    with open('/workspace/axaltyx/gui/tabs/output_tab.py', 'r') as f:
        content = f.read()
    exec(content)
    print("✓ OutputTab 代码语法正确")
except Exception as e:
    print(f"✗ OutputTab 代码语法错误: {e}")
    sys.exit(1)

print("\n3. 测试导入语句...")
try:
    # 尝试导入核心模块，不导入 GUI 相关的
    from axaltyx.i18n.i18n_manager import I18nManager
    print("✓ 核心模块导入成功")
except Exception as e:
    print(f"✗ 核心模块导入失败: {e}")
    sys.exit(1)

print("\n✅ 所有语法测试通过！")
print("输出内容查看器代码语法正确。")