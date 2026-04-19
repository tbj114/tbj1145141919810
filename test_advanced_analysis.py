#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证高级分析模块
"""

import numpy as np
import sys
sys.path.insert(0, '/workspace')

# 导入所有高级分析模块
from axaltyx.core.advanced import PCA, FactorAnalysis, TimeSeriesAnalysis, SEM, MetaAnalysis
from axaltyx.core.classification import KMeans, HierarchicalClustering, LinearDiscriminantAnalysis
from axaltyx.core.scale import Reliability, Validity
from axaltyx.core.survival import KaplanMeier
from axaltyx.core.causal import CausalInference
from axaltyx.core.ml import LogisticRegression, KNearestNeighbors, DecisionTreeClassifier, LinearRegression, RidgeRegression
from axaltyx.core.bayesian_advanced import BayesianAnalysis
from axaltyx.core.text import TextAnalysis
from axaltyx.core.spatial import SpatialAnalysis
from axaltyx.core.multilevel import MultilevelModel

# 设置随机种子
np.random.seed(42)

print("=" * 60)
print("高级分析模块验证")
print("=" * 60)
print()

# 测试 1: 因子分析和主成分分析
print("测试 1: 因子分析和主成分分析")
print("-" * 40)
try:
    # 生成测试数据
    X = np.random.normal(0, 1, (100, 5))
    # 主成分分析
    pca_result = PCA.fit(X, n_components=2)
    print(f"PCA 成功: 解释方差 = {pca_result['cumulative_variance'][-1]:.4f}")
    # 因子分析
    factor_result = FactorAnalysis.fit(X, n_factors=2)
    print(f"因子分析成功: 因子数量 = {factor_result['n_factors']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 2: 聚类分析和判别分析
print("测试 2: 聚类分析和判别分析")
print("-" * 40)
try:
    # 生成聚类数据
    X_cluster = np.vstack([
        np.random.normal(0, 1, (50, 2)),
        np.random.normal(3, 1, (50, 2))
    ])
    # K-均值聚类
    kmeans_result = KMeans.fit(X_cluster, n_clusters=2, random_state=42)
    print(f"K-均值聚类成功: 聚类数量 = {kmeans_result['n_clusters']}")
    # 层次聚类
    hierarchical_result = HierarchicalClustering.fit(X_cluster, method='ward')
    print(f"层次聚类成功: 合并历史长度 = {len(hierarchical_result['merge_history'])}")
    # 线性判别分析
    y = np.concatenate([np.zeros(50), np.ones(50)])
    lda_result = LinearDiscriminantAnalysis.fit(X_cluster, y)
    print(f"线性判别分析成功: 判别分量 = {lda_result['n_components']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 3: 信度效度分析
print("测试 3: 信度效度分析")
print("-" * 40)
try:
    # 生成信度数据
    X_reliability = np.random.normal(5, 1, (100, 5))
    # 信度分析
    reliability_result = Reliability.cronbach_alpha(X_reliability)
    print(f"Cronbach's Alpha: {reliability_result['cronbach_alpha']:.4f}")
    # 分半信度
    split_half_result = Reliability.split_half_reliability(X_reliability)
    print(f"分半信度: {split_half_result['spearman_brown']:.4f}")
    # 效度分析
    y_validity = np.sum(X_reliability, axis=1) + np.random.normal(0, 0.5, 100)
    validity_result = Validity.criterion_validity(X_reliability, y_validity)
    print(f"效标效度: {validity_result['total_correlation']:.4f}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 4: 生存分析
print("测试 4: 生存分析")
print("-" * 40)
try:
    # 生成生存数据
    time = np.random.exponential(10, 100)
    event = np.random.binomial(1, 0.7, 100)
    # Kaplan-Meier 分析
    km_result = KaplanMeier.fit(time, event)
    print(f"Kaplan-Meier 成功: 样本数 = {km_result['n_samples']}")
    print(f"中位生存时间: {km_result['median_survival_time']:.2f}")
    # 对数秩检验
    groups = {
        'group1': (time[:50], event[:50]),
        'group2': (time[50:], event[50:])
    }
    log_rank_result = KaplanMeier.log_rank_test(groups)
    print(f"对数秩检验: chi-square = {log_rank_result['chi_square']:.4f}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 5: 时间序列分析
print("测试 5: 时间序列分析")
print("-" * 40)
try:
    # 生成时间序列数据
    ts_data = np.random.random(100)
    # 描述性统计
    ts_stats = TimeSeriesAnalysis.descriptive_statistics(ts_data)
    print(f"时间序列统计: 均值 = {ts_stats['mean']:.4f}, 标准差 = {ts_stats['std']:.4f}")
    # 自相关函数
    acf_result = TimeSeriesAnalysis.acf(ts_data, nlags=10)
    print(f"ACF 成功: 滞后 1 自相关 = {acf_result['acf'][1]:.4f}")
    # 移动平均
    sma_result = TimeSeriesAnalysis.simple_moving_average(ts_data, window=5)
    print(f"移动平均成功: 结果长度 = {sma_result['n']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 6: 结构方程模型
print("测试 6: 结构方程模型")
print("-" * 40)
try:
    # 生成 SEM 数据
    X_sem = np.random.normal(0, 1, (200, 6))
    # 定义模型规格
    model_spec = {
        'latent_variables': {'F1', 'F2'},
        'measurement_model': {
            'F1': [0, 1, 2],
            'F2': [3, 4, 5]
        },
        'structural_model': {
            'F2': ['F1']
        }
    }
    # 拟合 SEM
    sem_result = SEM.fit(X_sem, model_spec)
    print(f"SEM 成功: 变量数 = {sem_result['n_variables']}")
    print(f"自由度 = {sem_result['fit_indices']['df']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 7: Meta 分析
print("测试 7: Meta 分析")
print("-" * 40)
try:
    # 生成 Meta 分析数据
    effect_sizes = np.random.normal(0.5, 0.2, 20)
    standard_errors = np.random.uniform(0.1, 0.3, 20)
    # 固定效应模型
    fixed_result = MetaAnalysis.fixed_effect_model(effect_sizes, standard_errors)
    print(f"固定效应模型: 合并效应量 = {fixed_result['pooled_effect']:.4f}")
    # 随机效应模型
    random_result = MetaAnalysis.random_effect_model(effect_sizes, standard_errors)
    print(f"随机效应模型: 合并效应量 = {random_result['pooled_effect']:.4f}")
    print(f"异质性 I² = {random_result['i_squared']:.2f}%")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 8: 因果推断
print("测试 8: 因果推断")
print("-" * 40)
try:
    # 生成因果推断数据
    n = 100
    X_causal = np.random.normal(0, 1, (n, 2))
    treatment = np.random.binomial(1, 0.5, n)
    y_causal = 1 + 2 * treatment + 0.5 * X_causal[:, 0] + np.random.normal(0, 1, n)
    # 倾向得分匹配
    psm_result = CausalInference.propensity_score_matching(X_causal, y_causal, treatment)
    print(f"倾向得分匹配: ATT = {psm_result['att']:.4f}")
    # 双重差分法
    y_pre = np.random.normal(5, 1, n)
    y_post = y_pre + 0.5 * treatment + np.random.normal(0, 0.5, n)
    did_result = CausalInference.difference_in_differences(y_pre, y_post, treatment)
    print(f"双重差分法: DID 估计 = {did_result['did_estimate']:.4f}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 9: 机器学习
print("测试 9: 机器学习")
print("-" * 40)
try:
    # 生成分类数据
    X_clf = np.random.normal(0, 1, (100, 2))
    y_clf = (X_clf[:, 0] + X_clf[:, 1] > 0).astype(int)
    # 逻辑回归
    lr = LogisticRegression()
    lr.fit(X_clf, y_clf)
    lr_pred = lr.predict(X_clf)
    print(f"逻辑回归: 预测准确率 = {(lr_pred == y_clf).mean():.4f}")
    # KNN 分类
    knn = KNearestNeighbors(n_neighbors=5)
    knn.fit(X_clf, y_clf)
    knn_pred = knn.predict(X_clf)
    print(f"KNN 分类: 预测准确率 = {(knn_pred == y_clf).mean():.4f}")
    # 线性回归
    X_reg = np.random.normal(0, 1, (100, 1))
    y_reg = 2 * X_reg[:, 0] + 1 + np.random.normal(0, 0.5, 100)
    lin_reg = LinearRegression()
    lin_reg.fit(X_reg, y_reg)
    lin_pred = lin_reg.predict(X_reg)
    print(f"线性回归: R² = {1 - np.mean((y_reg - lin_pred) ** 2) / np.var(y_reg):.4f}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 10: 贝叶斯分析
print("测试 10: 贝叶斯分析")
print("-" * 40)
try:
    # 贝塔-二项分布模型
    data = (100, 60)  # 100次试验，60次成功
    beta_binomial_result = BayesianAnalysis.beta_binomial_model(data)
    print(f"贝塔-二项模型: 后验均值 = {beta_binomial_result['posterior_mean']:.4f}")
    # 正态-正态模型
    normal_data = np.random.normal(5, 1, 50)
    normal_result = BayesianAnalysis.normal_normal_model(normal_data)
    print(f"正态-正态模型: 后验均值 = {normal_result['posterior_params']['mu']:.4f}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 11: 文本分析
print("测试 11: 文本分析")
print("-" * 40)
try:
    # 测试文本
    test_text = "This is a good example. I love this product. It's amazing!"
    # 词频统计
    word_freq = TextAnalysis.word_frequency(test_text)
    print(f"词频统计: 单词数 = {len(word_freq)}")
    # 情感分析
    sentiment_result = TextAnalysis.sentiment_analysis(test_text)
    print(f"情感分析: 情感 = {sentiment_result['sentiment']}, 分数 = {sentiment_result['sentiment_score']:.4f}")
    # 文本统计
    text_stats = TextAnalysis.text_statistics(test_text)
    print(f"文本统计: 单词数 = {text_stats['word_count']}, 句子数 = {text_stats['sentence_count']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 12: 空间分析
print("测试 12: 空间分析")
print("-" * 40)
try:
    # 生成空间数据
    points = np.random.random((50, 2))
    # 计算距离
    distance = SpatialAnalysis.euclidean_distance([0, 0], [1, 1])
    print(f"欧氏距离: {distance:.4f}")
    # KNN 搜索
    knn_result = SpatialAnalysis.knn_search([0.5, 0.5], points, k=3)
    print(f"KNN 搜索: 找到 {len(knn_result['nearest_neighbors'])} 个邻居")
    # 空间密度
    density_result = SpatialAnalysis.spatial_density(points)
    print(f"空间密度: 网格大小 = {density_result['grid_size']}x{density_result['grid_size']}")
except Exception as e:
    print(f"错误: {e}")
print()

# 测试 13: 多层模型
print("测试 13: 多层模型")
print("-" * 40)
try:
    # 生成多层模型数据
    n_groups = 5
    n_per_group = 20
    X_ml = np.random.normal(0, 1, (n_groups * n_per_group, 1))
    groups = np.repeat(range(n_groups), n_per_group)
    y_ml = np.random.normal(0, 1, n_groups * n_per_group)
    # 分层线性模型
    hlm_result = MultilevelModel.hierarchical_linear_model(X_ml, y_ml, groups)
    print(f"分层线性模型: 组数 = {hlm_result['n_groups']}")
    # 随机效应模型
    re_result = MultilevelModel.random_effects_model(X_ml, y_ml, groups)
    print(f"随机效应模型: ICC = {re_result['icc']:.4f}")
except Exception as e:
    print(f"错误: {e}")
print()

print("=" * 60)
print("所有高级分析模块验证完成!")
print("=" * 60)
