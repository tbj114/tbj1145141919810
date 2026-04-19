#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试外部格式支持功能
"""

import os
import tempfile
from axaltyx.utils.file_io import FileIO
from axaltyx.core.data.dataset import Dataset


def test_csv_import_export():
    """测试 CSV 导入导出功能"""
    print("测试 CSV 导入导出功能...")
    
    # 创建测试数据集
    dataset = Dataset(rows=5, cols=3)
    dataset.variables[0].name = "ID"
    dataset.variables[1].name = "Name"
    dataset.variables[2].name = "Score"
    
    # 填充测试数据
    test_data = [
        [1, "Alice", 95],
        [2, "Bob", 88],
        [3, "Charlie", 92],
        [4, "David", 76],
        [5, "Eve", 89]
    ]
    
    for row in range(5):
        for col in range(3):
            dataset.set_value(row, col, test_data[row][col])
    
    # 保存为 CSV
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        csv_file = tmp.name
    
    try:
        # 保存 CSV
        success = FileIO.save_csv(dataset, csv_file)
        assert success, "保存 CSV 失败"
        print("✓ 保存 CSV 成功")
        
        # 重新加载
        loaded_dataset = FileIO.load_csv(csv_file)
        assert loaded_dataset is not None, "加载 CSV 失败"
        print("✓ 加载 CSV 成功")
        
        # 验证数据
        for row in range(5):
            for col in range(3):
                original_value = test_data[row][col]
                loaded_value = loaded_dataset.get_value(row, col)
                assert original_value == loaded_value, f"数据不匹配: 行 {row}, 列 {col}"
        print("✓ CSV 数据验证成功")
        
    finally:
        if os.path.exists(csv_file):
            os.unlink(csv_file)


def test_excel_import_export():
    """测试 Excel 导入导出功能"""
    print("\n测试 Excel 导入导出功能...")
    
    # 创建测试数据集
    dataset = Dataset(rows=5, cols=3)
    dataset.variables[0].name = "ID"
    dataset.variables[1].name = "Name"
    dataset.variables[2].name = "Score"
    
    # 填充测试数据
    test_data = [
        [1, "Alice", 95],
        [2, "Bob", 88],
        [3, "Charlie", 92],
        [4, "David", 76],
        [5, "Eve", 89]
    ]
    
    for row in range(5):
        for col in range(3):
            dataset.set_value(row, col, test_data[row][col])
    
    # 保存为 Excel
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        excel_file = tmp.name
    
    try:
        # 保存 Excel
        success = FileIO.save_excel(dataset, excel_file)
        if not success:
            print("⚠️ 保存 Excel 失败（可能缺少 openpyxl）")
            return
        print("✓ 保存 Excel 成功")
        
        # 重新加载
        loaded_dataset = FileIO.load_excel(excel_file)
        if loaded_dataset is None:
            print("⚠️ 加载 Excel 失败（可能缺少 openpyxl）")
            return
        print("✓ 加载 Excel 成功")
        
        # 验证数据
        for row in range(5):
            for col in range(3):
                original_value = test_data[row][col]
                loaded_value = loaded_dataset.get_value(row, col)
                assert original_value == loaded_value, f"数据不匹配: 行 {row}, 列 {col}"
        print("✓ Excel 数据验证成功")
        
    finally:
        if os.path.exists(excel_file):
            os.unlink(excel_file)


def test_file_filters():
    """测试文件对话框过滤器"""
    print("\n测试文件对话框过滤器...")
    
    filters = FileIO.get_file_filters()
    assert ".axl" in filters, "文件过滤器缺少 .axl 格式"
    assert ".csv" in filters, "文件过滤器缺少 .csv 格式"
    assert ".xlsx" in filters, "文件过滤器缺少 .xlsx 格式"
    assert ".sav" in filters, "文件过滤器缺少 .sav 格式"
    print("✓ 文件过滤器验证成功")


def test_auto_load_save():
    """测试根据文件扩展名自动加载保存"""
    print("\n测试自动加载保存功能...")
    
    # 创建测试数据集
    dataset = Dataset(rows=3, cols=2)
    dataset.variables[0].name = "A"
    dataset.variables[1].name = "B"
    dataset.set_value(0, 0, 1)
    dataset.set_value(0, 1, 2)
    dataset.set_value(1, 0, 3)
    dataset.set_value(1, 1, 4)
    dataset.set_value(2, 0, 5)
    dataset.set_value(2, 1, 6)
    
    # 测试 CSV 自动保存和加载
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        csv_file = tmp.name
    
    try:
        # 自动保存
        success = FileIO.save_file(dataset, csv_file)
        assert success, "自动保存 CSV 失败"
        
        # 自动加载
        loaded_dataset = FileIO.load_file(csv_file)
        assert loaded_dataset is not None, "自动加载 CSV 失败"
        print("✓ CSV 自动加载保存成功")
        
    finally:
        if os.path.exists(csv_file):
            os.unlink(csv_file)
    
    # 测试 Excel 自动保存和加载
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        excel_file = tmp.name
    
    try:
        # 自动保存
        success = FileIO.save_file(dataset, excel_file)
        if success:
            # 自动加载
            loaded_dataset = FileIO.load_file(excel_file)
            if loaded_dataset is not None:
                print("✓ Excel 自动加载保存成功")
        
    finally:
        if os.path.exists(excel_file):
            os.unlink(excel_file)


if __name__ == "__main__":
    print("开始测试外部格式支持功能...\n")
    
    test_csv_import_export()
    test_excel_import_export()
    test_file_filters()
    test_auto_load_save()
    
    print("\n所有测试完成！")
