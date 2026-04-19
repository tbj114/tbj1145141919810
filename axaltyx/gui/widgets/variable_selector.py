from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from axaltyx.gui.widgets.variable_list import VariableList
from axaltyx.gui.widgets.transfer_button import TransferButton
from axaltyx.i18n import I18nManager


class VariableSelector(QWidget):
    """变量选择器组合控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)
        
        # 左侧：可用变量列表
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        main_layout.addLayout(left_layout)
        
        # 可用变量标签
        left_label = QLabel(self.i18n.t("dialogs.common.available_variables"))
        left_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #272E3B;
            }
        """)
        left_layout.addWidget(left_label)
        
        # 可用变量列表
        self.available_list = VariableList()
        left_layout.addWidget(self.available_list, 1)
        
        # 中间：移动按钮组
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(button_layout)
        
        self.transfer_buttons = TransferButton()
        self.transfer_buttons.move_all_right.connect(self._move_all_right)
        self.transfer_buttons.move_selected_right.connect(self._move_selected_right)
        self.transfer_buttons.move_selected_left.connect(self._move_selected_left)
        self.transfer_buttons.move_all_left.connect(self._move_all_left)
        button_layout.addWidget(self.transfer_buttons)
        
        # 右侧：已选变量列表
        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)
        main_layout.addLayout(right_layout)
        
        # 已选变量标签
        right_label = QLabel(self.i18n.t("dialogs.common.analysis_variables"))
        right_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #272E3B;
            }
        """)
        right_layout.addWidget(right_label)
        
        # 已选变量列表
        self.selected_list = VariableList()
        right_layout.addWidget(self.selected_list, 1)
    
    def _move_all_right(self):
        """移动所有变量到右侧"""
        variables = self.available_list.get_all_variables()
        for var_name, var_type in variables:
            self.selected_list.add_variable(var_name, var_type)
        self.available_list.clear_all()
    
    def _move_selected_right(self):
        """移动选中变量到右侧"""
        variables = self.available_list.get_selected_variables()
        for var_name, var_type in variables:
            self.selected_list.add_variable(var_name, var_type)
        self.available_list.remove_selected()
    
    def _move_selected_left(self):
        """移动选中变量到左侧"""
        variables = self.selected_list.get_selected_variables()
        for var_name, var_type in variables:
            self.available_list.add_variable(var_name, var_type)
        self.selected_list.remove_selected()
    
    def _move_all_left(self):
        """移动所有变量到左侧"""
        variables = self.selected_list.get_all_variables()
        for var_name, var_type in variables:
            self.available_list.add_variable(var_name, var_type)
        self.selected_list.clear_all()
    
    def set_variables(self, variables):
        """设置变量列表"""
        # 清空现有列表
        self.available_list.clear_all()
        self.selected_list.clear_all()
        
        # 添加变量到可用列表
        self.available_list.add_variables(variables)
    
    def get_selected_variables(self):
        """获取选中的变量列表"""
        return self.selected_list.get_all_variables()
    
    def clear(self):
        """清空所有变量"""
        self.available_list.clear_all()
        self.selected_list.clear_all()
