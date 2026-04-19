from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt
from axaltyx.i18n import I18nManager


class SideBar(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self._populate_tree()
        
        layout.addWidget(self.tree)

    def _populate_tree(self):
        analysis_root = QTreeWidgetItem(self.tree)
        analysis_root.setText(0, self.i18n.t("sidebar.analysis"))
        analysis_root.setExpanded(True)
        
        items = [
            ("sidebar.statistical_summary", [
                "sidebar.frequencies",
                "sidebar.descriptives",
                "sidebar.explore"
            ]),
            ("sidebar.compare_means", [
                "sidebar.means",
                "sidebar.one_sample_t",
                "sidebar.independent_t",
                "sidebar.paired_t"
            ]),
            ("sidebar.general_linear_model", [
                "sidebar.one_way_anova",
                "sidebar.manova",
                "sidebar.ancova",
                "sidebar.repeated_measures"
            ]),
            ("sidebar.nonparametric", [
                "sidebar.chi_square",
                "sidebar.binomial",
                "sidebar.runs_test",
                "sidebar.kolmogorov_smirnov",
                "sidebar.two_independent_samples",
                "sidebar.k_independent_samples",
                "sidebar.two_related_samples",
                "sidebar.k_related_samples"
            ]),
            ("sidebar.correlation", [
                "sidebar.bivariate",
                "sidebar.partial"
            ]),
            ("sidebar.regression", [
                "sidebar.linear",
                "sidebar.multiple_linear",
                "sidebar.logistic",
                "sidebar.ordinal",
                "sidebar.nonlinear",
                "sidebar.curve_estimation"
            ]),
            ("sidebar.classification", [
                "sidebar.factor_analysis",
                "sidebar.principal_components",
                "sidebar.cluster",
                "sidebar.discriminant",
                "sidebar.correspondence"
            ]),
            ("sidebar.scale", [
                "sidebar.reliability",
                "sidebar.validity",
                "sidebar.multidimensional_scaling"
            ]),
            ("sidebar.survival", [
                "sidebar.kaplan_meier",
                "sidebar.cox_regression"
            ])
        ]
        
        for parent_key, children in items:
            parent_item = QTreeWidgetItem(analysis_root)
            parent_item.setText(0, self.i18n.t(parent_key))
            for child_key in children:
                child_item = QTreeWidgetItem(parent_item)
                child_item.setText(0, self.i18n.t(child_key))
