import pandas as pd
import numpy as np

class DataManager:
    def __init__(self):
        self.data = pd.DataFrame()
    
    def create_dataframe(self, rows=100, cols=100):
        """创建一个指定大小的空数据框"""
        columns = [f'Var{i+1}' for i in range(cols)]
        self.data = pd.DataFrame(index=range(rows), columns=columns)
        return self.data
    
    def import_data(self, file_path, file_type=None):
        """导入数据文件"""
        if file_type is None:
            file_type = file_path.split('.')[-1].lower()
        
        if file_type == 'csv':
            self.data = pd.read_csv(file_path)
        elif file_type == 'xlsx' or file_type == 'xls':
            self.data = pd.read_excel(file_path)
        elif file_type == 'txt':
            self.data = pd.read_csv(file_path, sep='\t')
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return self.data
    
    def export_data(self, file_path, file_type=None):
        """导出数据文件"""
        if file_type is None:
            file_type = file_path.split('.')[-1].lower()
        
        if file_type == 'csv':
            self.data.to_csv(file_path, index=False)
        elif file_type == 'xlsx':
            self.data.to_excel(file_path, index=False)
        elif file_type == 'txt':
            self.data.to_csv(file_path, sep='\t', index=False)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def set_value(self, row, col, value):
        """设置单元格值"""
        if isinstance(col, int):
            col = self.data.columns[col]
        self.data.loc[row, col] = value
    
    def get_value(self, row, col):
        """获取单元格值"""
        if isinstance(col, int):
            col = self.data.columns[col]
        return self.data.loc[row, col]
    
    def rename_column(self, old_name, new_name):
        """重命名列"""
        self.data.rename(columns={old_name: new_name}, inplace=True)
    
    def add_column(self, column_name, values=None):
        """添加列"""
        if values is None:
            values = [None] * len(self.data)
        self.data[column_name] = values
    
    def remove_column(self, column_name):
        """删除列"""
        self.data.drop(column_name, axis=1, inplace=True)
    
    def add_row(self, values=None):
        """添加行"""
        if values is None:
            values = [None] * len(self.data.columns)
        new_row = pd.DataFrame([values], columns=self.data.columns)
        self.data = pd.concat([self.data, new_row], ignore_index=True)
    
    def remove_row(self, row_index):
        """删除行"""
        self.data.drop(row_index, axis=0, inplace=True)
        self.data.reset_index(drop=True, inplace=True)
    
    def get_shape(self):
        """获取数据形状"""
        return self.data.shape
    
    def get_columns(self):
        """获取列名"""
        return list(self.data.columns)
    
    def get_data(self):
        """获取数据"""
        return self.data
    
    def set_data(self, data):
        """设置数据"""
        self.data = data
