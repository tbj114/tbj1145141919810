from PyQt6.QtWidgets import QTextBrowser, QMenu, QFileDialog, QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QContextMenuEvent, QAction, QClipboard, QPixmap
import matplotlib.pyplot as plt
import io
from axaltyx.i18n.i18n_manager import I18nManager

class OutputViewer(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setReadOnly(True)
        self.setOpenExternalLinks(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self._setup_style()
    
    def _setup_style(self):
        self.setStyleSheet("""
            QTextBrowser {
                background-color: #f8f9fa;
                color: #333;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                border: none;
            }
            QTextBrowser::viewport {
                background-color: #f8f9fa;
            }
            QTextBrowser::focus {
                outline: none;
            }
        """)
    
    def _show_context_menu(self, pos):
        menu = QMenu(self)
        
        copy_action = QAction(self.i18n.translate('output', 'copy'), self)
        copy_action.triggered.connect(self._copy_selection)
        menu.addAction(copy_action)
        
        menu.addSeparator()
        
        export_html_action = QAction(self.i18n.translate('output', 'export_html'), self)
        export_html_action.triggered.connect(self._export_html)
        menu.addAction(export_html_action)
        
        export_pdf_action = QAction(self.i18n.translate('output', 'export_pdf'), self)
        export_pdf_action.triggered.connect(self._export_pdf)
        menu.addAction(export_pdf_action)
        
        export_png_action = QAction(self.i18n.translate('output', 'export_png'), self)
        export_png_action.triggered.connect(self._export_png)
        menu.addAction(export_png_action)
        
        menu.exec(self.mapToGlobal(pos))
    
    def _copy_selection(self):
        QApplication.clipboard().setText(self.textCursor().selectedText())
    
    def _export_html(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            self.i18n.translate('output', 'export_html'), 
            "", 
            "HTML Files (*.html);;All Files (*)"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.toHtml())
    
    def _export_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            self.i18n.translate('output', 'export_pdf'), 
            "", 
            "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)
            self.print(printer)
    
    def _export_png(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            self.i18n.translate('output', 'export_png'), 
            "", 
            "PNG Files (*.png);;All Files (*)"
        )
        if file_path:
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            pixmap.save(file_path, "PNG")
    
    def clear_content(self):
        self.clear()
    
    def add_log(self, text):
        html = f"<div style='color: #666; font-style: italic; margin: 5px 0;'>{text}</div>"
        self.insertHtml(html)
        self.append("<br>")
    
    def add_title(self, title, level=1):
        if level == 1:
            html = f"<h1 style='color: #2c3e50; margin: 20px 0 10px 0;'>{title}</h1>"
        elif level == 2:
            html = f"<h2 style='color: #34495e; margin: 15px 0 8px 0;'>{title}</h2>"
        elif level == 3:
            html = f"<h3 style='color: #34495e; margin: 10px 0 5px 0;'>{title}</h3>"
        else:
            html = f"<h4 style='color: #34495e; margin: 8px 0 3px 0;'>{title}</h4>"
        self.insertHtml(html)
        self.append("<br>")
    
    def add_text(self, text):
        html = f"<div style='margin: 5px 0;'>{text}</div>"
        self.insertHtml(html)
        self.append("<br>")
    
    def add_table(self, headers, rows):
        html = "<table style='border-collapse: collapse; width: 100%; margin: 10px 0;'>"
        
        # Header row
        html += "<tr style='background-color: #e3f2fd;'>"
        for header in headers:
            html += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: left; font-weight: bold;'>{header}</th>"
        html += "</tr>"
        
        # Data rows with alternating background
        for i, row in enumerate(rows):
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            html += f"<tr style='background-color: {bg_color};'>"
            for cell in row:
                html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{cell}</td>"
            html += "</tr>"
        
        html += "</table>"
        self.insertHtml(html)
        self.append("<br>")
    
    def add_chart(self, figure):
        buf = io.BytesIO()
        figure.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        
        img_tag = f"<img src='data:image/png;base64,{buf.getvalue().hex()}' style='max-width: 100%; margin: 10px 0;'>"
        self.insertHtml(img_tag)
        self.append("<br>")
        
        plt.close(figure)
    
    def add_html(self, html):
        self.insertHtml(html)
        self.append("<br>")