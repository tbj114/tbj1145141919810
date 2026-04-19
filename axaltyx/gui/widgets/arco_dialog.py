from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ArcoDialog(QDialog):
    """Arco Design 风格的对话框基类"""

    def __init__(self, parent=None, title="", width=520, height=480):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(width, height)
        self.setMaximumSize(1000, 800)
        self.setModal(True)
        
        # 应用样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        self.title_bar = self._create_title_bar()
        main_layout.addWidget(self.title_bar)
        
        # 内容区域
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(16)
        main_layout.addWidget(self.content_widget, 1)
        
        # 底部按钮栏
        self.button_bar = self._create_button_bar()
        main_layout.addWidget(self.button_bar)
    
    def _create_title_bar(self):
        """创建标题栏"""
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #E5E6EB;
                height: 40px;
            }
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(24, 0, 16, 0)
        layout.setSpacing(16)
        
        # 标题
        self.title_label = QLabel()
        font = QFont()
        font.setWeight(QFont.Weight.SemiBold)
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #272E3B;")
        layout.addWidget(self.title_label)
        
        # 占位
        layout.addStretch()
        
        # 关闭按钮
        close_button = QPushButton()
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #F2F3F5;
            }
            QPushButton:pressed {
                background-color: #E5E6EB;
            }
        """)
        close_button.setText("×")
        close_button.clicked.connect(self.reject)
        layout.addWidget(close_button)
        
        return title_bar
    
    def _create_button_bar(self):
        """创建底部按钮栏"""
        button_bar = QFrame()
        button_bar.setStyleSheet("""
            QFrame {
                background-color: #F7F8FA;
                border-top: 1px solid #E5E6EB;
                padding: 16px 24px;
            }
        """)
        
        layout = QHBoxLayout(button_bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # 左侧按钮
        left_layout = QHBoxLayout()
        left_layout.setSpacing(8)
        layout.addLayout(left_layout)
        
        # 占位
        layout.addStretch()
        
        # 右侧按钮
        right_layout = QHBoxLayout()
        right_layout.setSpacing(8)
        layout.addLayout(right_layout)
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton#cancel {
                background-color: white;
                border: 1px solid #C9CDD4;
                color: #4E5969;
                padding: 0 16px;
                height: 32px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#cancel:hover {
                border-color: #86909C;
                color: #272E3B;
            }
            QPushButton#cancel:pressed {
                background-color: #F2F3F5;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        right_layout.addWidget(self.cancel_button)
        
        # 确定按钮
        self.ok_button = QPushButton("确定")
        self.ok_button.setObjectName("ok")
        self.ok_button.setStyleSheet("""
            QPushButton#ok {
                background-color: #165DFF;
                color: white;
                padding: 0 16px;
                height: 32px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#ok:hover {
                background-color: #4080FF;
            }
            QPushButton#ok:pressed {
                background-color: #0E42D2;
            }
        """)
        self.ok_button.clicked.connect(self.accept)
        right_layout.addWidget(self.ok_button)
        
        return button_bar
    
    def set_title(self, title):
        """设置标题"""
        self.setWindowTitle(title)
        self.title_label.setText(title)
    
    def add_button(self, button, position="left"):
        """添加按钮到按钮栏"""
        if position == "left":
            layout = self.button_bar.layout().itemAt(0).layout()
        else:
            layout = self.button_bar.layout().itemAt(2).layout()
        layout.addWidget(button)
    
    def set_content_layout(self, layout):
        """设置内容布局"""
        # 清空现有内容
        while self.content_layout.count() > 0:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加新布局
        self.content_layout.addLayout(layout)
