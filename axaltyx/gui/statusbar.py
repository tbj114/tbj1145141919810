from PyQt6.QtWidgets import QStatusBar, QWidget, QLabel
from axaltyx.i18n import I18nManager


class StatusBar(QStatusBar):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()

    def _init_ui(self):
        self.status_label = QLabel(self.i18n.t("app.ready"))
        self.addWidget(self.status_label, 1)
        
        self.row_col_label = QLabel("0 × 0")
        self.addPermanentWidget(self.row_col_label)

    def show_message(self, text: str, timeout: int = 0):
        """显示消息 - 与QStatusBar API保持一致"""
        self.status_label.setText(text)
        self.showMessage(text, timeout)
    
    def showMessage(self, text: str, timeout: int = 0):
        """显示消息 - 标准Qt API"""
        super().showMessage(text, timeout)
    
    def set_status(self, text: str):
        self.status_label.setText(text)

    def set_row_col(self, rows: int, cols: int):
        self.row_col_label.setText(f"{rows} × {cols}")
