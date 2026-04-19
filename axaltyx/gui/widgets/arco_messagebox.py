#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arco Design 风格的消息框
"""

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt


class ArcoMessageBox(QMessageBox):
    """Arco Design 风格的消息框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()
    
    def _apply_style(self):
        self.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #272E3B;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #165DFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4080FF;
            }
            QMessageBox QPushButton:pressed {
                background-color: #0E42D2;
            }
        """)
    
    @staticmethod
    def information(parent, title, text, buttons=QMessageBox.StandardButton.Ok):
        msg_box = ArcoMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        return msg_box.exec()
    
    @staticmethod
    def warning(parent, title, text, buttons=QMessageBox.StandardButton.Ok):
        msg_box = ArcoMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        return msg_box.exec()
    
    @staticmethod
    def critical(parent, title, text, buttons=QMessageBox.StandardButton.Ok):
        msg_box = ArcoMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        return msg_box.exec()
    
    @staticmethod
    def question(parent, title, text, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No):
        msg_box = ArcoMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        return msg_box.exec()