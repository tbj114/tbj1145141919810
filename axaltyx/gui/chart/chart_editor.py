#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表编辑器
"""

import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from axaltyx.charting import (
    BarChart, LineChart, ScatterChart, Histogram, BoxPlot, PieChart,
    Heatmap, NetworkPlot, SankeyDiagram, WordcloudChart, MultiPanel
)
import numpy as np
import pandas as pd


class ChartEditor:
    """图表编辑器"""
    
    def __init__(self, root):
        """初始化图表编辑器
        
        Args:
            root: 根窗口
        """
        self.root = root
        self.root.title("高级图表编辑器")
        self.root.geometry("1200x900")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧控制面板
        self.control_panel = ttk.LabelFrame(self.main_frame, text="编辑面板")
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=False)
        
        # 创建右侧图表区域
        self.chart_frame = ttk.LabelFrame(self.main_frame, text="图表预览")
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        # 初始化图表类型选择
        self._init_chart_type()
        
        # 初始化数据输入
        self._init_data_input()
        
        # 初始化图表参数
        self._init_chart_params()
        
        # 初始化多面板设置
        self._init_multi_panel()
        
        # 初始化按钮
        self._init_buttons()
        
        # 初始化图表
        self.chart = None
        self.canvas = None
        
    def _init_chart_type(self):
        """初始化图表类型选择"""
        ttk.Label(self.control_panel, text="图表类型:").pack(padx=10, pady=5, anchor=tk.W)
        
        self.chart_type = tk.StringVar()
        chart_types = [
            "柱状图", "折线图", "散点图", "直方图", "箱线图", "饼图",
            "热力图", "网络图", "桑基图", "词云图", "多面板图"
        ]
        self.chart_type_combo = ttk.Combobox(self.control_panel, textvariable=self.chart_type, values=chart_types)
        self.chart_type_combo.current(0)
        self.chart_type_combo.pack(padx=10, pady=5, fill=tk.X)
        
        # 绑定图表类型变化事件
        self.chart_type_combo.bind("<<ComboboxSelected>>", self._on_chart_type_change)
    
    def _init_data_input(self):
        """初始化数据输入"""
        ttk.Label(self.control_panel, text="数据输入:").pack(padx=10, pady=5, anchor=tk.W)
        
        self.data_input = tk.Text(self.control_panel, height=10, width=30)
        self.data_input.pack(padx=10, pady=5, fill=tk.X)
        
        # 默认数据
        default_data = "类别A,30\n类别B,25\n类别C,20\n类别D,15\n类别E,10"
        self.data_input.insert(tk.END, default_data)
        
        # 数据导入按钮
        self.import_button = ttk.Button(self.control_panel, text="导入数据", command=self.import_data)
        self.import_button.pack(padx=10, pady=5, fill=tk.X)
    
    def _init_chart_params(self):
        """初始化图表参数"""
        ttk.Label(self.control_panel, text="图表参数:").pack(padx=10, pady=5, anchor=tk.W)
        
        # 标题
        ttk.Label(self.control_panel, text="标题:").pack(padx=10, pady=2, anchor=tk.W)
        self.title_input = ttk.Entry(self.control_panel)
        self.title_input.insert(0, "测试图表")
        self.title_input.pack(padx=10, pady=2, fill=tk.X)
        
        # X轴标签
        ttk.Label(self.control_panel, text="X轴标签:").pack(padx=10, pady=2, anchor=tk.W)
        self.xlabel_input = ttk.Entry(self.control_panel)
        self.xlabel_input.insert(0, "类别")
        self.xlabel_input.pack(padx=10, pady=2, fill=tk.X)
        
        # Y轴标签
        ttk.Label(self.control_panel, text="Y轴标签:").pack(padx=10, pady=2, anchor=tk.W)
        self.ylabel_input = ttk.Entry(self.control_panel)
        self.ylabel_input.insert(0, "数值")
        self.ylabel_input.pack(padx=10, pady=2, fill=tk.X)
        
        # 交互设置
        self.interactive_var = tk.BooleanVar()
        self.interactive_check = ttk.Checkbutton(self.control_panel, text="启用交互", variable=self.interactive_var)
        self.interactive_check.pack(padx=10, pady=5, anchor=tk.W)
    
    def _init_multi_panel(self):
        """初始化多面板设置"""
        self.multi_panel_frame = ttk.LabelFrame(self.control_panel, text="多面板设置")
        self.multi_panel_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # 行数
        ttk.Label(self.multi_panel_frame, text="行数:").pack(padx=10, pady=2, anchor=tk.W)
        self.rows_input = ttk.Spinbox(self.multi_panel_frame, from_=1, to=10, width=5)
        self.rows_input.delete(0, tk.END)
        self.rows_input.insert(0, "2")
        self.rows_input.pack(padx=10, pady=2, fill=tk.X)
        
        # 列数
        ttk.Label(self.multi_panel_frame, text="列数:").pack(padx=10, pady=2, anchor=tk.W)
        self.cols_input = ttk.Spinbox(self.multi_panel_frame, from_=1, to=10, width=5)
        self.cols_input.delete(0, tk.END)
        self.cols_input.insert(0, "2")
        self.cols_input.pack(padx=10, pady=2, fill=tk.X)
        
        # 默认隐藏多面板设置
        self.multi_panel_frame.pack_forget()
    
    def _init_buttons(self):
        """初始化按钮"""
        # 绘制按钮
        self.draw_button = ttk.Button(self.control_panel, text="绘制图表", command=self.draw_chart)
        self.draw_button.pack(padx=10, pady=10, fill=tk.X)
        
        # 保存按钮
        self.save_button = ttk.Button(self.control_panel, text="保存图表", command=self.save_chart)
        self.save_button.pack(padx=10, pady=5, fill=tk.X)
    
    def _on_chart_type_change(self, event):
        """图表类型变化事件处理"""
        chart_type = self.chart_type.get()
        if chart_type == "多面板图":
            self.multi_panel_frame.pack(padx=10, pady=5, fill=tk.X)
        else:
            self.multi_panel_frame.pack_forget()
    
    def import_data(self):
        """导入数据"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV文件", "*.csv"), ("Excel文件", "*.xlsx"), ("文本文件", "*.txt")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path, delimiter='\t')
                
                # 转换为文本格式
                data_text = ""
                for index, row in df.iterrows():
                    data_text += f"{index},{','.join(map(str, row.values))}\n"
                
                # 更新数据输入框
                self.data_input.delete(1.0, tk.END)
                self.data_input.insert(tk.END, data_text)
            except Exception as e:
                print(f"导入数据失败: {e}")
    
    def parse_data(self):
        """解析数据"""
        data_text = self.data_input.get(1.0, tk.END)
        lines = data_text.strip().split('\n')
        
        if not lines:
            return None
        
        # 检查是否为多列数据
        first_line = lines[0].strip().split(',')
        if len(first_line) > 2:
            # 多列数据
            data = {}
            headers = first_line[1:]
            for header in headers:
                data[header] = []
            
            for line in lines[1:]:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) > 1:
                        for i, header in enumerate(headers):
                            if i + 1 < len(parts):
                                data[header].append(float(parts[i + 1]))
            return data
        else:
            # 单列数据
            data = {}
            for line in lines:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        data[parts[0]] = float(parts[1])
            return data
    
    def draw_chart(self):
        """绘制图表"""
        # 清除旧图表
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
        
        # 获取数据
        data = self.parse_data()
        if not data:
            print("数据为空")
            return
        
        # 创建图表
        chart_type = self.chart_type.get()
        interactive = self.interactive_var.get()
        
        if chart_type == "柱状图":
            self.chart = BarChart()
            self.chart.plot(data)
        elif chart_type == "折线图":
            self.chart = LineChart()
            self.chart.plot(data)
        elif chart_type == "散点图":
            self.chart = ScatterChart()
            if isinstance(data, dict) and len(data) > 1:
                # 多列数据
                x = list(data.values())[0]
                y = list(data.values())[1]
            else:
                # 单列数据
                x = list(data.keys())
                y = list(data.values())
            self.chart.plot(x, y)
        elif chart_type == "直方图":
            self.chart = Histogram()
            if isinstance(data, dict):
                self.chart.plot(list(data.values()))
            else:
                self.chart.plot(list(data.values())[0])
        elif chart_type == "箱线图":
            self.chart = BoxPlot()
            if isinstance(data, dict) and len(data) > 1:
                self.chart.plot(list(data.values()))
            else:
                self.chart.plot([list(data.values())])
        elif chart_type == "饼图":
            self.chart = PieChart()
            self.chart.plot(list(data.values()), labels=list(data.keys()))
        elif chart_type == "热力图":
            self.chart = Heatmap()
            # 生成随机热力图数据
            heat_data = np.random.rand(10, 10)
            self.chart.plot(heat_data, interactive=interactive)
        elif chart_type == "网络图":
            self.chart = NetworkPlot()
            # 创建随机网络
            import networkx as nx
            G = nx.random_geometric_graph(20, 0.3)
            self.chart.plot(G, interactive=interactive)
        elif chart_type == "桑基图":
            self.chart = SankeyDiagram()
            # 创建示例数据
            sankey_data = pd.DataFrame({
                'source': [0, 1, 1, 2, 3, 3],
                'target': [2, 2, 3, 4, 4, 5],
                'value': [10, 15, 20, 25, 30, 35]
            })
            self.chart.plot(sankey_data, 'source', 'target', 'value', interactive=interactive)
        elif chart_type == "词云图":
            self.chart = WordcloudChart()
            # 创建示例文本
            text = "Python Java C++ JavaScript Ruby PHP C# Go Rust Swift Kotlin TypeScript"
            self.chart.plot(text, interactive=interactive)
        elif chart_type == "多面板图":
            self.chart = MultiPanel()
            # 生成多面板数据
            data_list = [
                {"A": 1, "B": 2, "C": 3},  # 柱状图数据
                [1, 2, 3, 4, 5],  # 折线图数据
                {"X": 4, "Y": 5, "Z": 6},  # 柱状图数据
                [5, 4, 3, 2, 1]   # 折线图数据
            ]
            rows = int(self.rows_input.get())
            cols = int(self.cols_input.get())
            self.chart.plot(data_list, rows, cols, interactive=interactive)
        
        # 设置标题和标签
        self.chart.set_title(self.title_input.get())
        self.chart.set_xlabel(self.xlabel_input.get())
        self.chart.set_ylabel(self.ylabel_input.get())
        
        # 显示图表
        if hasattr(self.chart, 'fig'):
            fig = self.chart.fig
            self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        elif hasattr(self.chart, 'get_figure'):
            fig = self.chart.get_figure()
            self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def save_chart(self):
        """保存图表"""
        if self.chart:
            # 保存为 PNG
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG文件", "*.png"), ("SVG文件", "*.svg"), ("PDF文件", "*.pdf")])
            if file_path:
                self.chart.save(file_path)
                print(f"图表已保存为 {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChartEditor(root)
    root.mainloop()