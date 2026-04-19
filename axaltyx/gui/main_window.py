from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QLabel
)
from PyQt6.QtCore import Qt
from .frameless_window import FramelessWindow
from .menubar import MenuBar
from .toolbar import ToolBar
from .sidebar import SideBar
from .statusbar import StatusBar
from axaltyx.i18n import I18nManager


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.i18n = I18nManager()
        self._init_ui()
        self._connect_signals()
        self.set_title(self.i18n.t("app.app_name"))
        self.resize(1280, 800)

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
        self.tab_widget.addTab(QLabel("欢迎使用 AxaltyX"), "首页")
        main_splitter.addWidget(self.tab_widget)

        main_splitter.setStretchFactor(0, 0)
        main_splitter.setStretchFactor(1, 1)

        self.status_bar = StatusBar()
        content_layout.addWidget(self.status_bar)

    def _connect_signals(self):
        self.menu_bar.new_file.connect(self.tool_bar.new_file)
        self.menu_bar.open_file.connect(self.tool_bar.open_file)
        self.menu_bar.save_file.connect(self.tool_bar.save_file)
        self.menu_bar.undo.connect(self.tool_bar.undo)
        self.menu_bar.redo.connect(self.tool_bar.redo)
        self.menu_bar.copy.connect(self.tool_bar.copy)
        self.menu_bar.paste.connect(self.tool_bar.paste)
        self.menu_bar.run.connect(self.tool_bar.run)
