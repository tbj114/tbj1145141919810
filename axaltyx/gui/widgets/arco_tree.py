from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QStyle, QStyleOptionViewItem
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class ArcoTreeDelegate(QStyledItemDelegate):
    """Arco Design 风格的树控件代理"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.primary_color = QColor("#165DFF")
        self.primary_light = QColor("#E8F3FF")
        self.gray_1 = QColor("#F7F8FA")
        self.gray_2 = QColor("#F2F3F5")
        self.gray_3 = QColor("#E5E6EB")
        self.gray_6 = QColor("#86909C")
        self.gray_8 = QColor("#4E5969")

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()

        rect = option.rect

        # 处理选中态和悬浮态
        is_selected = option.state & QStyle.StateFlag.State_Selected
        is_hovered = option.state & QStyle.StateFlag.State_MouseOver

        if is_selected:
            # 选中态背景
            painter.fillRect(rect, QBrush(self.primary_light))
            # 左侧 2px 蓝色指示条
            painter.fillRect(QRect(rect.left(), rect.top(), 2, rect.height()), QBrush(self.primary_color))
        elif is_hovered:
            # 悬浮态背景
            painter.fillRect(rect, QBrush(self.gray_2))

        # 绘制文字
        if is_selected:
            painter.setPen(self.primary_color)
        else:
            painter.setPen(self.gray_8)

        text = index.data(Qt.ItemDataRole.DisplayRole)
        # 为文字留出左侧空间（包括展开图标和可能的缩进）
        text_rect = QRect(rect.left() + 24, rect.top(), rect.width() - 24, rect.height())
        
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        size = super().sizeHint(option, index)
        return QSize(size.width(), 32)


class ArcoTreeItem(QTreeWidgetItem):
    """Arco Design 风格的树控件项"""

    def __init__(self, parent=None, icon_key=None):
        super().__init__(parent)
        self.icon_key = icon_key
        self.command = None


class ArcoTree(QTreeWidget):
    """Arco Design 风格的树控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setIndentation(16)
        self.setRootIsDecorated(False)
        self.setAnimated(True)
        self.setItemDelegate(ArcoTreeDelegate(self))
        self.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
                outline: none;
            }
            QTreeWidget::item {
                height: 32px;
                padding-left: 8px;
            }
            QTreeWidget::item:hover {
                background-color: transparent;
            }
            QTreeWidget::item:selected {
                background-color: transparent;
            }
            QTreeWidget::branch {
                background-color: transparent;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                border-image: none;
                image: none;
            }
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {
                border-image: none;
                image: none;
            }
        """)

    def expandAll(self):
        """展开所有项"""
        super().expandAll()
