#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
语法检查脚本
验证代码语法和导入是否正确
"""

import sys
import os

print("开始语法检查...")
print("=" * 50)

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath("."))

# 1. 检查SplashScreen类
print("检查 SplashScreen 类...")
try:
    from axaltyx.gui.splash_screen import SplashScreen
    # 检查是否存在update_progress方法
    if hasattr(SplashScreen, 'update_progress'):
        print("✓ SplashScreen.update_progress 方法存在")
    else:
        print("❌ SplashScreen.update_progress 方法不存在")
        sys.exit(1)
except Exception as e:
    print(f"❌ 导入 SplashScreen 失败: {e}")
    sys.exit(1)

# 2. 检查main.py导入
print("检查 main.py 导入...")
try:
    from axaltyx.main import main
    print("✓ main.py 导入成功")
except Exception as e:
    print(f"❌ main.py 导入失败: {e}")
    sys.exit(1)

# 3. 检查其他核心模块
print("检查核心模块...")
try:
    from axaltyx.app import create_app
    from axaltyx.i18n import I18nManager
    from axaltyx.gui.main_window import MainWindow
    print("✓ 核心模块导入成功")
except Exception as e:
    print(f"❌ 核心模块导入失败: {e}")
    sys.exit(1)

print("=" * 50)
print("🎉 语法检查通过！")
print("SplashScreen.update_progress 方法已成功添加")
print("所有模块导入正常")
