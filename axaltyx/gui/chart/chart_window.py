#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表窗口
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from axaltyx.charting import ChartBase, BarChart, LineChart, ScatterChart, Histogram, BoxPlot, PieChart


class ChartWindow:
    """图表窗口"""
    
    def __init__(self, root):
        """初始化图表窗口
        
        Args:
            root: 根窗口
        """
        self.root = root
        self.root.title("图表编辑器")
        self.root.geometry("1000x800")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧控制面板
        self.control_panel = ttk.LabelFrame(self.main_frame, text="控制面板")
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
        
        # 初始化按钮
        self._init_buttons()
        
        # 初始化图表
        self.chart = None
        self.canvas = None
        
    def _init_chart_type(self):
        """初始化图表类型选择"""
        ttk.Label(self.control_panel, text="图表类型:").pack(padx=10, pady=5, anchor=tk.W)
        
        self.chart_type = tk.StringVar()
        chart_types = ["柱状图", "折线图", "散点图", "直方图", "箱线图", "饼图"]
        self.chart_type_combo = ttk.Combobox(self.control_panel, textvariable=self.chart_type, values=chart_types)
        self.chart_type_combo.current(0)
        self.chart_type_combo.pack(padx=10, pady=5, fill=tk.X)
    
    def _init_data_input(self):
        """初始化数据输入"""
        ttk.Label(self.control_panel, text="数据输入:").pack(padx=10, pady=5, anchor=tk.W)
        
        self.data_input = tk.Text(self.control_panel, height=10, width=30)
        self.data_input.pack(padx=10, pady=5, fill=tk.X)
        
        # 默认数据
        default_data = "类别A,30\n类别B,25\n类别C,20\n类别D,15\n类别E,10"
        self.data_input.insert(tk.END, default_data)
    
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
    
    def _init_buttons(self):
        """初始化按钮"""
        # 绘制按钮
        self.draw_button = ttk.Button(self.control_panel, text="绘制图表", command=self.draw_chart)
        self.draw_button.pack(padx=10, pady=10, fill=tk.X)
        
        # 保存按钮
        self.save_button = ttk.Button(self.control_panel, text="保存图表", command=self.save_chart)
        self.save_button.pack(padx=10, pady=5, fill=tk.X)
        
        # 交互式按钮
        self.interactive_var = tk.BooleanVar()
        self.interactive_check = ttk.Checkbutton(self.control_panel, text="启用交互", variable=self.interactive_var)
        self.interactive_check.pack(padx=10, pady=5, anchor=tk.W)
    
    def parse_data(self):
        """解析数据"""
        data_text = self.data_input.get(1.0, tk.END)
        lines = data_text.strip().split('\n')
        
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
        
        # 创建图表
        chart_type = self.chart_type.get()
        if chart_type == "柱状图":
            self.chart = BarChart()
            self.chart.plot(data)
        elif chart_type == "折线图":
            self.chart = LineChart()
            self.chart.plot(data)
        elif chart_type == "散点图":
            self.chart = ScatterChart()
            x = list(data.keys())
            y = list(data.values())
            self.chart.plot(x, y)
        elif chart_type == "直方图":
            self.chart = Histogram()
            self.chart.plot(list(data.values()))
        elif chart_type == "箱线图":
            self.chart = BoxPlot()
            self.chart.plot([list(data.values())])
        elif chart_type == "饼图":
            self.chart = PieChart()
            self.chart.plot(list(data.values()), labels=list(data.keys()))
        
        # 设置标题和标签
        self.chart.set_title(self.title_input.get())
        self.chart.set_xlabel(self.xlabel_input.get())
        self.chart.set_ylabel(self.ylabel_input.get())
        
        # 显示图表
        fig = self.chart.get_figure()
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def save_chart(self):
        """保存图表"""
        if self.chart:
            # 保存为 PNG
            self.chart.save("chart_output.png")
            print("图表已保存为 chart_output.png")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChartWindow(root)
    root.mainloop()