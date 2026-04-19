#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试文件 I/O 功能
"""

import os
import tempfile
from axaltyx.utils.file_io import FileIO
from axaltyx.core.data.dataset import Dataset


def test_create_new_dataset():
    """测试创建新数据集"""
    print("=== 测试创建新数据集 ===")
    dataset = FileIO.create_new_dataset()
    print(f"创建的数据集: {dataset.rows}行 x {dataset.cols}列")
    print(f"变量数量: {len(dataset.variables)}")
    print(f"第一个变量名: {dataset.variables[0].name}")
    assert dataset.rows == 100
    assert dataset.cols == 100
    assert len(dataset.variables) == 100
    print("✓ 测试通过")


def test_save_and_load():
    """测试保存和加载数据集"""
    print("\n=== 测试保存和加载数据集 ===")
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.axl', delete=False) as f:
        temp_file = f.name
    
    try:
        # 创建并修改数据集
        dataset = FileIO.create_new_dataset()
        
        # 设置一些数据
        dataset.set_value(0, 0, 100)
        dataset.set_value(1, 1, "test")
        dataset.set_value(2, 2, 3.14)
        
        # 修改变量属性
        dataset.variables[0].name = "age"
        dataset.variables[0].label = "年龄"
        dataset.variables[1].name = "name"
        dataset.variables[1].type = "string"
        
        print(f"保存前: {dataset.rows}行 x {dataset.cols}列")
        print(f"保存前数据: ({dataset.get_value(0, 0)}, {dataset.get_value(1, 1)}, {dataset.get_value(2, 2)}")
        print(f"保存前变量名: {dataset.variables[0].name}, {dataset.variables[1].name}")
        
        # 保存数据集
        success = FileIO.save_dataset(dataset, temp_file)
        assert success, "保存失败"
        print("✓ 保存成功")
        
        # 加载数据集
        loaded_dataset = FileIO.load_dataset(temp_file)
        assert loaded_dataset is not None, "加载失败"
        print(f"加载后: {loaded_dataset.rows}行 x {loaded_dataset.cols}列")
        print(f"加载后数据: ({loaded_dataset.get_value(0, 0)}, {loaded_dataset.get_value(1, 1)}, {loaded_dataset.get_value(2, 2)}")
        print(f"加载后变量名: {loaded_dataset.variables[0].name}, {loaded_dataset.variables[1].name}")
        
        # 验证数据一致性
        assert loaded_dataset.rows == dataset.rows
        assert loaded_dataset.cols == dataset.cols
        assert loaded_dataset.get_value(0, 0) == dataset.get_value(0, 0)
        assert loaded_dataset.get_value(1, 1) == dataset.get_value(1, 1)
        assert loaded_dataset.get_value(2, 2) == dataset.get_value(2, 2)
        assert loaded_dataset.variables[0].name == dataset.variables[0].name
        assert loaded_dataset.variables[0].label == dataset.variables[0].label
        assert loaded_dataset.variables[1].name == dataset.variables[1].name
        assert loaded_dataset.variables[1].type == dataset.variables[1].type
        
        print("✓ 加载成功，数据一致")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_recent_files():
    """测试最近文件列表"""
    print("\n=== 测试最近文件列表 ===")
    
    # 清空最近文件列表
    FileIO.clear_recent_files()
    recent_files = FileIO.get_recent_files()
    print(f"清空后最近文件数量: {len(recent_files)}")
    assert len(recent_files) == 0
    
    # 创建临时文件
    temp_files = []
    for i in range(3):
        with tempfile.NamedTemporaryFile(suffix='.axl', delete=False) as f:
            temp_files.append(f.name)
    
    try:
        # 测试添加最近文件
        for i, temp_file in enumerate(temp_files):
            dataset = FileIO.create_new_dataset()
            FileIO.save_dataset(dataset, temp_file)
            recent_files = FileIO.get_recent_files()
            print(f"添加第{i+1}个文件后: {len(recent_files)}个文件")
            assert len(recent_files) == i + 1
            assert temp_file in recent_files
        
        # 验证最近文件顺序（最新的在最前面）
        recent_files = FileIO.get_recent_files()
        print(f"最近文件顺序: {[os.path.basename(f) for f in recent_files]}")
        assert recent_files[0] == temp_files[2]  # 最后添加的在最前面
        
        print("✓ 最近文件列表测试通过")
        
    finally:
        # 清理临时文件
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


def test_dataset_operations():
    """测试数据集操作"""
    print("\n=== 测试数据集操作 ===")
    dataset = FileIO.create_new_dataset()
    
    # 测试设置和获取值
    dataset.set_value(5, 5, 123)
    value = dataset.get_value(5, 5)
    print(f"设置值: 123, 获取值: {value}")
    assert value == 123
    
    # 测试添加变量
    original_cols = dataset.cols
    new_var_index = dataset.add_variable()
    print(f"添加变量前: {original_cols}列, 添加后: {dataset.cols}列")
    assert dataset.cols == original_cols + 1
    assert new_var_index == original_cols
    
    # 测试删除变量
    dataset.remove_variable(new_var_index)
    print(f"删除变量后: {dataset.cols}列")
    assert dataset.cols == original_cols
    
    # 测试添加行
    original_rows = dataset.rows
    new_row_index = dataset.add_row([1, 2, 3])
    print(f"添加行前: {original_rows}行, 添加后: {dataset.rows}行")
    assert dataset.rows == original_rows + 1
    assert new_row_index == original_rows
    
    # 测试删除行
    dataset.remove_row(new_row_index)
    print(f"删除行后: {dataset.rows}行")
    assert dataset.rows == original_rows
    
    print("✓ 数据集操作测试通过")


if __name__ == "__main__":
    test_create_new_dataset()
    test_dataset_operations()
    test_save_and_load()
    test_recent_files()
    print("\n🎉 所有测试通过！")
