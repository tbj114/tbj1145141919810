from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class TransferButton(QWidget):
    """变量移动按钮组"""

    # 信号定义
    move_all_right = pyqtSignal()    # 移动所有到右侧
    move_selected_right = pyqtSignal()  # 移动选中到右侧
    move_selected_left = pyqtSignal()   # 移动选中到左侧
    move_all_left = pyqtSignal()     # 移动所有到左侧

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(8)
        
        # 移动所有到右侧按钮
        self.btn_move_all_right = QPushButton(">>")
        self._setup_button(self.btn_move_all_right)
        self.btn_move_all_right.clicked.connect(self.move_all_right.emit)
        layout.addWidget(self.btn_move_all_right)
        
        # 移动选中到右侧按钮
        self.btn_move_right = QPushButton(">")
        self._setup_button(self.btn_move_right)
        self.btn_move_right.clicked.connect(self.move_selected_right.emit)
        layout.addWidget(self.btn_move_right)
        
        # 移动选中到左侧按钮
        self.btn_move_left = QPushButton("<")
        self._setup_button(self.btn_move_left)
        self.btn_move_left.clicked.connect(self.move_selected_left.emit)
        layout.addWidget(self.btn_move_left)
        
        # 移动所有到左侧按钮
        self.btn_move_all_left = QPushButton("<<")
        self._setup_button(self.btn_move_all_left)
        self.btn_move_all_left.clicked.connect(self.move_all_left.emit)
        layout.addWidget(self.btn_move_all_left)
    
    def _setup_button(self, button):
        """设置按钮样式"""
        button.setFixedSize(28, 28)
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #C9CDD4;
                border-radius: 4px;
                color: #4E5969;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                border-color: #165DFF;
                color: #165DFF;
            }
            QPushButton:pressed {
                background-color: #E8F3FF;
                border-color: #165DFF;
            }
            QPushButton:disabled {
                background-color: #F7F8FA;
                border-color: #E5E6EB;
                color: #A9AEB8;
            }
        """)
    
    def set_enabled(self, enabled):
        """设置所有按钮的启用状态"""
        self.btn_move_all_right.setEnabled(enabled)
        self.btn_move_right.setEnabled(enabled)
        self.btn_move_left.setEnabled(enabled)
        self.btn_move_all_left.setEnabled(enabled)
