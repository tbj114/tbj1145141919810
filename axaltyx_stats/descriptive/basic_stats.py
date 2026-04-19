import pandas as pd
import numpy as np

class BasicStats:
    def __init__(self, data):
        self.data = data
    
    def describe(self, columns=None):
        """获取描述性统计信息"""
        if columns is None:
            return self.data.describe()
        else:
            return self.data[columns].describe()
    
    def mean(self, columns=None):
        """计算均值"""
        if columns is None:
            return self.data.mean()
        else:
            return self.data[columns].mean()
    
    def median(self, columns=None):
        """计算中位数"""
        if columns is None:
            return self.data.median()
        else:
            return self.data[columns].median()
    
    def mode(self, columns=None):
        """计算众数"""
        if columns is None:
            return self.data.mode().iloc[0]
        else:
            return self.data[columns].mode().iloc[0]
    
    def std(self, columns=None):
        """计算标准差"""
        if columns is None:
            return self.data.std()
        else:
            return self.data[columns].std()
    
    def var(self, columns=None):
        """计算方差"""
        if columns is None:
            return self.data.var()
        else:
            return self.data[columns].var()
    
    def min(self, columns=None):
        """计算最小值"""
        if columns is None:
            return self.data.min()
        else:
            return self.data[columns].min()
    
    def max(self, columns=None):
        """计算最大值"""
        if columns is None:
            return self.data.max()
        else:
            return self.data[columns].max()
    
    def range(self, columns=None):
        """计算极差"""
        if columns is None:
            return self.data.max() - self.data.min()
        else:
            return self.data[columns].max() - self.data[columns].min()
    
    def q1(self, columns=None):
        """计算第一四分位数"""
        if columns is None:
            return self.data.quantile(0.25)
        else:
            return self.data[columns].quantile(0.25)
    
    def q3(self, columns=None):
        """计算第三四分位数"""
        if columns is None:
            return self.data.quantile(0.75)
        else:
            return self.data[columns].quantile(0.75)
    
    def iqr(self, columns=None):
        """计算四分位距"""
        if columns is None:
            return self.data.quantile(0.75) - self.data.quantile(0.25)
        else:
            return self.data[columns].quantile(0.75) - self.data[columns].quantile(0.25)
    
    def skewness(self, columns=None):
        """计算偏度"""
        if columns is None:
            return self.data.skew()
        else:
            return self.data[columns].skew()
    
    def kurtosis(self, columns=None):
        """计算峰度"""
        if columns is None:
            return self.data.kurtosis()
        else:
            return self.data[columns].kurtosis()
    
    def sum(self, columns=None):
        """计算总和"""
        if columns is None:
            return self.data.sum()
        else:
            return self.data[columns].sum()
    
    def count(self, columns=None):
        """计算非缺失值数量"""
        if columns is None:
            return self.data.count()
        else:
            return self.data[columns].count()
