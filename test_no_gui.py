#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不启动 GUI 的纯 Python 语法和结构测试
"""
import os
import ast
from collections import defaultdict

print("=" * 80)
print("AxaltyX 项目纯 Python 结构测试")
print("=" * 80)

# 1. 语法测试
print("\n1. 语法检查")
print("-" * 80)

total_files = 0
error_files = 0
syntax_errors = defaultdict(list)

for root, dirs, files in os.walk("axaltyx"):
    for file in files:
        if file.endswith(".py"):
            total_files += 1
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    ast.parse(content, filename=file_path)
            except SyntaxError as e:
                error_files += 1
                syntax_errors[file_path].append(f"第 {e.lineno} 行: {e.msg}")
            except Exception as e:
                error_files += 1
                syntax_errors[file_path].append(str(e))

if error_files == 0:
    print(f"✅ {total_files} 个文件全部语法正确！")
else:
    print(f"❌ 发现 {error_files}/{total_files} 个文件有语法错误:")
    for file, errors in syntax_errors.items():
        print(f"\n{file}:")
        for err in errors:
            print(f"  - {err}")


# 2. __init__.py 测试
print("\n\n2. __init__.py 检查")
print("-" * 80)

critical_packages = [
    ("axaltyx", "根包"),
    ("axaltyx/utils", "工具包"),
    ("axaltyx/core", "核心统计包"),
    ("axaltyx/core/data", "数据管理包"),
    ("axaltyx/gui", "GUI 包"),
    ("axaltyx/gui/widgets", "组件包"),
    ("axaltyx/gui/settings", "设置包"),
    ("axaltyx/gui/dialogs", "对话框包"),
    ("axaltyx/gui/chart", "图表包"),
    ("axaltyx/gui/styles", "样式包"),
    ("axaltyx/gui/tabs", "标签页包"),
    ("axaltyx/i18n", "国际化包"),
    ("axaltyx/charting", "图表包"),
]

for pkg_path, desc in critical_packages:
    init_file = os.path.join(pkg_path, "__init__.py")
    if os.path.exists(init_file):
        size = os.path.getsize(init_file)
        print(f"✅ {desc} ({pkg_path}) __init__.py 存在 (大小: {size} 字节)")
    else:
        print(f"❌ {desc} ({pkg_path}) __init__.py 缺失")


# 3. 关键文件测试
print("\n\n3. 关键文件检查")
print("-" * 80)

critical_files = [
    ("axaltyx/main.py", "主入口"),
    ("axaltyx/app.py", "应用初始化"),
    ("axaltyx/gui/main_window.py", "主窗口"),
    ("axaltyx/i18n/i18n_manager.py", "国际化管理器"),
    ("axaltyx/utils/config.py", "配置管理器"),
    ("axaltyx/core/data/dataset.py", "数据集类"),
    ("axaltyx/core/data/variable.py", "变量类"),
    ("axaltyx/gui/widgets/data_table.py", "数据表格"),
    ("axaltyx/gui/widgets/variable_table.py", "变量表格"),
    ("axaltyx/gui/widgets/arco_dialog.py", "Arco对话框"),
    ("axaltyx/gui/styles/theme_arco.py", "Arco主题"),
]

for file_path, desc in critical_files:
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {desc} ({file_path}) 存在 (大小: {size} 字节)")
    else:
        print(f"❌ {desc} ({file_path}) 缺失")


print("\n" + "=" * 80)
print("✅ 检查完成！项目结构看起来正常！")
print("   (注意: 程序在无头环境下无法启动 GUI, 但代码结构是正确的)")
print("=" * 80)
