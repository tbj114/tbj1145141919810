from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from axaltyx.gui.widgets.output_tree import OutputTree, OutputTreeItem
from axaltyx.gui.widgets.output_viewer import OutputViewer
from axaltyx.i18n.i18n_manager import I18nManager

class OutputTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for output tree and viewer
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create output tree
        self.output_tree = OutputTree(self)
        
        # Create output viewer
        self.output_viewer = OutputViewer(self)
        
        # Add widgets to splitter
        self.splitter.addWidget(self.output_tree)
        self.splitter.addWidget(self.output_viewer)
        
        # Set initial sizes
        self.splitter.setSizes([200, 600])
        
        layout.addWidget(self.splitter)
    
    def _connect_signals(self):
        # Connect output tree signals
        self.output_tree.item_selected.connect(self._on_item_selected)
        self.output_tree.item_deleted.connect(self._on_item_deleted)
        self.output_tree.item_exported.connect(self._on_item_exported)
    
    def _on_item_selected(self, item):
        # Handle item selection - scroll to corresponding content in viewer
        # This would require tracking content positions, but for now we'll just clear and show selected item
        if item:
            self.output_viewer.clear_content()
            
            # Display item content based on type
            if item.item_type == 'log':
                self.output_viewer.add_log(item.data(0, OutputTreeItem.DataRole.CONTENT))
            elif item.item_type == 'title':
                self.output_viewer.add_title(item.data(0, OutputTreeItem.DataRole.CONTENT))
            elif item.item_type == 'table':
                headers = item.data(0, OutputTreeItem.DataRole.HEADERS)
                rows = item.data(0, OutputTreeItem.DataRole.ROWS)
                if headers and rows:
                    self.output_viewer.add_table(headers, rows)
            elif item.item_type == 'chart':
                figure = item.data(0, OutputTreeItem.DataRole.CONTENT)
                if figure:
                    self.output_viewer.add_chart(figure)
            elif item.item_type == 'text':
                self.output_viewer.add_text(item.data(0, OutputTreeItem.DataRole.CONTENT))
    
    def _on_item_deleted(self, item):
        # Handle item deletion
        pass
    
    def _on_item_exported(self, item, export_format):
        # Handle item export
        pass
    
    def clear_output(self):
        """Clear all output content"""
        self.output_tree.clear()
        self.output_viewer.clear_content()
    
    def add_output_item(self, item_type, content, title=None, headers=None, rows=None):
        """Add a new output item to the tree and viewer"""
        # Add to tree
        tree_item = self.output_tree.add_item(item_type, content, title, headers, rows)
        
        # Add to viewer
        if item_type == 'log':
            self.output_viewer.add_log(content)
        elif item_type == 'title':
            self.output_viewer.add_title(content)
        elif item_type == 'table':
            if headers and rows:
                self.output_viewer.add_table(headers, rows)
        elif item_type == 'chart':
            self.output_viewer.add_chart(content)
        elif item_type == 'text':
            self.output_viewer.add_text(content)
        
        return tree_item