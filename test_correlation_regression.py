#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试相关与回归分析，与 statsmodels 结果交叉验证
"""

import numpy as np

print("="*80)
print("相关与回归分析测试")
print("="*80)

# 设置随机种子
np.random.seed(42)

# 生成测试数据
n = 100
x1 = np.random.normal(0, 1, n)
x2 = np.random.normal(0, 1, n)
x3 = np.random.normal(0, 1, n)
y = 0.5 + 1.2*x1 + 0.8*x2 + np.random.normal(0, 0.5, n)
# 二分类数据用于逻辑回归
y_binary = (y > np.mean(y)).astype(int)
# 协变量用于偏相关
z = np.random.normal(0, 1, n)

print("\n1. 双变量相关分析")
print("-"*80)

from axaltyx.core.correlation.bivariate import BivariateCorrelation

# Pearson 相关
pearson_result = BivariateCorrelation.pearson(x1, y)
print("\nPearson 相关系数:")
print(f"  r = {pearson_result['correlation']:.6f}")
print(f"  p-value = {pearson_result['p_value']:.6f}")
print(f"  有效样本数 = {pearson_result['valid_n']}")

# Spearman 相关
spearman_result = BivariateCorrelation.spearman(x1, y)
print("\nSpearman 秩相关系数:")
print(f"  r = {spearman_result['correlation']:.6f}")
print(f"  p-value = {spearman_result['p_value']:.6f}")

# 与 scipy 对比
try:
    from scipy import stats
    scipy_pearson = stats.pearsonr(x1, y)
    scipy_spearman = stats.spearmanr(x1, y)
    print(f"\n与 scipy 结果对比:")
    print(f"  scipy Pearson: r = {scipy_pearson.statistic:.6f}, p = {scipy_pearson.pvalue:.6f}")
    print(f"  scipy Spearman: r = {scipy_spearman.statistic:.6f}, p = {scipy_spearman.pvalue:.6f}")
    print(f"  Pearson 差异: {abs(pearson_result['correlation'] - scipy_pearson.statistic):.12f}")
except ImportError:
    print("\nscipy 未安装，无法对比")

print("\n✓ 双变量相关分析测试完成")

print("\n2. 偏相关分析")
print("-"*80)

from axaltyx.core.correlation.partial import PartialCorrelation

# 偏相关分析（控制 z）
partial_result = PartialCorrelation.partial(x1, y, z)
print("\n偏相关系数（控制 z）:")
print(f"  r = {partial_result['partial_correlation']:.6f}")
print(f"  p-value = {partial_result['p_value']:.6f}")
print(f"  有效样本数 = {partial_result['valid_n']}")

print("\n✓ 偏相关分析测试完成")

print("\n3. 简单线性回归")
print("-"*80)

from axaltyx.core.regression.linear import SimpleLinearRegression

slr_result = SimpleLinearRegression.fit(x1, y)
print("\n简单线性回归结果:")
print(f"  截距 = {slr_result['intercept']:.6f} (se = {slr_result['intercept_se']:.6f}, t = {slr_result['intercept_t']:.6f}, p = {slr_result['intercept_p']:.6f})")
print(f"  斜率 = {slr_result['slope']:.6f} (se = {slr_result['slope_se']:.6f}, t = {slr_result['slope_t']:.6f}, p = {slr_result['slope_p']:.6f})")
print(f"  R² = {slr_result['r_squared']:.6f}")
print(f"  F = {slr_result['f_statistic']:.6f}, p = {slr_result['f_p_value']:.6f}")
print(f"  RMSE = {slr_result['rmse']:.6f}")

# 与 statsmodels 对比
try:
    import statsmodels.api as sm
    X_sm = sm.add_constant(x1)
    model_sm = sm.OLS(y, X_sm).fit()
    print(f"\n与 statsmodels 结果对比:")
    print(f"  statsmodels 截距 = {model_sm.params[0]:.6f}")
    print(f"  statsmodels 斜率 = {model_sm.params[1]:.6f}")
    print(f"  statsmodels R² = {model_sm.rsquared:.6f}")
    print(f"  statsmodels F = {model_sm.fvalue:.6f}, p = {model_sm.f_pvalue:.6f}")
except ImportError:
    print("\nstatsmodels 未安装，无法对比")

print("\n✓ 简单线性回归测试完成")

print("\n4. 多元线性回归")
print("-"*80)

from axaltyx.core.regression.multiple import MultipleLinearRegression

mlr_result = MultipleLinearRegression.fit(y, [x1, x2])
print("\n多元线性回归结果:")
print(f"  系数 = {mlr_result['coefficients']}")
print(f"  标准误 = {mlr_result['se_coef']}")
print(f"  t 值 = {mlr_result['t_values']}")
print(f"  p 值 = {mlr_result['p_values']}")
print(f"  R² = {mlr_result['r_squared']:.6f}")
print(f"  调整 R² = {mlr_result['adj_r_squared']:.6f}")
print(f"  F = {mlr_result['f_statistic']:.6f}, p = {mlr_result['f_p_value']:.6f}")
print(f"  RMSE = {mlr_result['rmse']:.6f}")
if mlr_result['vif'] is not None:
    print(f"  VIF = {mlr_result['vif']}")

# 与 statsmodels 对比
try:
    import statsmodels.api as sm
    X_sm = sm.add_constant(np.column_stack([x1, x2]))
    model_sm = sm.OLS(y, X_sm).fit()
    print(f"\n与 statsmodels 结果对比:")
    print(f"  statsmodels 系数 = {model_sm.params}")
    print(f"  statsmodels R² = {model_sm.rsquared:.6f}")
    print(f"  statsmodels 调整 R² = {model_sm.rsquared_adj:.6f}")
    print(f"  statsmodels F = {model_sm.fvalue:.6f}, p = {model_sm.f_pvalue:.6f}")
except ImportError:
    print("\nstatsmodels 未安装，无法对比")

print("\n✓ 多元线性回归测试完成")

print("\n5. 逻辑回归")
print("-"*80)

from axaltyx.core.regression.logistic import LogisticRegression

lr_result = LogisticRegression.fit(y_binary, [x1, x2], learning_rate=0.1, max_iter=10000)
print("\n逻辑回归结果:")
print(f"  系数 = {lr_result['coefficients']}")
print(f"  标准误 = {lr_result['se_coef']}")
print(f"  z 值 = {lr_result['z_scores']}")
print(f"  p 值 = {lr_result['p_values']}")
print(f"  迭代次数 = {lr_result['n_iterations']}")
print(f"  准确率 = {lr_result['accuracy']:.6f}")
print(f"  伪 R² (McFadden) = {lr_result['pseudo_r2']:.6f}")
print(f"  似然比 = {lr_result['ll_ratio']:.6f}, p = {lr_result['lr_p_value']:.6f}")

# 与 statsmodels 对比
try:
    import statsmodels.api as sm
    X_sm = sm.add_constant(np.column_stack([x1, x2]))
    model_sm = sm.Logit(y_binary, X_sm).fit()
    print(f"\n与 statsmodels 结果对比:")
    print(f"  statsmodels 系数 = {model_sm.params}")
    print(f"  statsmodels 伪 R² = {model_sm.prsquared:.6f}")
except ImportError:
    print("\nstatsmodels 未安装，无法对比")

print("\n✓ 逻辑回归测试完成")

print("\n" + "="*80)
print("所有测试完成！")
print("="*80)
