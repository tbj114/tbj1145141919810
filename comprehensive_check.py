#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面项目检查脚本
检查语法、导入、空文件等问题
"""

import sys
import os
import ast
import traceback
from collections import defaultdict


def check_file_syntax(file_path):
    """检查单个文件的语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return ('empty', '文件为空')
            ast.parse(content, filename=file_path)
        return ('ok', None)
    except SyntaxError as e:
        return ('syntax_error', f'语法错误: 第{e.lineno}行, {e.msg}')
    except Exception as e:
        return ('error', f'其他错误: {str(e)}')


def check_file_imports(file_path):
    """检查文件的导入语句（仅语法分析）"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content, filename=file_path)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    pass  # 简单记录，不深度检查
            elif isinstance(node, ast.ImportFrom):
                pass
                
    except Exception:
        pass
    return issues


def main():
    print("=" * 70)
    print("AxaltyX 项目全面检查")
    print("=" * 70)
    print()
    
    # 添加项目根目录
    sys.path.insert(0, os.path.abspath("."))
    
    errors = defaultdict(list)
    warnings = defaultdict(list)
    empty_files = []
    
    total_files = 0
    
    # 遍历所有 Python 文件
    print("正在扫描项目文件...")
    for root, dirs, files in os.walk('axaltyx'):
        for file in files:
            if file.endswith('.py'):
                total_files += 1
                file_path = os.path.join(root, file)
                
                status, message = check_file_syntax(file_path)
                
                if status == 'empty':
                    empty_files.append(file_path)
                elif status == 'syntax_error':
                    errors['syntax'].append((file_path, message))
                elif status == 'error':
                    errors['other'].append((file_path, message))
    
    print(f"已扫描 {total_files} 个 Python 文件")
    print()
    
    # 报告空文件
    if empty_files:
        print("=" * 70)
        print(f"⚠️  发现 {len(empty_files)} 个空文件:")
        print("=" * 70)
        for f in empty_files:
            print(f"  - {f}")
        print()
    
    # 报告语法错误
    if errors:
        print("=" * 70)
        print(f"❌ 发现错误:")
        print("=" * 70)
        for error_type, error_list in errors.items():
            print(f"\n{error_type.upper()} ({len(error_list)}):")
            for file_path, msg in error_list:
                print(f"  - {file_path}: {msg}")
        print()
    else:
        print("✅ 未发现语法错误!")
        print()
    
    # 现在检查核心模块的纯导入（不运行GUI）
    print("=" * 70)
    print("检查核心模块结构...")
    print("=" * 70)
    
    # 检查一些关键文件是否存在
    critical_files = [
        'axaltyx/main.py',
        'axaltyx/app.py',
        'axaltyx/gui/main_window.py',
        'axaltyx/gui/splash_screen.py',
        'axaltyx/i18n/__init__.py',
        'axaltyx/i18n/i18n_manager.py',
        'axaltyx/gui/styles/theme_arco.py',
    ]
    
    missing_files = []
    for f in critical_files:
        if not os.path.exists(f):
            missing_files.append(f)
    
    if missing_files:
        print(f"\n❌ 缺失关键文件: {missing_files}")
    else:
        print("\n✅ 关键文件都存在")
    
    # 检查是否有 __init__.py
    print("\n检查包结构...")
    packages_to_check = [
        'axaltyx',
        'axaltyx/core',
        'axaltyx/gui',
        'axaltyx/gui/widgets',
        'axaltyx/gui/dialogs',
        'axaltyx/gui/tabs',
        'axaltyx/i18n',
        'axaltyx/utils',
    ]
    
    ok_packages = []
    problem_packages = []
    for package in packages_to_check:
        init_file = os.path.join(package, '__init__.py')
        if os.path.exists(init_file):
            ok_packages.append(package)
        else:
            problem_packages.append(package)
    
    if problem_packages:
        print(f"\n⚠️  缺失 __init__.py 的包: {problem_packages}")
    else:
        print(f"\n✅ 所有包结构正常: {ok_packages}")
    
    print()
    print("=" * 70)
    print("检查完成")
    print("=" * 70)


if __name__ == '__main__':
    main()
