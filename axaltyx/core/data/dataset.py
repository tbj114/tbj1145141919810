#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据集类 - 加载、保存、操作数据
"""

from .variable import Variable


class Dataset:
    """数据集类"""
    
    def __init__(self, rows=100, cols=100):
        """初始化数据集
        
        Args:
            rows: 初始行数
            cols: 初始列数
        """
        self.rows = rows
        self.cols = cols
        self.variables = []  # 变量列表
        self.data = []  # 数据存储 [row][col]
        self.filename = ""
        self.modified = False
        
        # 初始化默认变量和数据
        self._initialize_defaults()
    
    def _initialize_defaults(self):
        """初始化默认变量和数据"""
        # 创建默认变量
        for i in range(self.cols):
            var_name = f"VAR{i+1:05d}"
            var = Variable(name=var_name)
            self.variables.append(var)
        
        # 初始化数据为 None（表示缺失值）
        self.data = [[None for _ in range(self.cols)] for _ in range(self.rows)]
    
    def get_value(self, row, col):
        """获取单元格值
        
        Args:
            row: 行索引
            col: 列索引
            
        Returns:
            单元格值
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        return None
    
    def set_value(self, row, col, value):
        """设置单元格值
        
        Args:
            row: 行索引
            col: 列索引
            value: 新值
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = value
            self.modified = True
    
    def get_variable(self, index):
        """获取变量
        
        Args:
            index: 变量索引
            
        Returns:
            Variable 对象
        """
        if 0 <= index < len(self.variables):
            return self.variables[index]
        return None
    
    def add_variable(self, variable=None):
        """添加变量
        
        Args:
            variable: Variable 对象，如果为 None 则创建默认变量
            
        Returns:
            新变量的索引
        """
        if variable is None:
            var_name = f"VAR{len(self.variables)+1:05d}"
            variable = Variable(name=var_name)
        
        self.variables.append(variable)
        self.cols += 1
        
        # 为新变量添加数据列
        for row in self.data:
            row.append(None)
        
        self.modified = True
        return len(self.variables) - 1
    
    def remove_variable(self, index):
        """删除变量
        
        Args:
            index: 变量索引
        """
        if 0 <= index < len(self.variables):
            self.variables.pop(index)
            self.cols -= 1
            
            # 删除对应的数据列
            for row in self.data:
                row.pop(index)
            
            self.modified = True
    
    def add_row(self, values=None):
        """添加行
        
        Args:
            values: 行数据，如果为 None 则全为 None
        """
        if values is None:
            values = [None for _ in range(self.cols)]
        else:
            # 确保长度匹配
            values = values[:self.cols] + [None] * max(0, self.cols - len(values))
        
        self.data.append(values)
        self.rows += 1
        self.modified = True
        return self.rows - 1
    
    def remove_row(self, index):
        """删除行
        
        Args:
            index: 行索引
        """
        if 0 <= index < self.rows:
            self.data.pop(index)
            self.rows -= 1
            self.modified = True
    
    def to_dict(self):
        """将数据集转换为字典"""
        return {
            "rows": self.rows,
            "cols": self.cols,
            "variables": [var.to_dict() for var in self.variables],
            "data": self.data,
            "filename": self.filename
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建数据集"""
        rows = data.get("rows", 100)
        cols = data.get("cols", 100)
        dataset = cls(rows=rows, cols=cols)
        
        # 清空默认数据
        dataset.variables = []
        dataset.data = []
        
        # 加载变量
        variables_data = data.get("variables", [])
        for var_data in variables_data:
            var = Variable.from_dict(var_data)
            dataset.variables.append(var)
        
        # 加载数据
        dataset.data = data.get("data", [])
        dataset.rows = len(dataset.data)
        dataset.cols = len(dataset.variables)
        dataset.filename = data.get("filename", "")
        dataset.modified = False
        
        return dataset
    
    def is_empty(self):
        """检查数据集是否为空"""
        return all(all(cell is None for cell in row) for row in self.data)
