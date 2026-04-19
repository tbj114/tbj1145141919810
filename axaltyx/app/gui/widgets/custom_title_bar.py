from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon, QMouseEvent


class CustomTitleBar(QWidget):
    minimizeClicked = pyqtSignal()
    maximizeClicked = pyqtSignal()
    closeClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            CustomTitleBar {
                background-color: #f7f8fa;
                border-bottom: 1px solid #e5e6eb;
            }
        """)
        self._is_dragging = False
        self._drag_position = QPoint()
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        self.title_label = QLabel("AxaltyX")
        self.title_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        layout.addWidget(self.title_label)

        layout.addStretch()

        self.min_btn = QPushButton()
        self.min_btn.setFixedSize(40, 30)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e8f3ff;
            }
        """)
        self.min_btn.setText("—")
        self.min_btn.clicked.connect(self.minimizeClicked.emit)
        layout.addWidget(self.min_btn)

        self.max_btn = QPushButton()
        self.max_btn.setFixedSize(40, 30)
        self.max_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e8f3ff;
            }
        """)
        self.max_btn.setText("□")
        self.max_btn.clicked.connect(self.maximizeClicked.emit)
        layout.addWidget(self.max_btn)

        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(40, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f53f3f;
                color: white;
            }
        """)
        self.close_btn.setText("×")
        self.close_btn.clicked.connect(self.closeClicked.emit)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def set_title(self, title):
        self.title_label.setText(title)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_position)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._is_dragging = False

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.maximizeClicked.emit()
