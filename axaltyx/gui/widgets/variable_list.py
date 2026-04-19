from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QIcon, QFont


class VariableItem(QListWidgetItem):
    """变量列表项"""

    def __init__(self, variable_name, variable_type, parent=None):
        super().__init__(parent)
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.setText(variable_name)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled)


class VariableList(QListWidget):
    """变量列表框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #E5E6EB;
                border-radius: 4px;
                padding: 8px;
            }
            QListWidget::item {
                height: 32px;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #F2F3F5;
            }
            QListWidget::item:selected {
                background-color: #E8F3FF;
                color: #165DFF;
            }
            QListWidget::item:selected:!active {
                background-color: #E8F3FF;
            }
        """)
    
    def add_variable(self, variable_name, variable_type="numeric"):
        """添加变量"""
        item = VariableItem(variable_name, variable_type)
        self.addItem(item)
    
    def add_variables(self, variables):
        """批量添加变量"""
        for var_name, var_type in variables:
            self.add_variable(var_name, var_type)
    
    def get_selected_variables(self):
        """获取选中的变量"""
        selected = []
        for item in self.selectedItems():
            selected.append((item.variable_name, item.variable_type))
        return selected
    
    def get_all_variables(self):
        """获取所有变量"""
        variables = []
        for i in range(self.count()):
            item = self.item(i)
            variables.append((item.variable_name, item.variable_type))
        return variables
    
    def remove_selected(self):
        """移除选中的变量"""
        for item in self.selectedItems():
            self.takeItem(self.row(item))
    
    def clear_all(self):
        """清空所有变量"""
        self.clear()
    
    def startDrag(self, supportedActions):
        """开始拖拽"""
        if not self.selectedItems():
            return
        
        mime_data = QMimeData()
        selected_items = self.selectedItems()
        item_texts = [item.variable_name for item in selected_items]
        mime_data.setText("|" .join(item_texts))
        
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        
        if drag.exec(Qt.DropAction.MoveAction) == Qt.DropAction.MoveAction:
            for item in selected_items:
                self.takeItem(self.row(item))
    
    def dropEvent(self, event):
        """处理放置事件"""
        if event.source() == self:
            mime_data = event.mimeData()
            if mime_data.hasText():
                variable_names = mime_data.text().split("|")
                
                # 获取目标位置
                drop_row = self.indexAt(event.position().toPoint()).row()
                if drop_row == -1:
                    drop_row = self.count()
                
                # 插入变量
                for var_name in variable_names:
                    # 查找变量类型
                    var_type = "numeric"  # 默认类型
                    # 这里可以根据需要从数据源获取实际类型
                    
                    item = VariableItem(var_name, var_type)
                    self.insertItem(drop_row, item)
                    drop_row += 1
                
                event.acceptProposedAction()
    
    def dragEnterEvent(self, event):
        """处理拖拽进入事件"""
        if event.source() == self:
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        """处理拖拽移动事件"""
        if event.source() == self:
            event.acceptProposedAction()
