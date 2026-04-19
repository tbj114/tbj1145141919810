from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QMenuBar, 
                             QStatusBar, QSplitter, QTextEdit, QToolBar, QMenu)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.utils.locale_manager import tr
from app.gui.widgets.custom_title_bar import CustomTitleBar
from app.gui.widgets.data_editor import DataEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._is_maximized = False
        self._init_ui()
        self._load_style()

    def _init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar()
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        self.title_bar.maximizeClicked.connect(self._toggle_maximize)
        self.title_bar.closeClicked.connect(self.close)
        main_layout.addWidget(self.title_bar)

        self._create_menu_bar()
        self._create_tool_bar()

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.data_editor = DataEditor()
        splitter.addWidget(self.data_editor)

        self.output_view = QTextEdit()
        self.output_view.setReadOnly(True)
        self.output_view.setMinimumWidth(300)
        splitter.addWidget(self.output_view)

        splitter.setSizes([1000, 400])
        main_layout.addWidget(splitter)

        self.status_bar = QStatusBar()
        self.status_bar.showMessage(tr('status.ready'))
        main_layout.addWidget(self.status_bar)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _create_menu_bar(self):
        self.menu_bar = QMenuBar()
        self.menu_bar.setFixedHeight(36)

        file_menu = QMenu(tr('menu.file'))
        file_menu.addAction(QAction(tr('menu.new'), self))
        file_menu.addAction(QAction(tr('menu.open'), self))
        file_menu.addAction(QAction(tr('menu.save'), self))
        file_menu.addSeparator()
        file_menu.addAction(QAction(tr('menu.import'), self))
        file_menu.addAction(QAction(tr('menu.export'), self))
        file_menu.addSeparator()
        file_menu.addAction(QAction(tr('menu.exit'), self))

        edit_menu = QMenu(tr('edit.edit'))
        edit_menu.addAction(QAction(tr('edit.undo'), self))
        edit_menu.addAction(QAction(tr('edit.redo'), self))
        edit_menu.addSeparator()
        edit_menu.addAction(QAction(tr('edit.cut'), self))
        edit_menu.addAction(QAction(tr('edit.copy'), self))
        edit_menu.addAction(QAction(tr('edit.paste'), self))
        edit_menu.addAction(QAction(tr('edit.clear'), self))

        data_menu = QMenu(tr('data.data'))
        data_menu.addAction(QAction(tr('data.define_variable'), self))
        data_menu.addAction(QAction(tr('data.insert_variable'), self))
        data_menu.addAction(QAction(tr('data.delete_variable'), self))
        data_menu.addSeparator()
        data_menu.addAction(QAction(tr('data.insert_case'), self))
        data_menu.addAction(QAction(tr('data.delete_case'), self))
        data_menu.addSeparator()
        data_menu.addAction(QAction(tr('data.select_cases'), self))
        data_menu.addAction(QAction(tr('data.weight_cases'), self))
        data_menu.addSeparator()
        data_menu.addAction(QAction(tr('data.recode'), self))

        analyze_menu = QMenu(tr('analyze.analyze'))
        analyze_menu.addAction(QAction(tr('analyze.descriptive'), self))
        analyze_menu.addAction(QAction(tr('analyze.frequencies'), self))
        analyze_menu.addAction(QAction(tr('analyze.cross_table'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.t_test'), self))
        analyze_menu.addAction(QAction(tr('analyze.one_sample_t'), self))
        analyze_menu.addAction(QAction(tr('analyze.independent_samples_t'), self))
        analyze_menu.addAction(QAction(tr('analyze.paired_samples_t'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.anova'), self))
        analyze_menu.addAction(QAction(tr('analyze.one_way_anova'), self))
        analyze_menu.addAction(QAction(tr('analyze.n_way_anova'), self))
        analyze_menu.addAction(QAction(tr('analyze.ancova'), self))
        analyze_menu.addAction(QAction(tr('analyze.rm_anova'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.nonparametric'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.correlate'), self))
        analyze_menu.addAction(QAction(tr('analyze.partial_correlate'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.regression'), self))
        analyze_menu.addAction(QAction(tr('analyze.linear_regression'), self))
        analyze_menu.addAction(QAction(tr('analyze.logistic_regression'), self))
        analyze_menu.addAction(QAction(tr('analyze.ordinal_regression'), self))
        analyze_menu.addAction(QAction(tr('analyze.nonlinear_regression'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.factor'), self))
        analyze_menu.addAction(QAction(tr('analyze.pca'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.cluster'), self))
        analyze_menu.addAction(QAction(tr('analyze.discriminant'), self))
        analyze_menu.addAction(QAction(tr('analyze.correspondence'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.reliability'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.survival'), self))
        analyze_menu.addAction(QAction(tr('analyze.cox_regression'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.time_series'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.missing_values'), self))
        analyze_menu.addAction(QAction(tr('analyze.multiple_response'), self))
        analyze_menu.addAction(QAction(tr('analyze.loglinear'), self))
        analyze_menu.addAction(QAction(tr('analyze.probit'), self))
        analyze_menu.addAction(QAction(tr('analyze.meta_analysis'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.sem'), self))
        analyze_menu.addAction(QAction(tr('analyze.bayesian'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.ml'), self))
        analyze_menu.addAction(QAction(tr('analyze.deep_learning'), self))
        analyze_menu.addSeparator()
        analyze_menu.addAction(QAction(tr('analyze.psm'), self))
        analyze_menu.addAction(QAction(tr('analyze.did'), self))
        analyze_menu.addAction(QAction(tr('analyze.iv'), self))
        analyze_menu.addAction(QAction(tr('analyze.rdd'), self))
        analyze_menu.addAction(QAction(tr('analyze.quantile'), self))
        analyze_menu.addAction(QAction(tr('analyze.spatial'), self))
        analyze_menu.addAction(QAction(tr('analyze.network'), self))
        analyze_menu.addAction(QAction(tr('analyze.hlm'), self))

        graphs_menu = QMenu(tr('graphs.graphs'))
        graphs_menu.addAction(QAction(tr('graphs.bar'), self))
        graphs_menu.addAction(QAction(tr('graphs.column'), self))
        graphs_menu.addAction(QAction(tr('graphs.stacked_bar'), self))
        graphs_menu.addAction(QAction(tr('graphs.grouped_bar'), self))
        graphs_menu.addSeparator()
        graphs_menu.addAction(QAction(tr('graphs.pie'), self))
        graphs_menu.addAction(QAction(tr('graphs.ring'), self))
        graphs_menu.addSeparator()
        graphs_menu.addAction(QAction(tr('graphs.histogram'), self))
        graphs_menu.addAction(QAction(tr('graphs.density'), self))
        graphs_menu.addSeparator()
        graphs_menu.addAction(QAction(tr('graphs.scatter'), self))
        graphs_menu.addAction(QAction(tr('graphs.scatter_matrix'), self))
        graphs_menu.addAction(QAction(tr('graphs.scatter_3d'), self))
        graphs_menu.addSeparator()
        graphs_menu.addAction(QAction(tr('graphs.line'), self))
        graphs_menu.addAction(QAction(tr('graphs.area'), self))
        graphs_menu.addSeparator()
        graphs_menu.addAction(QAction(tr('graphs.box'), self))
        graphs_menu.addAction(QAction(tr('graphs.error_bar'), self))
        graphs_menu.addSeparator()
        graphs_menu.addAction(QAction(tr('graphs.pp_plot'), self))
        graphs_menu.addAction(QAction(tr('graphs.qq_plot'), self))
        graphs_menu.addSeparator()
        graphs_menu.addAction(QAction(tr('graphs.roc'), self))
        graphs_menu.addAction(QAction(tr('graphs.heatmap'), self))

        window_menu = QMenu(tr('window.window'))
        window_menu.addAction(QAction(tr('window.new_window'), self))

        help_menu = QMenu(tr('help.help'))
        help_menu.addAction(QAction(tr('help.about'), self))

        self.menu_bar.addMenu(file_menu)
        self.menu_bar.addMenu(edit_menu)
        self.menu_bar.addMenu(data_menu)
        self.menu_bar.addMenu(analyze_menu)
        self.menu_bar.addMenu(graphs_menu)
        self.menu_bar.addMenu(window_menu)
        self.menu_bar.addMenu(help_menu)

    def _create_tool_bar(self):
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)

    def _toggle_maximize(self):
        if self._is_maximized:
            self.showNormal()
            self._is_maximized = False
        else:
            self.showMaximized()
            self._is_maximized = True

    def _load_style(self):
        style_file = Path(__file__).parent / 'styles' / 'byte_style.qss'
        try:
            with open(style_file, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass
