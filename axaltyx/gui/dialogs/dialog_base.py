from PyQt6.QtWidgets import QPushButton, QVBoxLayout
from axaltyx.gui.widgets.arco_dialog import ArcoDialog
from axaltyx.i18n import I18nManager


class DialogBase(ArcoDialog):
    """分析对话框基类"""

    def __init__(self, parent=None, title="", width=520, height=480):
        super().__init__(parent, title, width, height)
        self.i18n = I18nManager()
        self._init_buttons()
    
    def _init_buttons(self):
        """初始化按钮"""
        # 移除默认的确定和取消按钮
        self.ok_button.deleteLater()
        self.cancel_button.deleteLater()
        
        # 重新创建底部按钮
        right_layout = self.button_bar.layout().itemAt(2).layout()
        
        # 粘贴按钮
        paste_button = QPushButton(self.i18n.t("dialogs.common.paste"))
        paste_button.setObjectName("paste")
        paste_button.setStyleSheet("""
            QPushButton#paste {
                background-color: transparent;
                border: none;
                color: #4E5969;
                padding: 0 16px;
                height: 32px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#paste:hover {
                color: #165DFF;
                background-color: #F2F3F5;
                border-radius: 4px;
            }
            QPushButton#paste:pressed {
                background-color: #E5E6EB;
            }
        """)
        paste_button.clicked.connect(self._on_paste)
        
        # 重置按钮
        reset_button = QPushButton(self.i18n.t("dialogs.common.reset"))
        reset_button.setObjectName("reset")
        reset_button.setStyleSheet("""
            QPushButton#reset {
                background-color: transparent;
                border: none;
                color: #4E5969;
                padding: 0 16px;
                height: 32px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#reset:hover {
                color: #165DFF;
                background-color: #F2F3F5;
                border-radius: 4px;
            }
            QPushButton#reset:pressed {
                background-color: #E5E6EB;
            }
        """)
        reset_button.clicked.connect(self._on_reset)
        
        # 取消按钮
        cancel_button = QPushButton(self.i18n.t("dialogs.common.cancel"))
        cancel_button.setObjectName("cancel")
        cancel_button.setStyleSheet("""
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
        cancel_button.clicked.connect(self.reject)
        
        # 确定按钮
        ok_button = QPushButton(self.i18n.t("dialogs.common.ok"))
        ok_button.setObjectName("ok")
        ok_button.setStyleSheet("""
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
        ok_button.clicked.connect(self.accept)
        
        # 添加按钮到布局
        right_layout.addWidget(paste_button)
        right_layout.addWidget(reset_button)
        right_layout.addWidget(cancel_button)
        right_layout.addWidget(ok_button)
        
        # 保存按钮引用
        self.paste_button = paste_button
        self.reset_button = reset_button
        self.cancel_button = cancel_button
        self.ok_button = ok_button
    
    def _on_paste(self):
        """粘贴按钮点击事件"""
        pass
    
    def _on_reset(self):
        """重置按钮点击事件"""
        pass
    
    def get_selected_variables(self):
        """获取选中的变量列表"""
        return []
    
    def set_variables(self, variables):
        """设置变量列表"""
        pass
    
    def accept(self):
        """确定按钮点击事件"""
        super().accept()
    
    def reject(self):
        """取消按钮点击事件"""
        super().reject()
