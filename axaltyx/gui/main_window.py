from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QLabel, QMessageBox, QFileDialog, QApplication, QShortcut
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from .frameless_window import FramelessWindow
from .menubar import MenuBar
from .toolbar import ToolBar
from .sidebar import SideBar
from .statusbar import StatusBar
from .tabs.data_editor_tab import DataEditorTab
from .tabs.variable_view_tab import VariableViewTab
from .tabs.output_tab import OutputTab
from .tabs.syntax_tab import SyntaxTab
from .dialogs.about_dialog import AboutDialog
from axaltyx.i18n import I18nManager
from axaltyx.core.data.dataset import Dataset
from axaltyx.utils.file_io import FileIO


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.i18n = I18nManager()
        self.current_file = None
        self.dataset = None
        self._init_ui()
        self._connect_signals()
        self._create_shortcuts()
        self.set_title(self.i18n.t("app.app_name"))
        self.resize(1280, 800)
        
        # 默认创建新数据集
        self._create_new_dataset()

    def _init_ui(self):
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.menu_bar = MenuBar()
        content_layout.addWidget(self.menu_bar)

        self.tool_bar = ToolBar()
        content_layout.addWidget(self.tool_bar)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_layout.addWidget(main_splitter, 1)

        self.sidebar = SideBar()
        self.sidebar.setMaximumWidth(280)
        self.sidebar.setMinimumWidth(200)
        main_splitter.addWidget(self.sidebar)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        main_splitter.addWidget(self.tab_widget)

        main_splitter.setStretchFactor(0, 0)
        main_splitter.setStretchFactor(1, 1)

        self.status_bar = StatusBar()
        content_layout.addWidget(self.status_bar)

        # 用于跟踪已打开的标签
        self.data_editor_tab = None
        self.variable_view_tab = None
        self.output_tab = None
        self.syntax_tab = None

    def _connect_signals(self):
        # 文件菜单
        self.menu_bar.new_file.connect(self._on_new_file)
        self.menu_bar.open_file.connect(self._on_open_file)
        self.menu_bar.save_file.connect(self._on_save_file)
        self.menu_bar.save_as.connect(self._on_save_as)
        self.menu_bar.close_file.connect(self._on_close_file)
        self.menu_bar.exit_app.connect(QApplication.instance().quit)
        
        # 编辑菜单
        self.menu_bar.undo.connect(self._on_undo)
        self.menu_bar.redo.connect(self._on_redo)
        self.menu_bar.cut.connect(self._on_cut)
        self.menu_bar.copy.connect(self.tool_bar.copy.emit)
        self.menu_bar.paste.connect(self.tool_bar.paste.emit)
        self.menu_bar.find.connect(self._on_find)
        self.menu_bar.replace.connect(self._on_replace)
        
        # 数据菜单
        self.menu_bar.define_variables.connect(self._on_define_variables)
        self.menu_bar.sort_cases.connect(self._on_sort_cases)
        self.menu_bar.select_cases.connect(self._on_select_cases)
        self.menu_bar.weight_cases.connect(self._on_weight_cases)
        self.menu_bar.transpose.connect(self._on_transpose)
        self.menu_bar.restructure.connect(self._on_restructure)
        self.menu_bar.merge_files.connect(self._on_merge_files)
        self.menu_bar.split_file.connect(self._on_split_file)
        
        # 视图菜单
        self.menu_bar.toggle_panel.connect(self._on_toggle_panel)
        
        # 帮助菜单
        self.menu_bar.show_about.connect(self._on_show_about)
        
        # 侧边栏
        self.sidebar.item_clicked.connect(self._on_sidebar_item_clicked)

    def _create_shortcuts(self):
        """创建快捷键"""
        # 文件操作
        QShortcut(QKeySequence.StandardKey.New, self, self._on_new_file)
        QShortcut(QKeySequence.StandardKey.Open, self, self._on_open_file)
        QShortcut(QKeySequence.StandardKey.Save, self, self._on_save_file)
        QShortcut(QKeySequence.StandardKey.SaveAs, self, self._on_save_as)
        QShortcut(QKeySequence.StandardKey.Close, self, self._on_close_file)
        
        # 编辑操作
        QShortcut(QKeySequence.StandardKey.Undo, self, self._on_undo)
        QShortcut(QKeySequence.StandardKey.Redo, self, self._on_redo)
        QShortcut(QKeySequence.StandardKey.Cut, self, self._on_cut)
        QShortcut(QKeySequence.StandardKey.Copy, self, self.tool_bar.copy.emit)
        QShortcut(QKeySequence.StandardKey.Paste, self, self.tool_bar.paste.emit)
        QShortcut(QKeySequence.StandardKey.Find, self, self._on_find)
        QShortcut(QKeySequence.StandardKey.Replace, self, self._on_replace)

    def _create_new_dataset(self):
        """创建新数据集"""
        self.dataset = FileIO.create_new_dataset()
        if self.data_editor_tab is None:
            self.data_editor_tab = DataEditorTab()
            self.tab_widget.addTab(self.data_editor_tab, self.i18n.t("app.data_editor"))
        self.data_editor_tab.data_table.set_dataset(self.dataset)
        self.tab_widget.setCurrentWidget(self.data_editor_tab)
        self.status_bar.show_message(self.i18n.t("app.new_file_created"))

    # ==================== 文件菜单方法 ====================
    def _on_new_file(self):
        """新建文件"""
        self._create_new_dataset()

    def _on_open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.i18n.t("app.import_title"),
            "",
            "AxaltyX Files (*.tbj);;CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;SPSS Files (*.sav);;All Files (*)"
        )
        if file_path:
            dataset = FileIO.load_file(file_path)
            if dataset:
                self.dataset = dataset
                self.current_file = file_path
                if self.data_editor_tab is None:
                    self.data_editor_tab = DataEditorTab()
                    self.tab_widget.addTab(self.data_editor_tab, self.i18n.t("app.data_editor"))
                self.data_editor_tab.data_table.set_dataset(self.dataset)
                self.tab_widget.setCurrentWidget(self.data_editor_tab)
                self.status_bar.show_message(self.i18n.t("app.file_opened", file=file_path))
            else:
                QMessageBox.critical(self, "错误", "无法加载文件")

    def _sync_data_from_tables(self):
        """从表格同步数据到数据集"""
        if self.dataset is None:
            return
        if self.data_editor_tab:
            self.data_editor_tab.data_table.update_dataset_from_table()
        if self.variable_view_tab:
            self.variable_view_tab.variable_table.update_dataset_from_table()

    def _on_save_file(self):
        """保存文件"""
        if self.dataset is None:
            return
        self._sync_data_from_tables()
        if self.current_file:
            if FileIO.save_file(self.dataset, self.current_file):
                self.status_bar.show_message(self.i18n.t("app.file_saved", file=self.current_file))
        else:
            self._on_save_as()

    def _on_save_as(self):
        """另存为"""
        if self.dataset is None:
            return
        self._sync_data_from_tables()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.t("app.export_title"),
            "",
            "AxaltyX Files (*.tbj);;CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
        )
        if file_path:
            if FileIO.save_file(self.dataset, file_path):
                self.current_file = file_path
                self.status_bar.show_message(self.i18n.t("app.file_saved", file=file_path))

    def _on_close_file(self):
        """关闭文件"""
        if self.current_file:
            reply = QMessageBox.question(
                self,
                self.i18n.t("app.confirm_close"),
                self.i18n.t("app.close_file_prompt"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._on_save_file()
                self.current_file = None
            elif reply == QMessageBox.StandardButton.No:
                self.current_file = None
            self.status_bar.show_message(self.i18n.t("app.file_closed"))

    # ==================== 编辑菜单方法 ====================
    def _on_undo(self):
        """撤销"""
        self.tool_bar.undo.emit()
        self.status_bar.show_message(self.i18n.t("app.undo_performed"))

    def _on_redo(self):
        """重做"""
        self.tool_bar.redo.emit()
        self.status_bar.show_message(self.i18n.t("app.redo_performed"))

    def _on_cut(self):
        """剪切"""
        self.status_bar.show_message(self.i18n.t("app.cut_performed"))

    def _on_find(self):
        """查找"""
        self.status_bar.show_message(self.i18n.t("app.find_function"))

    def _on_replace(self):
        """替换"""
        self.status_bar.show_message(self.i18n.t("app.replace_function"))

    # ==================== 数据菜单方法 ====================
    def _on_define_variables(self):
        """定义变量"""
        if self.variable_view_tab is None:
            self.variable_view_tab = VariableViewTab()
            self.tab_widget.addTab(self.variable_view_tab, self.i18n.t("app.variable_view"))
        if self.dataset:
            self.variable_view_tab.variable_table.set_dataset(self.dataset)
        self.tab_widget.setCurrentWidget(self.variable_view_tab)
        self.status_bar.show_message(self.i18n.t("app.define_variables"))

    def _on_sort_cases(self):
        """排序"""
        self.status_bar.show_message(self.i18n.t("app.sort_cases"))

    def _on_select_cases(self):
        """选择个案"""
        self.status_bar.show_message(self.i18n.t("app.select_cases"))

    def _on_weight_cases(self):
        """加权"""
        self.status_bar.show_message(self.i18n.t("app.weight_cases"))

    def _on_transpose(self):
        """转置"""
        self.status_bar.show_message(self.i18n.t("app.transpose_data"))

    def _on_restructure(self):
        """重构"""
        self.status_bar.show_message(self.i18n.t("app.restructure_data"))

    def _on_merge_files(self):
        """合并"""
        self.status_bar.show_message(self.i18n.t("app.merge_files"))

    def _on_split_file(self):
        """拆分"""
        self.status_bar.show_message(self.i18n.t("app.split_file"))

    # ==================== 视图菜单方法 ====================
    def _on_toggle_panel(self, panel_name):
        """切换面板显示/隐藏"""
        if panel_name == "data_editor":
            if self.data_editor_tab is None:
                self.data_editor_tab = DataEditorTab()
                self.tab_widget.addTab(self.data_editor_tab, self.i18n.t("app.data_editor"))
            if self.dataset:
                self.data_editor_tab.data_table.set_dataset(self.dataset)
            self.tab_widget.setCurrentWidget(self.data_editor_tab)
            self.status_bar.show_message(self.i18n.t("app.data_editor"))
        elif panel_name == "variable_view":
            if self.variable_view_tab is None:
                self.variable_view_tab = VariableViewTab()
                self.tab_widget.addTab(self.variable_view_tab, self.i18n.t("app.variable_view"))
            if self.dataset:
                self.variable_view_tab.variable_table.set_dataset(self.dataset)
            self.tab_widget.setCurrentWidget(self.variable_view_tab)
            self.status_bar.show_message(self.i18n.t("app.variable_view"))
        elif panel_name == "output":
            if self.output_tab is None:
                self.output_tab = OutputTab()
                self.tab_widget.addTab(self.output_tab, self.i18n.t("app.output"))
            self.tab_widget.setCurrentWidget(self.output_tab)
            self.status_bar.show_message(self.i18n.t("app.output"))
        elif panel_name == "syntax":
            if self.syntax_tab is None:
                self.syntax_tab = SyntaxTab()
                self.tab_widget.addTab(self.syntax_tab, self.i18n.t("app.syntax"))
            self.tab_widget.setCurrentWidget(self.syntax_tab)
            self.status_bar.show_message(self.i18n.t("app.syntax"))

    # ==================== 侧边栏处理 ====================
    def _on_sidebar_item_clicked(self, command: str):
        """处理侧边栏项目点击"""
        dialog_map = {
            "frequencies": "frequencies",
            "descriptives": "descriptives",
            "explore": "explore",
            "means": "means",
            "one_sample_t": "ttest_one",
            "independent_t": "ttest_independent",
            "paired_t": "ttest_paired",
            "one_way_anova": "oneway_anova",
            "manova": "manova",
            "ancova": "ancova",
            "repeated_measures": "rm_anova",
            "chi_square": "chisquare",
            "binomial": "binomial",
            "runs_test": "runs",
            "kolmogorov_smirnov": "ks",
            "two_independent_samples": "two_independent",
            "k_independent_samples": "k_independent",
            "two_related_samples": "two_related",
            "k_related_samples": "two_related",
            "bivariate": "correlation",
            "partial": "correlation",
            "linear": "regression",
            "multiple_linear": "regression",
            "logistic": "regression",
            "ordinal": "regression",
            "nonlinear": "regression",
            "curve_estimation": "regression",
            "factor_analysis": "factor",
            "principal_components": "factor",
            "cluster": "cluster",
            "discriminant": "cluster",
            "correspondence": "cluster",
            "reliability": "reliability",
            "validity": "reliability",
            "multidimensional_scaling": "reliability",
            "kaplan_meier": "survival",
            "cox_regression": "survival",
            "sem": "sem",
            "bayesian": "sem",
            "meta_analysis": "sem",
            "time_series": "sem",
            "log_linear": "sem",
            "probit": "sem",
            "psm": "cluster",
            "did": "cluster",
            "instrumental_variables": "cluster",
            "rdd": "cluster",
            "quantile_regression": "cluster",
            "regularization": "cluster",
            "random_forest": "cluster",
            "svm": "cluster",
            "gradient_boosting": "cluster",
            "neural_network": "cluster",
            "bayesian_network": "cluster",
            "text_mining": "cluster",
            "sentiment": "cluster",
            "word_cloud": "cluster",
            "spatial_econometrics": "cluster",
            "network_analysis": "cluster",
            "hlm": "cluster",
            "bayesian_hierarchical": "cluster",
            "bayesian_factor": "cluster",
            "bayesian_cluster": "cluster",
            "bayesian_survival": "cluster",
            "bayesian_logistic": "cluster"
        }
        
        dialog_name = dialog_map.get(command, None)
        if dialog_name:
            self._show_dialog(dialog_name)
        else:
            self.status_bar.show_message(f"功能 {command} 正在开发中...")

    def _show_dialog(self, dialog_name: str):
        """显示对应的对话框"""
        dialog_classes = {}
        
        try:
            # 动态导入对话框
            module_name = f"axaltyx.gui.dialogs.{dialog_name}_dialog"
            module = __import__(module_name, fromlist=[""])
            
            # 尝试获取对话框类名
            class_name = dialog_name.replace("_", " ").title().replace(" ", "") + "Dialog"
            
            # 查找类
            dialog_class = None
            for name in dir(module):
                if "Dialog" in name:
                    dialog_class = getattr(module, name)
                    break
            
            if dialog_class:
                dialog = dialog_class(self)
                dialog.exec()
                self.status_bar.show_message(f"已打开 {dialog_name} 对话框")
            else:
                QMessageBox.information(self, "提示", f"{dialog_name} 对话框正在开发中...")
        except ImportError:
            QMessageBox.information(self, "提示", f"{dialog_name} 功能正在开发中...")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载对话框失败: {str(e)}")

    # ==================== 帮助菜单方法 ====================
    def _on_show_about(self):
        """显示关于对话框"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()
