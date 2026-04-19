from PyQt6.QtWidgets import QMenuBar, QMenu, QWidget
from PyQt6.QtCore import pyqtSignal
from axaltyx.i18n import I18nManager


class MenuBar(QMenuBar):
    new_file = pyqtSignal()
    open_file = pyqtSignal()
    save_file = pyqtSignal()
    undo = pyqtSignal()
    redo = pyqtSignal()
    copy = pyqtSignal()
    paste = pyqtSignal()
    run = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()

    def _init_ui(self):
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_data_menu()
        self._create_transform_menu()
        self._create_analyze_menu()
        self._create_graphs_menu()
        self._create_utilities_menu()
        self._create_window_menu()
        self._create_help_menu()

    def _create_file_menu(self):
        file_menu = self.addMenu(self.i18n.t("menu.file"))
        new_action = file_menu.addAction(self.i18n.t("menu.file_new"))
        new_action.triggered.connect(self.new_file.emit)
        
        open_action = file_menu.addAction(self.i18n.t("menu.file_open"))
        open_action.triggered.connect(self.open_file.emit)
        
        save_action = file_menu.addAction(self.i18n.t("menu.file_save"))
        save_action.triggered.connect(self.save_file.emit)
        
        file_menu.addSeparator()
        file_menu.addAction(self.i18n.t("menu.file_close"))
        file_menu.addSeparator()
        file_menu.addAction(self.i18n.t("menu.file_exit"))

    def _create_edit_menu(self):
        edit_menu = self.addMenu(self.i18n.t("menu.edit"))
        undo_action = edit_menu.addAction(self.i18n.t("menu.edit_undo"))
        undo_action.triggered.connect(self.undo.emit)
        
        redo_action = edit_menu.addAction(self.i18n.t("menu.edit_redo"))
        redo_action.triggered.connect(self.redo.emit)
        
        edit_menu.addSeparator()
        edit_menu.addAction(self.i18n.t("menu.edit_cut"))
        copy_action = edit_menu.addAction(self.i18n.t("menu.edit_copy"))
        copy_action.triggered.connect(self.copy.emit)
        
        paste_action = edit_menu.addAction(self.i18n.t("menu.edit_paste"))
        paste_action.triggered.connect(self.paste.emit)
        
        edit_menu.addSeparator()
        edit_menu.addAction(self.i18n.t("menu.edit_clear"))
        edit_menu.addSeparator()
        edit_menu.addAction(self.i18n.t("menu.edit_find"))
        edit_menu.addAction(self.i18n.t("menu.edit_replace"))

    def _create_view_menu(self):
        view_menu = self.addMenu(self.i18n.t("menu.view"))
        view_menu.addAction(self.i18n.t("menu.view_data_editor"))
        view_menu.addAction(self.i18n.t("menu.view_variable_view"))
        view_menu.addAction(self.i18n.t("menu.view_output"))
        view_menu.addAction(self.i18n.t("menu.view_syntax"))

    def _create_data_menu(self):
        data_menu = self.addMenu(self.i18n.t("menu.data"))
        data_menu.addAction(self.i18n.t("menu.data_define_variables"))
        data_menu.addAction(self.i18n.t("menu.data_sort_cases"))
        data_menu.addAction(self.i18n.t("menu.data_select_cases"))
        data_menu.addAction(self.i18n.t("menu.data_weight_cases"))
        data_menu.addSeparator()
        data_menu.addAction(self.i18n.t("menu.data_transpose"))
        data_menu.addAction(self.i18n.t("menu.data_restructure"))
        data_menu.addAction(self.i18n.t("menu.data_merge_files"))
        data_menu.addAction(self.i18n.t("menu.data_split_file"))

    def _create_transform_menu(self):
        self.addMenu(self.i18n.t("menu.transform"))

    def _create_analyze_menu(self):
        analyze_menu = self.addMenu(self.i18n.t("menu.analyze"))
        analyze_menu.addAction(self.i18n.t("menu.analyze_descriptives"))
        analyze_menu.addAction(self.i18n.t("menu.analyze_frequencies"))
        analyze_menu.addAction(self.i18n.t("menu.analyze_crosstabs"))

    def _create_graphs_menu(self):
        self.addMenu(self.i18n.t("menu.graphs"))

    def _create_utilities_menu(self):
        self.addMenu(self.i18n.t("menu.utilities"))

    def _create_window_menu(self):
        self.addMenu(self.i18n.t("menu.window"))

    def _create_help_menu(self):
        help_menu = self.addMenu(self.i18n.t("menu.help"))
        help_menu.addAction(self.i18n.t("menu.help_documentation"))
        help_menu.addSeparator()
        help_menu.addAction(self.i18n.t("menu.help_about"))
