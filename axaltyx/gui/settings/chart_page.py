from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QComboBox, QCheckBox, QLabel, QHBoxLayout
from axaltyx.core.managers import I18nManager, ConfigManager


class ChartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.config = ConfigManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # 图表类型设置
        chart_type_group = QGroupBox(self.i18n.t("settings.chart.chart_type"))
        chart_type_layout = QVBoxLayout()

        # 图表类型选择
        chart_type_layout.addWidget(QLabel(self.i18n.t("settings.chart.default_chart_type")))
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems([
            self.i18n.t("settings.chart.line"),
            self.i18n.t("settings.chart.bar"),
            self.i18n.t("settings.chart.scatter"),
            self.i18n.t("settings.chart.pie")
        ])
        chart_type_layout.addWidget(self.chart_type_combo)
        chart_type_group.setLayout(chart_type_layout)
        layout.addWidget(chart_type_group)

        # 图表外观设置
        appearance_group = QGroupBox(self.i18n.t("settings.chart.appearance"))
        appearance_layout = QVBoxLayout()

        # 图表主题
        appearance_layout.addWidget(QLabel(self.i18n.t("settings.chart.theme")))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            self.i18n.t("settings.chart.light"),
            self.i18n.t("settings.chart.dark"),
            self.i18n.t("settings.chart.blue"),
            self.i18n.t("settings.chart.green")
        ])
        appearance_layout.addWidget(self.theme_combo)

        # 显示图例
        self.show_legend_checkbox = QCheckBox(self.i18n.t("settings.chart.show_legend"))
        appearance_layout.addWidget(self.show_legend_checkbox)

        # 显示网格
        self.show_grid_checkbox = QCheckBox(self.i18n.t("settings.chart.show_grid"))
        appearance_layout.addWidget(self.show_grid_checkbox)

        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)

        # 图表尺寸设置
        size_group = QGroupBox(self.i18n.t("settings.chart.size"))
        size_layout = QVBoxLayout()

        # 图表宽度
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel(self.i18n.t("settings.chart.width")))
        self.width_combo = QComboBox()
        self.width_combo.addItems(["600", "800", "1000", "1200"])
        width_layout.addWidget(self.width_combo)
        size_layout.addLayout(width_layout)

        # 图表高度
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel(self.i18n.t("settings.chart.height")))
        self.height_combo = QComboBox()
        self.height_combo.addItems(["400", "500", "600", "800"])
        height_layout.addWidget(self.height_combo)
        size_layout.addLayout(height_layout)

        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        # 加载设置
        self._load_settings()

        layout.addStretch()
        self.setLayout(layout)

    def _load_settings(self):
        # 加载图表类型设置
        chart_type = self.config.get("chart", "default_type", "line")
        if chart_type == "line":
            self.chart_type_combo.setCurrentIndex(0)
        elif chart_type == "bar":
            self.chart_type_combo.setCurrentIndex(1)
        elif chart_type == "scatter":
            self.chart_type_combo.setCurrentIndex(2)
        elif chart_type == "pie":
            self.chart_type_combo.setCurrentIndex(3)

        # 加载主题设置
        theme = self.config.get("chart", "theme", "light")
        if theme == "light":
            self.theme_combo.setCurrentIndex(0)
        elif theme == "dark":
            self.theme_combo.setCurrentIndex(1)
        elif theme == "blue":
            self.theme_combo.setCurrentIndex(2)
        elif theme == "green":
            self.theme_combo.setCurrentIndex(3)

        # 加载图例设置
        self.show_legend_checkbox.setChecked(self.config.get("chart", "show_legend", True))

        # 加载网格设置
        self.show_grid_checkbox.setChecked(self.config.get("chart", "show_grid", True))

        # 加载尺寸设置
        width = self.config.get("chart", "width", "800")
        self.width_combo.setCurrentText(width)

        height = self.config.get("chart", "height", "500")
        self.height_combo.setCurrentText(height)

    def save_settings(self):
        # 保存图表类型设置
        chart_type_index = self.chart_type_combo.currentIndex()
        chart_types = ["line", "bar", "scatter", "pie"]
        self.config.set("chart", "default_type", chart_types[chart_type_index])

        # 保存主题设置
        theme_index = self.theme_combo.currentIndex()
        themes = ["light", "dark", "blue", "green"]
        self.config.set("chart", "theme", themes[theme_index])

        # 保存图例设置
        self.config.set("chart", "show_legend", self.show_legend_checkbox.isChecked())

        # 保存网格设置
        self.config.set("chart", "show_grid", self.show_grid_checkbox.isChecked())

        # 保存尺寸设置
        self.config.set("chart", "width", self.width_combo.currentText())
        self.config.set("chart", "height", self.height_combo.currentText())
