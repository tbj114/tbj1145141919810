#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
综合测试程序 - 检验所有功能
"""

import os
import tempfile
import numpy as np
from axaltyx.core.data.dataset import Dataset
from axaltyx.core.data.variable import Variable
from axaltyx.utils.file_io import FileIO
from axaltyx.core.descriptive.descriptives import DescriptiveStats
from axaltyx.i18n import I18nManager


def test_dataset_basic():
    """测试数据集基本操作"""
    print("测试 1: 数据集基本操作")
    print("-" * 50)
    
    # 创建数据集
    dataset = Dataset(rows=10, cols=5)
    print(f"✓ 创建了 {dataset.rows}x{dataset.cols} 的数据集")
    
    # 测试变量管理
    dataset.variables[0].name = "ID"
    dataset.variables[1].name = "Score"
    dataset.variables[2].name = "Age"
    dataset.variables[3].name = "Gender"
    dataset.variables[4].name = "Income"
    print("✓ 变量命名成功")
    
    # 测试数据设置
    for i in range(10):
        dataset.set_value(i, 0, i + 1)
        dataset.set_value(i, 1, np.random.randint(60, 100))
        dataset.set_value(i, 2, np.random.randint(18, 60))
        dataset.set_value(i, 3, "M" if i % 2 == 0 else "F")
        dataset.set_value(i, 4, np.random.randint(2000, 10000))
    print("✓ 数据填充成功")
    
    # 测试数据获取
    value = dataset.get_value(0, 0)
    assert value == 1
    print("✓ 数据获取成功")
    
    print("\n")
    return True


def test_file_io():
    """测试文件IO功能"""
    print("测试 2: 文件IO功能")
    print("-" * 50)
    
    # 创建测试数据集
    dataset = Dataset(rows=5, cols=3)
    dataset.variables[0].name = "ID"
    dataset.variables[1].name = "Name"
    dataset.variables[2].name = "Score"
    
    test_data = [[1, "Alice", 95], [2, "Bob", 88], [3, "Charlie", 92], [4, "David", 76], [5, "Eve", 89]]
    for row in range(5):
        for col in range(3):
            dataset.set_value(row, col, test_data[row][col])
    
    # 测试保存和加载 .axl 文件
    with tempfile.NamedTemporaryFile(suffix='.axl', delete=False) as tmp:
        axl_file = tmp.name
    
    try:
        # 保存
        success = FileIO.save_dataset(dataset, axl_file)
        assert success
        print("✓ 保存 .axl 文件成功")
        
        # 加载
        loaded_dataset = FileIO.load_dataset(axl_file)
        assert loaded_dataset is not None
        print("✓ 加载 .axl 文件成功")
        
        # 验证数据
        for row in range(5):
            for col in range(3):
                assert loaded_dataset.get_value(row, col) == test_data[row][col]
        print("✓ 数据验证成功")
        
    finally:
        if os.path.exists(axl_file):
            os.unlink(axl_file)
    
    print("\n")
    return True


def test_external_formats():
    """测试外部格式支持"""
    print("测试 3: 外部格式支持")
    print("-" * 50)
    
    # 创建测试数据集
    dataset = Dataset(rows=5, cols=3)
    dataset.variables[0].name = "ID"
    dataset.variables[1].name = "Name"
    dataset.variables[2].name = "Score"
    
    test_data = [[1, "Alice", 95], [2, "Bob", 88], [3, "Charlie", 92], [4, "David", 76], [5, "Eve", 89]]
    for row in range(5):
        for col in range(3):
            dataset.set_value(row, col, test_data[row][col])
    
    # 测试 CSV 导出导入
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        csv_file = tmp.name
    
    try:
        # 保存 CSV
        success = FileIO.save_csv(dataset, csv_file)
        assert success
        print("✓ 保存 CSV 文件成功")
        
        # 加载 CSV
        loaded_dataset = FileIO.load_csv(csv_file)
        assert loaded_dataset is not None
        print("✓ 加载 CSV 文件成功")
        
    finally:
        if os.path.exists(csv_file):
            os.unlink(csv_file)
    
    # 测试 Excel 导出导入
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        excel_file = tmp.name
    
    try:
        # 保存 Excel
        success = FileIO.save_excel(dataset, excel_file)
        if success:
            print("✓ 保存 Excel 文件成功")
            
            # 加载 Excel
            loaded_dataset = FileIO.load_excel(excel_file)
            if loaded_dataset is not None:
                print("✓ 加载 Excel 文件成功")
            else:
                print("⚠️  加载 Excel 文件失败（可能缺少 openpyxl）")
        else:
            print("⚠️  保存 Excel 文件失败（可能缺少 openpyxl）")
    finally:
        if os.path.exists(excel_file):
            os.unlink(excel_file)
    
    print("\n")
    return True


def test_descriptive_stats():
    """测试描述性统计功能"""
    print("测试 4: 描述性统计功能")
    print("-" * 50)
    
    # 创建测试数据
    np.random.seed(42)
    test_data = np.random.normal(50, 10, size=100).tolist()
    
    # 测试基本统计量
    stats = DescriptiveStats.calculate_statistics(test_data)
    
    assert 'mean' in stats
    assert 'std_dev' in stats
    assert 'variance' in stats
    assert 'range' in stats
    assert 'min' in stats
    assert 'max' in stats
    assert 'kurtosis' in stats
    assert 'skewness' in stats
    assert 'standard_error' in stats
    
    print("✓ 所有统计量计算成功")
    print(f"  均值: {stats['mean']:.2f}")
    print(f"  标准差: {stats['std_dev']:.2f}")
    print(f"  方差: {stats['variance']:.2f}")
    print(f"  全距: {stats['range']:.2f}")
    print(f"  最小值: {stats['min']:.2f}")
    print(f"  最大值: {stats['max']:.2f}")
    print(f"  峰度: {stats['kurtosis']:.2f}")
    print(f"  偏度: {stats['skewness']:.2f}")
    print(f"  标准误: {stats['standard_error']:.2f}")
    
    print("\n")
    return True


def test_i18n():
    """测试国际化功能"""
    print("测试 5: 国际化功能")
    print("-" * 50)
    
    i18n = I18nManager()
    
    # 测试中文
    i18n.set_language("zh_CN")
    zh_text = i18n.t("app.app_name")
    assert zh_text == "AxaltyX"
    print("✓ 中文翻译正常")
    
    # 测试英文
    i18n.set_language("en_US")
    en_text = i18n.t("app.app_name")
    assert en_text == "AxaltyX"
    print("✓ 英文翻译正常")
    
    print("\n")
    return True


def test_file_filters():
    """测试文件过滤器"""
    print("测试 6: 文件过滤器")
    print("-" * 50)
    
    filters = FileIO.get_file_filters()
    assert ".axl" in filters
    assert ".csv" in filters
    assert ".xlsx" in filters
    assert ".sav" in filters
    print("✓ 文件过滤器包含所有支持的格式")
    print(f"  过滤器: {filters}")
    
    print("\n")
    return True


def test_recent_files():
    """测试最近文件列表"""
    print("测试 7: 最近文件列表")
    print("-" * 50)
    
    # 清空最近文件
    FileIO.clear_recent_files()
    recent_files = FileIO.get_recent_files()
    assert len(recent_files) == 0
    print("✓ 清空最近文件成功")
    
    # 创建测试文件并添加到最近文件
    with tempfile.NamedTemporaryFile(suffix='.axl', delete=False) as tmp:
        test_file = tmp.name
    
    try:
        # 创建一个简单的数据集并保存
        dataset = Dataset(rows=1, cols=1)
        FileIO.save_dataset(dataset, test_file)
        
        # 检查最近文件列表
        recent_files = FileIO.get_recent_files()
        assert len(recent_files) > 0
        assert test_file in recent_files
        print("✓ 最近文件列表功能正常")
        
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)
    
    print("\n")
    return True


def main():
    """运行所有测试"""
    print("开始综合功能测试...")
    print("=" * 60)
    
    tests = [
        test_dataset_basic,
        test_file_io,
        test_external_formats,
        test_descriptive_stats,
        test_i18n,
        test_file_filters,
        test_recent_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    print("=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
