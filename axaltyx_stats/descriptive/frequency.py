import pandas as pd
import numpy as np

class FrequencyAnalysis:
    def __init__(self, data):
        self.data = data
    
    def frequency_table(self, column):
        """生成频数表"""
        freq = self.data[column].value_counts().sort_index()
        percent = (freq / len(self.data)) * 100
        cumulative_freq = freq.cumsum()
        cumulative_percent = (cumulative_freq / len(self.data)) * 100
        
        table = pd.DataFrame({
            'Frequency': freq,
            'Percentage': percent,
            'Cumulative Frequency': cumulative_freq,
            'Cumulative Percentage': cumulative_percent
        })
        
        return table
    
    def group_frequency(self, column, bins, labels=None):
        """生成分组频数表"""
        grouped = pd.cut(self.data[column], bins=bins, labels=labels, include_lowest=True)
        freq = grouped.value_counts().sort_index()
        percent = (freq / len(self.data)) * 100
        cumulative_freq = freq.cumsum()
        cumulative_percent = (cumulative_freq / len(self.data)) * 100
        
        table = pd.DataFrame({
            'Frequency': freq,
            'Percentage': percent,
            'Cumulative Frequency': cumulative_freq,
            'Cumulative Percentage': cumulative_percent
        })
        
        return table
