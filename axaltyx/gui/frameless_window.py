#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
无边框窗口基类
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QCursor, QMouseEvent

from .title_bar import TitleBar


class FramelessWindow(QWidget):
    """无边框窗口基类"""
    
    def __init__(self):
        """初始化无边框窗口"""
        super().__init__()
        
        # 设置无边框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 初始化布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建标题栏
        self.title_bar = TitleBar(self)
        self.main_layout.addWidget(self.title_bar)
        
        # 内容区域
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: white;")
        self.main_layout.addWidget(self.content_widget)
        
        # 拖拽相关变量
        self.drag_pos = QPoint()
        self.is_dragging = False
        
        # 调整大小相关变量
        self.resize_edge = None
        self.resize_margin = 8
        
        # 设置默认大小
        self.setMinimumSize(800, 600)
    
    def set_title(self, title):
        """设置窗口标题"""
        self.title_bar.set_title(title)
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 检查是否在标题栏区域
            if self.title_bar.geometry().contains(event.pos()):
                self.is_dragging = True
                self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
            else:
                # 检查是否在窗口边缘
                self.resize_edge = self._get_resize_edge(event.pos())
                if self.resize_edge:
                    event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.is_dragging:
                # 拖拽移动窗口
                self.move(event.globalPos() - self.drag_pos)
                event.accept()
            elif self.resize_edge:
                # 调整窗口大小
                self._resize_window(event)
                event.accept()
        else:
            # 检查鼠标是否在窗口边缘，更新光标
            edge = self._get_resize_edge(event.pos())
            self._set_cursor(edge)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        self.is_dragging = False
        self.resize_edge = None
        self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def _get_resize_edge(self, pos):
        """获取调整大小的边缘"""
        rect = self.rect()
        margin = self.resize_margin
        
        if pos.x() <= margin and pos.y() <= margin:
            return "top-left"
        elif pos.x() >= rect.width() - margin and pos.y() <= margin:
            return "top-right"
        elif pos.x() <= margin and pos.y() >= rect.height() - margin:
            return "bottom-left"
        elif pos.x() >= rect.width() - margin and pos.y() >= rect.height() - margin:
            return "bottom-right"
        elif pos.x() <= margin:
            return "left"
        elif pos.x() >= rect.width() - margin:
            return "right"
        elif pos.y() <= margin:
            return "top"
        elif pos.y() >= rect.height() - margin:
            return "bottom"
        return None
    
    def _set_cursor(self, edge):
        """设置光标形状"""
        if edge == "top-left" or edge == "bottom-right":
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge == "top-right" or edge == "bottom-left":
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge == "left" or edge == "right":
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge == "top" or edge == "bottom":
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def _resize_window(self, event):
        """调整窗口大小"""
        global_pos = event.globalPos()
        rect = self.frameGeometry()
        
        if self.resize_edge == "top-left":
            rect.setTopLeft(global_pos)
        elif self.resize_edge == "top-right":
            rect.setTopRight(global_pos)
        elif self.resize_edge == "bottom-left":
            rect.setBottomLeft(global_pos)
        elif self.resize_edge == "bottom-right":
            rect.setBottomRight(global_pos)
        elif self.resize_edge == "left":
            rect.setLeft(global_pos.x())
        elif self.resize_edge == "right":
            rect.setRight(global_pos.x())
        elif self.resize_edge == "top":
            rect.setTop(global_pos.y())
        elif self.resize_edge == "bottom":
            rect.setBottom(global_pos.y())
        
        # 确保窗口不小于最小尺寸
        if rect.width() >= self.minimumWidth() and rect.height() >= self.minimumHeight():
            self.setGeometry(rect)

