#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入测试脚本 - 检查所有模块的导入问题
"""

import sys
import os
import traceback
from collections import defaultdict

sys.path.insert(0, os.path.abspath("."))


def test_import(file_path):
    """尝试动态导入单个模块"""
    try:
        # 转换文件路径为模块名
        module_name = file_path.replace(os.sep, '.')[:-3]  # 去掉.py
        if module_name.startswith('.'):
            module_name = module_name[1:]
        
        # 动态导入
        __import__(module_name)
        return True, None
    except Exception as e:
        return False, traceback.format_exc()


def main():
    print("=" * 80)
    print("AxaltyX 模块导入测试")
    print("=" * 80)
    print()
    
    errors = defaultdict(list)
    success_count = 0
    total_count = 0
    
    # 遍历 axaltyx 目录下所有 Python 文件
    for root, dirs, files in os.walk('axaltyx'):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                total_count += 1
                file_path = os.path.join(root, file)
                
                # 检查文件大小
                if os.path.getsize(file_path) == 0:
                    print(f"⚠️  空文件: {file_path}")
                    continue
                
                # 测试导入
                ok, error_msg = test_import(file_path)
                if ok:
                    success_count += 1
                    print(f"✅ 成功: {file_path}")
                else:
                    errors[file_path].append(error_msg)
                    print(f"❌ 失败: {file_path}")
    
    print()
    print("=" * 80)
    print(f"测试结果: {success_count}/{total_count} 成功")
    print("=" * 80)
    
    if errors:
        print()
        print("=" * 80)
        print("详细错误信息:")
        print("=" * 80)
        for file_path, err_list in errors.items():
            print(f"\n{'='*80}")
            print(f"文件: {file_path}")
            print(f"{'='*80}")
            for err in err_list:
                print(err)
    
    print()
    print("=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == '__main__':
    main()
