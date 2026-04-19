#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AST 分析导入 - 不实际运行代码，只分析导入结构
"""

import os
import ast
from collections import defaultdict


def analyze_file_imports(file_path):
    """分析单个文件的导入"""
    imports = {
        'absolute': [],
        'relative': [],
        'from_imports': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return imports, 'empty'
            
            tree = ast.parse(content, filename=file_path)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports['absolute'].append(name.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                level = node.level
                for name in node.names:
                    if level > 0:
                        imports['relative'].append(f"{'.'*level}{module or ''}.{name.name}")
                    else:
                        imports['from_imports'].append(f"{module}.{name.name}")
        
        return imports, 'ok'
    except Exception as e:
        return imports, str(e)


def check_module_exists(module_name, project_root):
    """检查项目内模块是否存在"""
    # 转换模块名为路径
    module_path = module_name.replace('.', os.sep)
    
    # 检查是否是包 (带 __init__.py 的目录)
    package_path = os.path.join(project_root, module_path, '__init__.py')
    if os.path.exists(package_path):
        return True
    
    # 检查是否是 .py 文件
    file_path = os.path.join(project_root, module_path + '.py')
    if os.path.exists(file_path):
        return True
    
    return False


def main():
    print("=" * 80)
    print("AxaltyX 导入关系分析")
    print("=" * 80)
    print()
    
    project_root = '/workspace'
    all_imports = defaultdict(dict)
    missing_modules = defaultdict(list)
    
    total_files = 0
    
    # 遍历所有文件
    for root, dirs, files in os.walk(os.path.join(project_root, 'axaltyx')):
        for file in files:
            if file.endswith('.py'):
                total_files += 1
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_root)
                
                imports, status = analyze_file_imports(file_path)
                
                if status == 'empty':
                    print(f"⚠️  空文件: {rel_path}")
                    continue
                elif status != 'ok':
                    print(f"❌ 分析失败: {rel_path}: {status}")
                    continue
                
                all_imports[rel_path] = imports
                
                # 检查项目内导入的模块是否存在
                for imp in imports['absolute'] + imports['from_imports']:
                    if imp.startswith('axaltyx.'):
                        # 项目内模块
                        if not check_module_exists(imp, project_root):
                            missing_modules[rel_path].append(imp)
    
    print()
    print("=" * 80)
    print(f"已分析 {total_files} 个文件")
    print("=" * 80)
    
    if missing_modules:
        print()
        print("=" * 80)
        print("⚠️  发现可能缺失的模块:")
        print("=" * 80)
        for file_path, mods in missing_modules.items():
            print(f"\n{file_path}:")
            for mod in mods:
                print(f"  - {mod}")
    
    print()
    print("=" * 80)
    print("现在检查关键入口点 (main.py, app.py) 的实际导入:")
    print("=" * 80)
    
    # 尝试静态分析 main.py 的问题
    main_file = os.path.join(project_root, 'axaltyx', 'main.py')
    app_file = os.path.join(project_root, 'axaltyx', 'app.py')
    
    import sys
    import traceback
    sys.path.insert(0, project_root)
    
    print("\n1. 尝试导入 app.py ...")
    try:
        from axaltyx.app import AxaltyXApp, create_app
        print("✅ 成功")
    except Exception as e:
        print(f"❌ 失败: {e}")
        print(traceback.format_exc())
    
    print("\n2. 尝试导入 i18n 模块 ...")
    try:
        from axaltyx.i18n import I18nManager
        print("✅ 成功")
    except Exception as e:
        print(f"❌ 失败: {e}")
        print(traceback.format_exc())
    
    print("\n3. 尝试导入 gui 基础模块 ...")
    try:
        from axaltyx.gui.styles.theme_arco import apply_theme
        print("✅ 成功")
    except Exception as e:
        print(f"❌ 失败: {e}")
        print(traceback.format_exc())
    
    print("\n4. 检查 main_window.py ...")
    try:
        print("   不直接导入 main_window.py，先查看文件内容...")
        with open(os.path.join(project_root, 'axaltyx', 'gui', 'main_window.py'), 'r', encoding='utf-8') as f:
            print("   ✅ 文件可读")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    
    print()
    print("=" * 80)
    print("分析完成")
    print("=" * 80)


if __name__ == '__main__':
    main()
