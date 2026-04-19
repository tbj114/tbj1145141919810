#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的导入测试
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath("."))

print("=" * 60)
print("核心模块导入测试")
print("=" * 60)

test_modules = [
    ("app 模块", "axaltyx.app"),
    ("i18n 模块", "axaltyx.i18n"),
    ("utils 模块", "axaltyx.utils"),
    ("core/data 模块", "axaltyx.core.data"),
    ("charting 模块", "axaltyx.charting"),
    ("gui/styles 模块", "axaltyx.gui.styles"),
    ("gui/widgets 模块", "axaltyx.gui.widgets"),
    ("gui/dialogs 模块", "axaltyx.gui.dialogs"),
    ("gui/settings 模块", "axaltyx.gui.settings"),
    ("gui/tabs 模块", "axaltyx.gui.tabs"),
]

success_count = 0
fail_count = 0

for name, module_path in test_modules:
    try:
        print(f"  测试 {name}...", end="")
        __import__(module_path)
        print(" ✅ 成功")
        success_count += 1
    except Exception as e:
        print(f" ❌ 失败: {str(e)}")
        fail_count += 1

print("\n" + "=" * 60)
print(f"结果: {success_count}/{len(test_modules)} 成功")
if fail_count == 0:
    print("✅ 所有核心模块导入成功！")
else:
    print("❌ 有模块导入失败")
print("=" * 60)

print("\n\n" + "=" * 60)
print("关键类导入测试")
print("=" * 60)

test_classes = [
    ("ConfigManager", "axaltyx.utils.config", "ConfigManager"),
    ("I18nManager", "axaltyx.i18n", "I18nManager"),
    ("Dataset", "axaltyx.core.data", "Dataset"),
    ("Variable", "axaltyx.core.data", "Variable"),
    ("ArcoDialog", "axaltyx.gui.widgets", "ArcoDialog"),
    ("SettingsDialog", "axaltyx.gui.settings", "SettingsDialog"),
    ("DataTable", "axaltyx.gui.widgets", "DataTable"),
    ("VariableTable", "axaltyx.gui.widgets", "VariableTable"),
]

success_count_cls = 0
fail_count_cls = 0

for name, module, cls_name in test_classes:
    try:
        print(f"  测试 {name}...", end="")
        mod = __import__(module, fromlist=[cls_name])
        cls = getattr(mod, cls_name)
        print(f" ✅ 成功 (类型: {type(cls)})")
        success_count_cls += 1
    except Exception as e:
        print(f" ❌ 失败: {str(e)}")
        fail_count_cls += 1

print("\n" + "=" * 60)
print(f"结果: {success_count_cls}/{len(test_classes)} 成功")
if fail_count_cls == 0:
    print("✅ 所有关键类导入成功！")
else:
    print("❌ 有关键类导入失败")
print("=" * 60)
