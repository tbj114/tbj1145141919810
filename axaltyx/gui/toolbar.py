from PyQt6.QtWidgets import QToolBar, QWidget, QToolButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from axaltyx.i18n import I18nManager


class ToolBar(QToolBar):
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
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        
        self._add_action("📄", "menu.file_new", self.new_file.emit)
        self._add_action("📂", "menu.file_open", self.open_file.emit)
        self._add_action("💾", "menu.file_save", self.save_file.emit)
        self.addSeparator()
        self._add_action("↩️", "menu.edit_undo", self.undo.emit)
        self._add_action("↪️", "menu.edit_redo", self.redo.emit)
        self.addSeparator()
        self._add_action("📋", "menu.edit_copy", self.copy.emit)
        self._add_action("📝", "menu.edit_paste", self.paste.emit)
        self.addSeparator()
        self._add_action("▶️", "menu.run", self.run.emit)

    def _add_action(self, icon_text, text_key, slot):
        button = QToolButton()
        button.setText(icon_text)
        button.setToolTip(self.i18n.t(text_key))
        button.clicked.connect(slot)
        self.addWidget(button)
