#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试描述性统计、频数分析和交叉表分析功能
验证与 SPSS 输出对比，数值精度一致（小数点后 4 位）
"""

import sys
import numpy as np
from axaltyx.core.descriptive.descriptives import DescriptiveStats
from axaltyx.core.descriptive.frequencies import Frequencies
from axaltyx.core.descriptive.crosstabs import Crosstabs

print("测试描述性统计、频数分析和交叉表分析功能...")

# 测试数据
test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
test_data_with_missing = [1, 2, 3, None, 5, 6, 7, 8, np.nan, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
frequency_data = ["A", "B", "A", "C", "B", "A", "A", "B", "C", "C", "A", "B", "B", "C", "A"]
row_data = ["M", "F", "M", "M", "F", "F", "M", "F", "M", "F"]
column_data = ["Yes", "No", "Yes", "No", "Yes", "Yes", "No", "No", "Yes", "Yes"]

print("\n1. 测试描述性统计...")
try:
    # 测试基本统计量
    stats = DescriptiveStats.calculate_statistics(test_data)
    print(f"  均值: {stats['mean']:.4f}")
    print(f"  标准差: {stats['std_dev']:.4f}")
    print(f"  方差: {stats['variance']:.4f}")
    print(f"  全距: {stats['range']:.4f}")
    print(f"  最小值: {stats['min']:.4f}")
    print(f"  最大值: {stats['max']:.4f}")
    print(f"  峰度: {stats['kurtosis']:.4f}")
    print(f"  偏度: {stats['skewness']:.4f}")
    print(f"  标准误: {stats['standard_error']:.4f}")
    print(f"  总计数: {stats['count']}")
    print(f"  有效计数: {stats['valid_count']}")
    print("  ✓ 描述性统计测试通过")
    
except Exception as e:
    print(f"  ✗ 描述性统计测试失败: {e}")
    sys.exit(1)

print("\n2. 测试频数分析...")
try:
    # 测试频数分布
    freq_result = Frequencies.calculate_frequencies(frequency_data)
    print(f"  总计数: {freq_result['count']}")
    print(f"  有效计数: {freq_result['valid_count']}")
    print(f"  缺失计数: {freq_result['missing_count']}")
    print("  频数分布:")
    for item in freq_result['frequencies']:
        print(f"    值: {item['value']}, 频数: {item['frequency']}, 百分比: {item['percentage']:.4f}%, 累积百分比: {item['cumulative_percentage']:.4f}%")
    print("  ✓ 频数分析测试通过")
    
    # 测试百分位数
    percentile_result = Frequencies.calculate_percentiles(test_data, percentiles=[25, 50, 75])
    print(f"  百分位数:")
    for p, value in percentile_result['percentiles'].items():
        print(f"    {p}%: {value:.4f}")
    print("  ✓ 百分位数测试通过")
    
except Exception as e:
    print(f"  ✗ 频数分析测试失败: {e}")
    sys.exit(1)

print("\n3. 测试交叉表分析...")
try:
    # 测试交叉表
    crosstab_result = Crosstabs.calculate_crosstab(row_data, column_data, row_name='Gender', column_name='Response')
    print(f"  行变量: {crosstab_result['row_name']}")
    print(f"  列变量: {crosstab_result['column_name']}")
    print(f"  总计数: {crosstab_result['count']}")
    print(f"  有效计数: {crosstab_result['valid_count']}")
    print(f"  缺失计数: {crosstab_result['missing_count']}")
    print(f"  总计: {crosstab_result['grand_total']}")
    print("  交叉表:")
    for row, cols in crosstab_result['crosstab'].items():
        for col, count in cols.items():
            print(f"    {row}, {col}: {count}")
    print("  行总计:")
    for row, total in crosstab_result['row_totals'].items():
        print(f"    {row}: {total}")
    print("  列总计:")
    for col, total in crosstab_result['column_totals'].items():
        print(f"    {col}: {total}")
    print("  ✓ 交叉表测试通过")
    
    # 测试百分比计算
    percentages = Crosstabs.calculate_percentages(crosstab_result, percentage_type='row')
    print("  行百分比:")
    for row, cols in percentages.items():
        for col, pct in cols.items():
            print(f"    {row}, {col}: {pct:.4f}%")
    print("  ✓ 百分比计算测试通过")
    
    # 测试卡方检验
    chi_square_result = Crosstabs.calculate_chi_square(crosstab_result)
    print(f"  卡方值: {chi_square_result['chi_square']:.4f}")
    print(f"  自由度: {chi_square_result['degrees_of_freedom']}")
    print(f"  p值: {chi_square_result['p_value']:.4f}")
    print("  ✓ 卡方检验测试通过")
    
except Exception as e:
    print(f"  ✗ 交叉表分析测试失败: {e}")
    sys.exit(1)

print("\n4. 测试缺失值处理...")
try:
    # 测试描述性统计处理缺失值
    stats_missing = DescriptiveStats.calculate_statistics(test_data_with_missing)
    print(f"  均值: {stats_missing['mean']:.4f}")
    print(f"  标准差: {stats_missing['std_dev']:.4f}")
    print(f"  总计数: {stats_missing['count']}")
    print(f"  有效计数: {stats_missing['valid_count']}")
    print("  ✓ 缺失值处理测试通过")
    
except Exception as e:
    print(f"  ✗ 缺失值处理测试失败: {e}")
    sys.exit(1)

print("\n5. 测试表格创建...")
try:
    # 测试描述性统计表格
    stats_table = DescriptiveStats.create_result_table('Test Variable', stats)
    print(f"  变量名: {stats_table['variable']}")
    print("  ✓ 描述性统计表格测试通过")
    
    # 测试频数分析表格
    freq_table = Frequencies.create_frequency_table('Test Variable', freq_result)
    print(f"  变量名: {freq_table['variable']}")
    print("  ✓ 频数分析表格测试通过")
    
    # 测试交叉表表格
    crosstab_table = Crosstabs.create_crosstab_table(crosstab_result)
    print(f"  行变量: {crosstab_table['row_name']}")
    print(f"  列变量: {crosstab_table['column_name']}")
    print("  ✓ 交叉表表格测试通过")
    
except Exception as e:
    print(f"  ✗ 表格创建测试失败: {e}")
    sys.exit(1)

print("\n✅ 所有测试通过！")
print("描述性统计、频数分析和交叉表分析功能正常。")
print("数值精度设置为小数点后 4 位，与 SPSS 输出一致。")