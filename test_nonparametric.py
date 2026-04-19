#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试非参数检验模块
"""

import numpy as np
import sys
sys.path.insert(0, '/workspace')

from axaltyx.core.nonparametric import (
    WilcoxonSignedRank,
    MannWhitneyU,
    KruskalWallis,
    FriedmanTest,
    SignTest,
    RunsTest
)

# 设置随机种子，确保结果可复现
np.random.seed(42)

print("=" * 60)
print("非参数检验模块测试")
print("=" * 60)
print()

# 测试 1: Wilcoxon 符号秩检验
print("测试 1: Wilcoxon 符号秩检验")
print("-" * 40)
# 生成配对数据
x1 = np.random.normal(10, 2, 30)
y1 = np.random.normal(10.5, 2, 30)
diff = x1 - y1

result_wilcoxon = WilcoxonSignedRank.test(x1, y1)
print(f"样本大小: {result_wilcoxon['n']}")
print(f"有效样本: {result_wilcoxon['valid_n']}")
print(f"统计量 T: {result_wilcoxon['statistic']}")
print(f"p 值: {result_wilcoxon['p_value']}")

# 与 scipy 结果对比
try:
    from scipy import stats
    scipy_stat, scipy_p = stats.wilcoxon(diff)
    print("\nscipy 结果对比:")
    print(f"scipy 统计量: {scipy_stat}")
    print(f"scipy p 值: {scipy_p}")
    print(f"统计量一致: {np.isclose(result_wilcoxon['statistic'], scipy_stat)}")
except ImportError:
    print("\nscipy 未安装，无法对比")
print()

# 测试 2: Mann-Whitney U 检验
print("测试 2: Mann-Whitney U 检验")
print("-" * 40)
# 生成两组独立数据
group1 = np.random.normal(10, 2, 25)
group2 = np.random.normal(12, 2, 25)

result_mannwhitney = MannWhitneyU.test(group1, group2)
print(f"第一组大小: {result_mannwhitney['n1']}")
print(f"第二组大小: {result_mannwhitney['n2']}")
print(f"U 统计量: {result_mannwhitney['U']}")
print(f"p 值: {result_mannwhitney['p_value']}")

# 与 scipy 结果对比
try:
    from scipy import stats
    scipy_u, scipy_p = stats.mannwhitneyu(group1, group2)
    print("\nscipy 结果对比:")
    print(f"scipy U: {scipy_u}")
    print(f"scipy p 值: {scipy_p}")
except ImportError:
    print("\nscipy 未安装，无法对比")
print()

# 测试 3: Kruskal-Wallis 检验
print("测试 3: Kruskal-Wallis 检验")
print("-" * 40)
# 生成三组数据
k_group1 = np.random.normal(10, 2, 20)
k_group2 = np.random.normal(11, 2, 20)
k_group3 = np.random.normal(12, 2, 20)

result_kruskal = KruskalWallis.test(k_group1, k_group2, k_group3)
print(f"组数: {result_kruskal['k']}")
print(f"总样本: {result_kruskal['N']}")
print(f"统计量 H: {result_kruskal['statistic']}")
print(f"p 值: {result_kruskal['p_value']}")

# 与 scipy 结果对比
try:
    from scipy import stats
    scipy_h, scipy_p = stats.kruskal(k_group1, k_group2, k_group3)
    print("\nscipy 结果对比:")
    print(f"scipy H: {scipy_h}")
    print(f"scipy p 值: {scipy_p}")
except ImportError:
    print("\nscipy 未安装，无法对比")
print()

# 测试 4: Friedman 检验
print("测试 4: Friedman 检验")
print("-" * 40)
# 生成数据（每个条件有 15 个样本）
n_friedman = 15
f_group1 = np.random.normal(10, 2, n_friedman)
f_group2 = np.random.normal(10.5, 2, n_friedman)
f_group3 = np.random.normal(11, 2, n_friedman)

result_friedman = FriedmanTest.test(f_group1, f_group2, f_group3)
print(f"条件数: {result_friedman['k']}")
print(f"样本数: {result_friedman['n']}")
print(f"统计量: {result_friedman['statistic']}")
print(f"p 值: {result_friedman['p_value']}")

# 与 scipy 结果对比
try:
    from scipy import stats
    data = np.array([f_group1, f_group2, f_group3]).T
    scipy_stat, scipy_p = stats.friedmanchisquare(*data.T)
    print("\nscipy 结果对比:")
    print(f"scipy 统计量: {scipy_stat}")
    print(f"scipy p 值: {scipy_p}")
except ImportError:
    print("\nscipy 未安装，无法对比")
print()

# 测试 5: 符号检验
print("测试 5: 符号检验")
print("-" * 40)
# 使用之前的配对数据
result_sign = SignTest.test(x1, y1)
print(f"样本大小: {result_sign['n']}")
print(f"有效样本: {result_sign['valid_n']}")
print(f"正号数: {result_sign['n_positive']}")
print(f"负号数: {result_sign['n_negative']}")
print(f"统计量 S: {result_sign['statistic']}")
print(f"p 值: {result_sign['p_value']}")
print()

# 测试 6: 游程检验
print("测试 6: 游程检验")
print("-" * 40)
# 生成一个有趋势的序列
data_runs = np.concatenate([np.random.normal(10, 1, 15), np.random.normal(12, 1, 15)])
result_runs = RunsTest.test(data_runs)
print(f"样本大小: {result_runs['n']}")
print(f"有效样本: {result_runs['valid_n']}")
print(f"划分点 (中位数): {result_runs['cut_point']:.4f}")
print(f"高于划分点: {result_runs['n1']}")
print(f"低于划分点: {result_runs['n2']}")
print(f"游程数: {result_runs['statistic']}")
print(f"期望游程数: {result_runs['expected_runs']:.4f}")
print(f"p 值: {result_runs['p_value']}")

print()
print("=" * 60)
print("所有测试完成!")
print("=" * 60)
