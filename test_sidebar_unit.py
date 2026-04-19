#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
侧边栏分析菜单树单元测试 - 不依赖完整 GUI
"""

from axaltyx.i18n import I18nManager


def test_i18n_translations():
    """测试 i18n 翻译是否完整"""
    i18n = I18nManager()

    # 根菜单
    assert i18n.t("sidebar.analysis") is not None
    assert i18n.t("sidebar.analysis") != "sidebar.analysis"
    print("✓ 根菜单翻译正常")

    # 主要分类菜单
    categories = [
        "sidebar.statistical_summary",
        "sidebar.compare_means",
        "sidebar.general_linear_model",
        "sidebar.nonparametric",
        "sidebar.correlation",
        "sidebar.regression",
        "sidebar.classification",
        "sidebar.scale",
        "sidebar.survival",
        "sidebar.advanced",
        "sidebar.causal_inference",
        "sidebar.machine_learning",
        "sidebar.text_analysis",
        "sidebar.spatial",
        "sidebar.multilevel",
        "sidebar.advanced_bayesian"
    ]

    for cat in categories:
        translation = i18n.t(cat)
        assert translation is not None
        assert translation != cat
        print(f"✓ 分类菜单 {cat} 翻译正常")

    # 统计摘要子菜单
    summary_items = [
        "sidebar.frequencies",
        "sidebar.descriptives",
        "sidebar.explore"
    ]

    for item in summary_items:
        translation = i18n.t(item)
        assert translation is not None
        assert translation != item
        print(f"✓ 统计摘要子菜单 {item} 翻译正常")

    # 比较均値子菜单
    compare_items = [
        "sidebar.means",
        "sidebar.one_sample_t",
        "sidebar.independent_t",
        "sidebar.paired_t"
    ]

    for item in compare_items:
        translation = i18n.t(item)
        assert translation is not None
        assert translation != item
        print(f"✓ 比较均値子菜单 {item} 翻译正常")

    print("\n所有 i18n 翻译测试通过！")


def test_menu_structure_complete():
    """测试菜单结构是否完整"""
    i18n = I18nManager()

    # 完整的菜单结构定义
    complete_menu_structure = {
        "sidebar.statistical_summary": [
            "sidebar.frequencies",
            "sidebar.descriptives",
            "sidebar.explore"
        ],
        "sidebar.compare_means": [
            "sidebar.means",
            "sidebar.one_sample_t",
            "sidebar.independent_t",
            "sidebar.paired_t"
        ],
        "sidebar.general_linear_model": [
            "sidebar.one_way_anova",
            "sidebar.manova",
            "sidebar.ancova",
            "sidebar.repeated_measures"
        ],
        "sidebar.nonparametric": [
            "sidebar.chi_square",
            "sidebar.binomial",
            "sidebar.runs_test",
            "sidebar.kolmogorov_smirnov",
            "sidebar.two_independent_samples",
            "sidebar.k_independent_samples",
            "sidebar.two_related_samples",
            "sidebar.k_related_samples"
        ],
        "sidebar.correlation": [
            "sidebar.bivariate",
            "sidebar.partial"
        ],
        "sidebar.regression": [
            "sidebar.linear",
            "sidebar.multiple_linear",
            "sidebar.logistic",
            "sidebar.ordinal",
            "sidebar.nonlinear",
            "sidebar.curve_estimation"
        ],
        "sidebar.classification": [
            "sidebar.factor_analysis",
            "sidebar.principal_components",
            "sidebar.cluster",
            "sidebar.discriminant",
            "sidebar.correspondence"
        ],
        "sidebar.scale": [
            "sidebar.reliability",
            "sidebar.validity",
            "sidebar.multidimensional_scaling"
        ],
        "sidebar.survival": [
            "sidebar.kaplan_meier",
            "sidebar.cox_regression"
        ],
        "sidebar.advanced": [
            "sidebar.sem",
            "sidebar.bayesian",
            "sidebar.meta_analysis",
            "sidebar.time_series",
            "sidebar.log_linear",
            "sidebar.probit"
        ],
        "sidebar.causal_inference": [
            "sidebar.psm",
            "sidebar.did",
            "sidebar.instrumental_variables",
            "sidebar.rdd",
            "sidebar.quantile_regression"
        ],
        "sidebar.machine_learning": [
            "sidebar.regularization",
            "sidebar.random_forest",
            "sidebar.svm",
            "sidebar.gradient_boosting",
            "sidebar.neural_network",
            "sidebar.bayesian_network"
        ],
        "sidebar.text_analysis": [
            "sidebar.text_mining",
            "sidebar.sentiment",
            "sidebar.word_cloud"
        ],
        "sidebar.spatial": [
            "sidebar.spatial_econometrics",
            "sidebar.network_analysis"
        ],
        "sidebar.multilevel": [
            "sidebar.hlm",
            "sidebar.bayesian_hierarchical"
        ],
        "sidebar.advanced_bayesian": [
            "sidebar.bayesian_factor",
            "sidebar.bayesian_cluster",
            "sidebar.bayesian_survival",
            "sidebar.bayesian_logistic"
        ]
    }

    # 验证所有菜单项都有翻译
    all_menu_items = ["sidebar.analysis"]
    for category, children in complete_menu_structure.items():
        all_menu_items.append(category)
        all_menu_items.extend(children)

    for item_key in all_menu_items:
        translation = i18n.t(item_key)
        assert translation is not None
        assert translation != item_key

    print("✓ 所有菜单项翻译完整")
    print("✓ 菜单结构验证通过")
    print(f"\n菜单结构完整：{len(complete_menu_structure)} 个分类，总计 {len(all_menu_items)} 个菜单项")


if __name__ == "__main__":
    print("开始侧边栏分析菜单树测试...\n")
    test_i18n_translations()
    print("\n" + "=" * 50)
    test_menu_structure_complete()
    print("\n✅ 所有测试通过！")
