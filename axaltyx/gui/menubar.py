from PyQt6.QtWidgets import QMenuBar, QMenu, QWidget
from PyQt6.QtCore import pyqtSignal
from axaltyx.i18n import I18nManager


class MenuBar(QMenuBar):
    # 文件菜单信号
    new_file = pyqtSignal()
    open_file = pyqtSignal()
    save_file = pyqtSignal()
    save_as = pyqtSignal()
    close_file = pyqtSignal()
    exit_app = pyqtSignal()
    
    # 编辑菜单信号
    undo = pyqtSignal()
    redo = pyqtSignal()
    cut = pyqtSignal()
    copy = pyqtSignal()
    paste = pyqtSignal()
    find = pyqtSignal()
    replace = pyqtSignal()
    
    # 数据菜单信号
    define_variables = pyqtSignal()
    sort_cases = pyqtSignal()
    select_cases = pyqtSignal()
    weight_cases = pyqtSignal()
    transpose = pyqtSignal()
    restructure = pyqtSignal()
    merge_files = pyqtSignal()
    split_file = pyqtSignal()
    
    # 视图菜单信号
    toggle_panel = pyqtSignal(str)  # 面板名称作为参数
    
    # 帮助菜单信号
    show_about = pyqtSignal()
    
    # 运行信号
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
        
        save_as_action = file_menu.addAction(self.i18n.t("menu.file_save_as"))
        save_as_action.triggered.connect(self.save_as.emit)
        
        file_menu.addSeparator()
        close_action = file_menu.addAction(self.i18n.t("menu.file_close"))
        close_action.triggered.connect(self.close_file.emit)
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction(self.i18n.t("menu.file_exit"))
        exit_action.triggered.connect(self.exit_app.emit)

    def _create_edit_menu(self):
        edit_menu = self.addMenu(self.i18n.t("menu.edit"))
        undo_action = edit_menu.addAction(self.i18n.t("menu.edit_undo"))
        undo_action.triggered.connect(self.undo.emit)
        
        redo_action = edit_menu.addAction(self.i18n.t("menu.edit_redo"))
        redo_action.triggered.connect(self.redo.emit)
        
        edit_menu.addSeparator()
        cut_action = edit_menu.addAction(self.i18n.t("menu.edit_cut"))
        cut_action.triggered.connect(self.cut.emit)
        
        copy_action = edit_menu.addAction(self.i18n.t("menu.edit_copy"))
        copy_action.triggered.connect(self.copy.emit)
        
        paste_action = edit_menu.addAction(self.i18n.t("menu.edit_paste"))
        paste_action.triggered.connect(self.paste.emit)
        
        edit_menu.addSeparator()
        find_action = edit_menu.addAction(self.i18n.t("menu.edit_find"))
        find_action.triggered.connect(self.find.emit)
        
        replace_action = edit_menu.addAction(self.i18n.t("menu.edit_replace"))
        replace_action.triggered.connect(self.replace.emit)

    def _create_view_menu(self):
        view_menu = self.addMenu(self.i18n.t("menu.view"))
        data_editor_action = view_menu.addAction(self.i18n.t("menu.view_data_editor"))
        data_editor_action.triggered.connect(lambda: self.toggle_panel.emit("data_editor"))
        
        variable_view_action = view_menu.addAction(self.i18n.t("menu.view_variable_view"))
        variable_view_action.triggered.connect(lambda: self.toggle_panel.emit("variable_view"))
        
        output_action = view_menu.addAction(self.i18n.t("menu.view_output"))
        output_action.triggered.connect(lambda: self.toggle_panel.emit("output"))
        
        syntax_action = view_menu.addAction(self.i18n.t("menu.view_syntax"))
        syntax_action.triggered.connect(lambda: self.toggle_panel.emit("syntax"))

    def _create_data_menu(self):
        data_menu = self.addMenu(self.i18n.t("menu.data"))
        define_action = data_menu.addAction(self.i18n.t("menu.data_define_variables"))
        define_action.triggered.connect(self.define_variables.emit)
        
        sort_action = data_menu.addAction(self.i18n.t("menu.data_sort_cases"))
        sort_action.triggered.connect(self.sort_cases.emit)
        
        select_action = data_menu.addAction(self.i18n.t("menu.data_select_cases"))
        select_action.triggered.connect(self.select_cases.emit)
        
        weight_action = data_menu.addAction(self.i18n.t("menu.data_weight_cases"))
        weight_action.triggered.connect(self.weight_cases.emit)
        
        data_menu.addSeparator()
        transpose_action = data_menu.addAction(self.i18n.t("menu.data_transpose"))
        transpose_action.triggered.connect(self.transpose.emit)
        
        restructure_action = data_menu.addAction(self.i18n.t("menu.data_restructure"))
        restructure_action.triggered.connect(self.restructure.emit)
        
        merge_action = data_menu.addAction(self.i18n.t("menu.data_merge_files"))
        merge_action.triggered.connect(self.merge_files.emit)
        
        split_action = data_menu.addAction(self.i18n.t("menu.data_split_file"))
        split_action.triggered.connect(self.split_file.emit)

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
        about_action = help_menu.addAction(self.i18n.t("menu.help_about"))
        about_action.triggered.connect(self.show_about.emit)
