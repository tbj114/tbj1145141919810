from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableView, QSplitter
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.utils.locale_manager import tr


class DataTableModel(QAbstractTableModel):
    def __init__(self, rows=100, cols=100, parent=None):
        super().__init__(parent)
        self._data = [['' for _ in range(cols)] for _ in range(rows)]
        self._headers = [f'var{i+1}' for i in range(cols)]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self._data[index.row()][index.column()]
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section] if section < len(self._headers) else str(section + 1)
            else:
                return str(section + 1)
        return None

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable


class DataEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.South)

        self.data_view = QTableView()
        self.data_model = DataTableModel(100, 100)
        self.data_view.setModel(self.data_model)

        self.variable_view = QTableView()
        self.variable_model = DataTableModel(100, 10)
        self.variable_view.setModel(self.variable_model)

        self.tab_widget.addTab(self.data_view, tr('data_editor.data_view'))
        self.tab_widget.addTab(self.variable_view, tr('data_editor.variable_view'))

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
