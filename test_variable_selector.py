#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试变量选择器和对话框功能
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
from axaltyx.gui.dialogs.dialog_base import DialogBase
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.gui.styles.theme_arco import ArcoTheme


class TestDialog(DialogBase):
    """测试对话框"""

    def __init__(self, parent=None):
        super().__init__(parent, "测试对话框")
        self._init_content()
    
    def _init_content(self):
        """初始化内容"""
        # 创建变量选择器
        self.variable_selector = VariableSelector()
        
        # 测试数据
        test_variables = [
            ("VAR00001", "numeric"),
            ("VAR00002", "string"),
            ("VAR00003", "numeric"),
            ("VAR00004", "string"),
            ("VAR00005", "numeric"),
            ("VAR00006", "string"),
            ("VAR00007", "numeric"),
            ("VAR00008", "string"),
        ]
        
        # 设置变量
        self.variable_selector.set_variables(test_variables)
        
        # 添加到布局
        layout = QVBoxLayout()
        layout.addWidget(self.variable_selector)
        
        # 设置内容布局
        self.set_content_layout(layout)
    
    def get_selected_variables(self):
        """获取选中的变量列表"""
        return self.variable_selector.get_selected_variables()
    
    def _on_reset(self):
        """重置按钮点击事件"""
        self.variable_selector.clear()
    
    def accept(self):
        """确定按钮点击事件"""
        selected_vars = self.get_selected_variables()
        print(f"选中的变量: {selected_vars}")
        super().accept()


class TestWindow(QMainWindow):
    """测试窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试变量选择器")
        self.setGeometry(100, 100, 800, 600)

        # 应用 Arco 主题
        self.theme = ArcoTheme()
        self.theme.apply(self)

        self._init_ui()
    
    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # 测试按钮
        test_button = QPushButton("打开测试对话框")
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #165DFF;
                color: white;
                padding: 12px 24px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #4080FF;
            }
            QPushButton:pressed {
                background-color: #0E42D2;
            }
        """)
        test_button.clicked.connect(self._open_dialog)
        layout.addWidget(test_button)

        # 结果显示
        self.result_label = QLabel("点击按钮打开对话框进行测试")
        self.result_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #4E5969;
                padding: 12px;
                background-color: #F7F8FA;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.result_label)

        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                color: #4E5969;
                padding: 12px;
                background-color: #F7F8FA;
                border: 1px solid #E5E6EB;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.status_text, 1)
    
    def _open_dialog(self):
        """打开测试对话框"""
        dialog = TestDialog(self)
        result = dialog.exec()
        
        if result == dialog.DialogCode.Accepted:
            selected_vars = dialog.get_selected_variables()
            self.result_label.setText(f"对话框已确认，选中了 {len(selected_vars)} 个变量")
            self.status_text.append(f"选中的变量: {selected_vars}")
        else:
            self.result_label.setText("对话框已取消")
            self.status_text.append("对话框已取消")


def main():
    app = QApplication(sys.argv)

    window = TestWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
