import pandas as pd
import numpy as np

class MissingValuesHandler:
    def __init__(self, data):
        self.data = data
    
    def detect_missing(self):
        """检测缺失值"""
        return self.data.isnull()
    
    def get_missing_summary(self):
        """获取缺失值汇总"""
        missing_count = self.data.isnull().sum()
        missing_percentage = (missing_count / len(self.data)) * 100
        summary = pd.DataFrame({
            'Missing Count': missing_count,
            'Missing Percentage': missing_percentage
        })
        return summary[summary['Missing Count'] > 0]
    
    def drop_missing(self, axis=0, thresh=None):
        """删除包含缺失值的行或列"""
        return self.data.dropna(axis=axis, thresh=thresh)
    
    def fill_missing(self, method='mean', value=None, columns=None):
        """填充缺失值"""
        data_copy = self.data.copy()
        
        if columns is None:
            columns = data_copy.columns
        
        for col in columns:
            if data_copy[col].dtype in ['float64', 'int64']:
                if method == 'mean':
                    fill_value = data_copy[col].mean()
                elif method == 'median':
                    fill_value = data_copy[col].median()
                elif method == 'mode':
                    fill_value = data_copy[col].mode().iloc[0]
                elif method == 'constant':
                    fill_value = value
                else:
                    raise ValueError(f"Unsupported method: {method}")
                data_copy[col] = data_copy[col].fillna(fill_value)
            else:
                if method in ['mean', 'median']:
                    # 对于非数值列，自动使用mode方法
                    fill_value = data_copy[col].mode().iloc[0]
                elif method == 'mode':
                    fill_value = data_copy[col].mode().iloc[0]
                elif method == 'constant':
                    fill_value = value
                else:
                    raise ValueError(f"Unsupported method for non-numeric column: {method}")
                data_copy[col] = data_copy[col].fillna(fill_value)
        
        return data_copy
    
    def interpolate_missing(self, method='linear', columns=None):
        """插值填充缺失值"""
        data_copy = self.data.copy()
        
        if columns is None:
            columns = data_copy.columns
        
        for col in columns:
            if data_copy[col].dtype in ['float64', 'int64']:
                data_copy[col] = data_copy[col].interpolate(method=method)
        
        return data_copy
    
    def forward_fill(self, columns=None):
        """前向填充"""
        data_copy = self.data.copy()
        
        if columns is None:
            columns = data_copy.columns
        
        for col in columns:
            data_copy[col] = data_copy[col].fillna(method='ffill')
        
        return data_copy
    
    def backward_fill(self, columns=None):
        """后向填充"""
        data_copy = self.data.copy()
        
        if columns is None:
            columns = data_copy.columns
        
        for col in columns:
            data_copy[col] = data_copy[col].fillna(method='bfill')
        
        return data_copy
