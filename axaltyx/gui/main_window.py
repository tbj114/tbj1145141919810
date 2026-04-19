from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QLabel, QMessageBox, QFileDialog, QApplication
)
from PyQt6.QtCore import Qt
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


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.i18n = I18nManager()
        self.current_file = None
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
        self.menu_bar.copy.connect(self.tool_bar.copy)
        self.menu_bar.paste.connect(self.tool_bar.paste)
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

    # ==================== 文件菜单方法 ====================
    def _on_new_file(self):
        """新建文件"""
        if self.data_editor_tab is None:
            self.data_editor_tab = DataEditorTab()
            self.tab_widget.addTab(self.data_editor_tab, "数据编辑器")
        self.tab_widget.setCurrentWidget(self.data_editor_tab)
        self.status_bar.show_message("新建文件")

    def _on_open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "打开文件",
            "",
            "AxaltyX文件 (*.axo);;所有文件 (*.*)"
        )
        if file_path:
            self.current_file = file_path
            if self.data_editor_tab is None:
                self.data_editor_tab = DataEditorTab()
                self.tab_widget.addTab(self.data_editor_tab, "数据编辑器")
            self.tab_widget.setCurrentWidget(self.data_editor_tab)
            self.status_bar.show_message(f"打开文件: {file_path}")

    def _on_save_file(self):
        """保存文件"""
        if self.current_file:
            self.status_bar.show_message(f"保存文件: {self.current_file}")
        else:
            self._on_save_as()

    def _on_save_as(self):
        """另存为"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "另存为",
            "",
            "AxaltyX文件 (*.axo);;所有文件 (*.*)"
        )
        if file_path:
            self.current_file = file_path
            self.status_bar.show_message(f"保存文件: {file_path}")

    def _on_close_file(self):
        """关闭文件"""
        if self.current_file:
            reply = QMessageBox.question(
                self,
                "关闭文件",
                "是否保存当前文件？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._on_save_file()
                self.current_file = None
            elif reply == QMessageBox.StandardButton.No:
                self.current_file = None
            self.status_bar.show_message("文件已关闭")

    # ==================== 编辑菜单方法 ====================
    def _on_undo(self):
        """撤销"""
        self.tool_bar.undo()
        self.status_bar.show_message("撤销")

    def _on_redo(self):
        """重做"""
        self.tool_bar.redo()
        self.status_bar.show_message("重做")

    def _on_cut(self):
        """剪切"""
        self.status_bar.show_message("剪切")

    def _on_find(self):
        """查找"""
        self.status_bar.show_message("查找功能")

    def _on_replace(self):
        """替换"""
        self.status_bar.show_message("替换功能")

    # ==================== 数据菜单方法 ====================
    def _on_define_variables(self):
        """定义变量"""
        if self.variable_view_tab is None:
            self.variable_view_tab = VariableViewTab()
            self.tab_widget.addTab(self.variable_view_tab, "变量视图")
        self.tab_widget.setCurrentWidget(self.variable_view_tab)
        self.status_bar.show_message("定义变量")

    def _on_sort_cases(self):
        """排序"""
        self.status_bar.show_message("排序个案")

    def _on_select_cases(self):
        """选择个案"""
        self.status_bar.show_message("选择个案")

    def _on_weight_cases(self):
        """加权"""
        self.status_bar.show_message("加权个案")

    def _on_transpose(self):
        """转置"""
        self.status_bar.show_message("转置数据")

    def _on_restructure(self):
        """重构"""
        self.status_bar.show_message("重构数据")

    def _on_merge_files(self):
        """合并"""
        self.status_bar.show_message("合并文件")

    def _on_split_file(self):
        """拆分"""
        self.status_bar.show_message("拆分文件")

    # ==================== 视图菜单方法 ====================
    def _on_toggle_panel(self, panel_name):
        """切换面板显示/隐藏"""
        if panel_name == "data_editor":
            if self.data_editor_tab is None:
                self.data_editor_tab = DataEditorTab()
                self.tab_widget.addTab(self.data_editor_tab, "数据编辑器")
            self.tab_widget.setCurrentWidget(self.data_editor_tab)
            self.status_bar.show_message("数据编辑器")
        elif panel_name == "variable_view":
            if self.variable_view_tab is None:
                self.variable_view_tab = VariableViewTab()
                self.tab_widget.addTab(self.variable_view_tab, "变量视图")
            self.tab_widget.setCurrentWidget(self.variable_view_tab)
            self.status_bar.show_message("变量视图")
        elif panel_name == "output":
            if self.output_tab is None:
                self.output_tab = OutputTab()
                self.tab_widget.addTab(self.output_tab, "输出")
            self.tab_widget.setCurrentWidget(self.output_tab)
            self.status_bar.show_message("输出面板")
        elif panel_name == "syntax":
            if self.syntax_tab is None:
                self.syntax_tab = SyntaxTab()
                self.tab_widget.addTab(self.syntax_tab, "语法")
            self.tab_widget.setCurrentWidget(self.syntax_tab)
            self.status_bar.show_message("语法面板")

    # ==================== 帮助菜单方法 ====================
    def _on_show_about(self):
        """显示关于对话框"""
        about_dialog = AboutDialog(self)
        about_dialog.exec()
