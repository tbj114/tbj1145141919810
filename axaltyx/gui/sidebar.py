from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from axaltyx.i18n import I18nManager
from axaltyx.gui.widgets.arco_tree import ArcoTree, ArcoTreeItem


class SideBar(QWidget):
    """侧边栏分析菜单树"""

    item_clicked = pyqtSignal(str)  # 发送点击的命令

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tree = ArcoTree()
        self.tree.itemClicked.connect(self._on_item_clicked)
        self._populate_tree()

        layout.addWidget(self.tree)

    def _populate_tree(self):
        """填充分析菜单树"""
        analysis_root = ArcoTreeItem(self.tree)
        analysis_root.setText(0, self.i18n.t("sidebar.analysis"))
        analysis_root.setExpanded(True)

        # 完整的菜单结构
        menu_items = [
            ("sidebar.statistical_summary", [
                ("sidebar.frequencies", "frequencies"),
                ("sidebar.descriptives", "descriptives"),
                ("sidebar.explore", "explore")
            ]),
            ("sidebar.compare_means", [
                ("sidebar.means", "means"),
                ("sidebar.one_sample_t", "one_sample_t"),
                ("sidebar.independent_t", "independent_t"),
                ("sidebar.paired_t", "paired_t")
            ]),
            ("sidebar.general_linear_model", [
                ("sidebar.one_way_anova", "one_way_anova"),
                ("sidebar.manova", "manova"),
                ("sidebar.ancova", "ancova"),
                ("sidebar.repeated_measures", "repeated_measures")
            ]),
            ("sidebar.nonparametric", [
                ("sidebar.chi_square", "chi_square"),
                ("sidebar.binomial", "binomial"),
                ("sidebar.runs_test", "runs_test"),
                ("sidebar.kolmogorov_smirnov", "kolmogorov_smirnov"),
                ("sidebar.two_independent_samples", "two_independent_samples"),
                ("sidebar.k_independent_samples", "k_independent_samples"),
                ("sidebar.two_related_samples", "two_related_samples"),
                ("sidebar.k_related_samples", "k_related_samples")
            ]),
            ("sidebar.correlation", [
                ("sidebar.bivariate", "bivariate"),
                ("sidebar.partial", "partial")
            ]),
            ("sidebar.regression", [
                ("sidebar.linear", "linear"),
                ("sidebar.multiple_linear", "multiple_linear"),
                ("sidebar.logistic", "logistic"),
                ("sidebar.ordinal", "ordinal"),
                ("sidebar.nonlinear", "nonlinear"),
                ("sidebar.curve_estimation", "curve_estimation")
            ]),
            ("sidebar.classification", [
                ("sidebar.factor_analysis", "factor_analysis"),
                ("sidebar.principal_components", "principal_components"),
                ("sidebar.cluster", "cluster"),
                ("sidebar.discriminant", "discriminant"),
                ("sidebar.correspondence", "correspondence")
            ]),
            ("sidebar.scale", [
                ("sidebar.reliability", "reliability"),
                ("sidebar.validity", "validity"),
                ("sidebar.multidimensional_scaling", "multidimensional_scaling")
            ]),
            ("sidebar.survival", [
                ("sidebar.kaplan_meier", "kaplan_meier"),
                ("sidebar.cox_regression", "cox_regression")
            ]),
            ("sidebar.advanced", [
                ("sidebar.sem", "sem"),
                ("sidebar.bayesian", "bayesian"),
                ("sidebar.meta_analysis", "meta_analysis"),
                ("sidebar.time_series", "time_series"),
                ("sidebar.log_linear", "log_linear"),
                ("sidebar.probit", "probit")
            ]),
            ("sidebar.causal_inference", [
                ("sidebar.psm", "psm"),
                ("sidebar.did", "did"),
                ("sidebar.instrumental_variables", "instrumental_variables"),
                ("sidebar.rdd", "rdd"),
                ("sidebar.quantile_regression", "quantile_regression")
            ]),
            ("sidebar.machine_learning", [
                ("sidebar.regularization", "regularization"),
                ("sidebar.random_forest", "random_forest"),
                ("sidebar.svm", "svm"),
                ("sidebar.gradient_boosting", "gradient_boosting"),
                ("sidebar.neural_network", "neural_network"),
                ("sidebar.bayesian_network", "bayesian_network")
            ]),
            ("sidebar.text_analysis", [
                ("sidebar.text_mining", "text_mining"),
                ("sidebar.sentiment", "sentiment"),
                ("sidebar.word_cloud", "word_cloud")
            ]),
            ("sidebar.spatial", [
                ("sidebar.spatial_econometrics", "spatial_econometrics"),
                ("sidebar.network_analysis", "network_analysis")
            ]),
            ("sidebar.multilevel", [
                ("sidebar.hlm", "hlm"),
                ("sidebar.bayesian_hierarchical", "bayesian_hierarchical")
            ]),
            ("sidebar.advanced_bayesian", [
                ("sidebar.bayesian_factor", "bayesian_factor"),
                ("sidebar.bayesian_cluster", "bayesian_cluster"),
                ("sidebar.bayesian_survival", "bayesian_survival"),
                ("sidebar.bayesian_logistic", "bayesian_logistic")
            ])
        ]

        for parent_key, children in menu_items:
            parent_item = ArcoTreeItem(analysis_root)
            parent_item.setText(0, self.i18n.t(parent_key))
            parent_item.setExpanded(True)

            for child_key, command in children:
                child_item = ArcoTreeItem(parent_item)
                child_item.setText(0, self.i18n.t(child_key))
                child_item.command = command

    def _on_item_clicked(self, item: ArcoTreeItem, column: int):
        """处理菜单项点击事件"""
        if item.command:
            self.item_clicked.emit(item.command)
