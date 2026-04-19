#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试方差分析系列
使用标准数据集进行验证
"""

import numpy as np

print("="*80)
print("方差分析系列测试")
print("="*80)

# 设置随机种子
np.random.seed(42)

print("\n1. 单因素方差分析测试")
print("="*80)

# 创建测试数据 - 三组不同均值的数据
group1 = np.random.normal(10, 2, 30)
group2 = np.random.normal(12, 2, 30)
group3 = np.random.normal(15, 2, 30)

try:
    from scipy import stats
    scipy_result = stats.f_oneway(group1, group2, group3)
    print(f"SciPy OneWay ANOVA:")
    print(f"  F = {scipy_result.statistic:.6f}, p = {scipy_result.pvalue:.6f}")
except ImportError:
    print("SciPy 未安装，跳过 SciPy 结果对比")

from axaltyx.core.anova.oneway import OneWayANOVA
our_result = OneWayANOVA.calculate(group1, group2, group3)

print(f"\n我们的 OneWay ANOVA:")
if our_result:
    print(f"  F = {our_result['f_value']:.6f}, p = {our_result['p_value']:.6f}")
    print(f"  df_between = {our_result['df_between']}, df_within = {our_result['df_within']}")
    print(f"  SS_between = {our_result['sum_sq_between']:.6f}, SS_within = {our_result['sum_sq_within']:.6f}")
    print(f"  MS_between = {our_result['mean_sq_between']:.6f}, MS_within = {our_result['mean_sq_within']:.6f}")

print(f"\n各组统计:")
if our_result and our_result['group_stats']:
    for g in our_result['group_stats']:
        print(f"  {g['name']}: 均值 = {g['mean']:.4f}, 标准差 = {g['std_dev']:.4f}, n = {g['count']}")

# 测试 Tukey HSD
print(f"\nTukey's HSD 检验:")
try:
    tukey_result = OneWayANOVA.tukey_hsd(group1, group2, group3)
    if tukey_result and 'comparisons' in tukey_result:
        print(f"  比较结果:")
        for comp in tukey_result['comparisons']:
            print(f"    {comp['group_i']} vs {comp['group_j']}:")
            print(f"      均值差 = {comp['mean_diff']:.4f}, p = {comp['p_value']:.6f}")
except Exception as e:
    print(f"  Tukey HSD 测试跳过: {e}")

print("\n✓ 单因素方差分析测试完成")

print("\n2. 多元方差分析测试")
print("="*80)

# 创建 MANOVA 测试数据
manova_data = []
manova_groups = []

for i, (mu1, mu2) in enumerate([(10, 5), (12, 7), (15, 9)]):
    for _ in range(30):
        var1 = np.random.normal(mu1, 2)
        var2 = np.random.normal(mu2, 1.5)
        manova_data.append([var1, var2])
        manova_groups.append(f"Group{i+1}")

try:
    from scipy import stats
    import scipy.linalg
    # 这里会比较复杂，但我们先尝试自己的实现
except ImportError:
    print("SciPy 未安装，跳过 SciPy 结果对比")

from axaltyx.core.anova.manova import MANOVA
manova_result = MANOVA.calculate(manova_data, manova_groups)

if manova_result:
    print(f"MANOVA 结果:")
    if 'lambda_wilks' in manova_result:
        print(f"  Wilks' Lambda = {manova_result['lambda_wilks']:.6f}")
    if 'pillai_trace' in manova_result:
        print(f"  Pillai's Trace = {manova_result['pillai_trace']:.6f}")
    if 'hotelling_trace' in manova_result:
        print(f"  Hotelling-Lawley Trace = {manova_result['hotelling_trace']:.6f}")
    if 'roy_root' in manova_result:
        print(f"  Roy's Greatest Root = {manova_result['roy_root']:.6f}")
    if 'f_value' in manova_result:
        print(f"  F = {manova_result['f_value']:.6f}, p = {manova_result['p_value']:.6f}")
    print(f"  组数 = {manova_result['group_count']}, 总样本数 = {manova_result['total_count']}")

print("\n✓ 多元方差分析测试完成")

print("\n3. 协方差分析测试")
print("="*80)

# 创建 ANCOVA 测试数据
# 我们有三组，因变量 y，协变量 x
ancova_y = []
ancova_x = []
ancova_groups = []

for i, (mu_y, mu_x, effect) in enumerate([(10, 5, 0), (12, 6, 2), (15, 7, 5)]):
    for _ in range(25):
        x = np.random.normal(mu_x, 1.5)
        y = mu_y + 2 * x + np.random.normal(0, 3)
        ancova_y.append(y)
        ancova_x.append(x)
        ancova_groups.append(f"Group{i+1}")

from axaltyx.core.anova.ancova import ANCOVA
ancova_result = ANCOVA.calculate(ancova_y, ancova_x, ancova_groups)

if ancova_result:
    print(f"ANCOVA 结果:")
    print(f"  组数 = {ancova_result['group_count']}, 总样本数 = {ancova_result['total_count']}")
    print(f"  SS_total = {ancova_result['ss_total']:.6f}")
    print(f"  SS_group = {ancova_result['ss_group']:.6f}, SS_covariate = {ancova_result['ss_covariate']:.6f}")
    print(f"  SS_residual = {ancova_result['ss_residual']:.6f}")
    if 'f_value' in ancova_result:
        print(f"  F_group = {ancova_result['f_value']:.6f}, p = {ancova_result['p_value']:.6f}")
    print(f"  df_group = {ancova_result['df_group']}, df_residual = {ancova_result['df_residual']}")
    print(f"  协变量数量 = {ancova_result['df_covariate']}")

print("\n✓ 协方差分析测试完成")

print("\n4. 重复测量方差分析测试")
print("="*80)

# 创建重复测量数据
n_subjects = 20
n_time = 4

rm_data = []
time_effects = [0, 1, 3, 6]

for i in range(n_subjects):
    subject_effect = np.random.normal(0, 1)
    row = []
    for t in range(n_time):
        y = 10 + time_effects[t] + subject_effect + np.random.normal(0, 1.5)
        row.append(y)
    rm_data.append(row)

from axaltyx.core.anova.rm_anova import RMANOVA
rm_result = RMANOVA.calculate(rm_data)

if rm_result:
    print(f"RM ANOVA 结果:")
    print(f"  被试数 = {rm_result['n']}, 测量次数 = {rm_result['k']}")
    print(f"  SS_total = {rm_result['ss_total']:.6f}")
    print(f"  SS_time = {rm_result['ss_time']:.6f}, SS_subject = {rm_result['ss_subject']:.6f}")
    print(f"  SS_error = {rm_result['ss_error']:.6f}")
    print(f"  F_time = {rm_result['f_value']:.6f}, p = {rm_result['p_value']:.6f}")
    print(f"  Eta squared = {rm_result['eta_squared']:.6f}")
    print(f"  Partial eta squared = {rm_result['partial_eta_squared']:.6f}")
    print(f"  时间均值: {np.array2string(rm_result['time_means'], formatter={'float_kind':lambda x: '%.4f' % x})}")
    if rm_result['sphericity']:
        print(f"  球形检验:")
        if 'w_statistic' in rm_result['sphericity']:
            print(f"    W = {rm_result['sphericity']['w_statistic']:.6f}")
        if 'p_value' in rm_result['sphericity']:
            print(f"    p = {rm_result['sphericity']['p_value']:.6f}")
        if 'epsilon_gg' in rm_result['sphericity']:
            print(f"    Greenhouse-Geisser epsilon = {rm_result['sphericity']['epsilon_gg']:.6f}")
        if 'epsilon_hf' in rm_result['sphericity']:
            print(f"    Huynh-Feldt epsilon = {rm_result['sphericity']['epsilon_hf']:.6f}")

print("\n✓ 重复测量方差分析测试完成")

print("\n" + "="*80)
print("所有测试完成！")
print("="*80)
