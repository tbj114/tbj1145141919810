#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 T 检验实现
验证与 scipy 结果的交叉验证
"""

import numpy as np
from axaltyx.core.means.ttest_one import TTestOne
from axaltyx.core.means.ttest_independent import TTestIndependent
from axaltyx.core.means.ttest_paired import TTestPaired

print("="*60)
print("开始 T 检验测试")
print("="*60)

# 设置随机种子，以便结果可重复
np.random.seed(42)

# 测试数据
data1 = np.random.normal(10, 2, 100)
data2 = np.random.normal(12, 2, 100)
data_paired_before = np.random.normal(10, 2, 50)
data_paired_after = np.random.normal(11, 2, 50)
data_with_missing = np.append(data1, [None, np.nan])

print("\n1. 单样本 t 检验")
print("-"*40)
try:
    from scipy import stats
    scipy_result = stats.ttest_1samp(data1, 10.5)
    print(f"Scipy 结果: t = {scipy_result.statistic:.6f}, p = {scipy_result.pvalue:.6f}")
except ImportError:
    print("Scipy 未安装，跳过 Scipy 结果对比")

# 测试我们的实现
our_result = TTestOne.calculate(data1, 10.5)
print(f"我们的实现: t = {our_result['t_value']:.6f}, p = {our_result['p_value']:.6f}")
print(f"样本均值 = {our_result['mean']:.4f}, 标准差 = {our_result['std_dev']:.4f}")
print(f"样本数 = {our_result['count']}, 有效样本数 = {our_result['valid_count']}")
print(f"置信区间 = [{our_result['confidence_interval'][0]:.4f}, {our_result['confidence_interval'][1]:.4f}]")

# 测试带缺失值的数据
print("\n测试带缺失值的数据:")
our_result_missing = TTestOne.calculate(data_with_missing, 10.5)
print(f"我们的实现: t = {our_result_missing['t_value']:.6f}, p = {our_result_missing['p_value']:.6f}")
print(f"样本数 = {our_result_missing['count']}, 有效样本数 = {our_result_missing['valid_count']}")

print("\n✓ 单样本 t 检验测试完成")

print("\n2. 独立样本 t 检验")
print("-"*40)
try:
    from scipy import stats
    # 假设方差相等
    scipy_result_equal = stats.ttest_ind(data1, data2, equal_var=True)
    print(f"Scipy (方差相等): t = {scipy_result_equal.statistic:.6f}, p = {scipy_result_equal.pvalue:.6f}")
    
    # 不假设方差相等
    scipy_result_unequal = stats.ttest_ind(data1, data2, equal_var=False)
    print(f"Scipy (方差不等): t = {scipy_result_unequal.statistic:.6f}, p = {scipy_result_unequal.pvalue:.6f}")
    
    # Levene 检验
    levene_result = stats.levene(data1, data2)
    print(f"Scipy Levene 检验: W = {levene_result.statistic:.6f}, p = {levene_result.pvalue:.6f}")
except ImportError:
    print("Scipy 未安装，跳过 Scipy 结果对比")

# 测试我们的实现
our_result_equal = TTestIndependent.calculate(data1, data2, equal_var=True)
print(f"我们的实现 (方差相等): t = {our_result_equal['t_value']:.6f}, p = {our_result_equal['p_value']:.6f}")
print(f"样本均值: 组1 = {our_result_equal['mean1']:.4f}, 组2 = {our_result_equal['mean2']:.4f}")
print(f"均值差 = {our_result_equal['mean_diff']:.4f}")

our_result_unequal = TTestIndependent.calculate(data1, data2, equal_var=False)
print(f"我们的实现 (方差不等): t = {our_result_unequal['t_value']:.6f}, p = {our_result_unequal['p_value']:.6f}")

# 测试 Levene 检验
our_levene = TTestIndependent.levene_test(data1, data2)
print(f"我们的实现 Levene 检验: W = {our_levene['w_value']:.6f}, p = {our_levene['p_value']:.6f}")

print("\n✓ 独立样本 t 检验测试完成")

print("\n3. 配对样本 t 检验")
print("-"*40)
try:
    from scipy import stats
    scipy_result = stats.ttest_rel(data_paired_before, data_paired_after)
    print(f"Scipy 结果: t = {scipy_result.statistic:.6f}, p = {scipy_result.pvalue:.6f}")
except ImportError:
    print("Scipy 未安装，跳过 Scipy 结果对比")

# 测试我们的实现
our_result = TTestPaired.calculate(data_paired_before, data_paired_after)
print(f"我们的实现: t = {our_result['t_value']:.6f}, p = {our_result['p_value']:.6f}")
print(f"前测均值 = {our_result['mean1']:.4f}, 后测均值 = {our_result['mean2']:.4f}")
print(f"差值均值 = {our_result['mean_diff']:.4f}, 差值标准差 = {our_result['std_dev_diff']:.4f}")
print(f"样本数 = {our_result['count']}, 有效样本数 = {our_result['valid_count']}")
print(f"置信区间 = [{our_result['confidence_interval'][0]:.4f}, {our_result['confidence_interval'][1]:.4f}]")

print("\n✓ 配对样本 t 检验测试完成")

print("\n" + "="*60)
print("所有测试完成！")
print("="*60)
