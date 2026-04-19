import pandas as pd
import numpy as np
from scipy import stats

class CrosstabAnalysis:
    def __init__(self, data):
        self.data = data
    
    def crosstab(self, row_var, col_var, normalize=False):
        """生成交叉表"""
        if normalize:
            return pd.crosstab(self.data[row_var], self.data[col_var], normalize='all')
        else:
            return pd.crosstab(self.data[row_var], self.data[col_var])
    
    def chi_square_test(self, row_var, col_var):
        """执行卡方检验"""
        cross_table = pd.crosstab(self.data[row_var], self.data[col_var])
        chi2, p_value, dof, expected = stats.chi2_contingency(cross_table)
        
        result = {
            'Chi-square Statistic': chi2,
            'P-value': p_value,
            'Degrees of Freedom': dof,
            'Expected Frequencies': expected
        }
        
        return result
    
    def crosstab_with_statistics(self, row_var, col_var):
        """生成带统计信息的交叉表"""
        cross_table = pd.crosstab(self.data[row_var], self.data[col_var])
        chi2_result = self.chi_square_test(row_var, col_var)
        
        return {
            'Crosstab': cross_table,
            'Chi-square Test': chi2_result
        }
