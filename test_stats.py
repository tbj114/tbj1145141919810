import pandas as pd
import numpy as np
from axaltyx_stats.data.data_manager import DataManager
from axaltyx_stats.data.missing_values import MissingValuesHandler
from axaltyx_stats.descriptive.basic_stats import BasicStats
from axaltyx_stats.descriptive.frequency import FrequencyAnalysis
from axaltyx_stats.descriptive.crosstab import CrosstabAnalysis

# 测试数据管理模块
def test_data_manager():
    print("Testing DataManager...")
    dm = DataManager()
    
    # 创建100x100的空数据框
    df = dm.create_dataframe(rows=100, cols=100)
    print(f"Created dataframe with shape: {df.shape}")
    
    # 测试设置和获取值
    dm.set_value(0, 0, 10)
    value = dm.get_value(0, 0)
    print(f"Set value at (0,0) to 10, got: {value}")
    
    # 测试重命名列
    dm.rename_column('Var1', 'NewVar1')
    columns = dm.get_columns()
    print(f"First column name after rename: {columns[0]}")
    
    # 测试添加列
    dm.add_column('NewColumn', [1]*100)
    print(f"Dataframe shape after adding column: {dm.get_shape()}")
    
    print("DataManager test completed successfully!\n")

# 测试缺失值处理模块
def test_missing_values():
    print("Testing MissingValuesHandler...")
    # 创建包含缺失值的测试数据
    data = pd.DataFrame({
        'A': [1, 2, np.nan, 4, 5],
        'B': [6, np.nan, 8, 9, 10],
        'C': ['a', 'b', 'c', np.nan, 'e']
    })
    
    mvh = MissingValuesHandler(data)
    
    # 检测缺失值
    missing = mvh.detect_missing()
    print("Missing values:")
    print(missing)
    
    # 获取缺失值汇总
    summary = mvh.get_missing_summary()
    print("\nMissing values summary:")
    print(summary)
    
    # 测试填充缺失值
    filled_data = mvh.fill_missing(method='mean')
    print("\nData after filling missing values with mean:")
    print(filled_data)
    
    print("MissingValuesHandler test completed successfully!\n")

# 测试描述性统计模块
def test_basic_stats():
    print("Testing BasicStats...")
    # 创建测试数据
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [6, 7, 8, 9, 10],
        'C': [11, 12, 13, 14, 15]
    })
    
    bs = BasicStats(data)
    
    # 测试基本统计量
    print("Mean:")
    print(bs.mean())
    
    print("\nMedian:")
    print(bs.median())
    
    print("\nStandard Deviation:")
    print(bs.std())
    
    print("\nDescribe:")
    print(bs.describe())
    
    print("BasicStats test completed successfully!\n")

# 测试频数分析模块
def test_frequency_analysis():
    print("Testing FrequencyAnalysis...")
    # 创建测试数据
    data = pd.DataFrame({
        'Category': ['A', 'B', 'A', 'C', 'B', 'A', 'D', 'C', 'B', 'A'],
        'Value': [10, 20, 15, 25, 30, 35, 40, 45, 50, 55]
    })
    
    fa = FrequencyAnalysis(data)
    
    # 测试频数表
    freq_table = fa.frequency_table('Category')
    print("Frequency table for Category:")
    print(freq_table)
    
    # 测试分组频数表
    group_freq = fa.group_frequency('Value', bins=3, labels=['Low', 'Medium', 'High'])
    print("\nGroup frequency table for Value:")
    print(group_freq)
    
    print("FrequencyAnalysis test completed successfully!\n")

# 测试交叉表与卡方检验模块
def test_crosstab_analysis():
    print("Testing CrosstabAnalysis...")
    # 创建测试数据
    data = pd.DataFrame({
        'Gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
        'Preference': ['A', 'B', 'A', 'A', 'B', 'B', 'A', 'B']
    })
    
    ca = CrosstabAnalysis(data)
    
    # 测试交叉表
    cross_table = ca.crosstab('Gender', 'Preference')
    print("Crosstab:")
    print(cross_table)
    
    # 测试卡方检验
    chi2_result = ca.chi_square_test('Gender', 'Preference')
    print("\nChi-square test result:")
    print(f"Chi-square Statistic: {chi2_result['Chi-square Statistic']}")
    print(f"P-value: {chi2_result['P-value']}")
    print(f"Degrees of Freedom: {chi2_result['Degrees of Freedom']}")
    
    print("CrosstabAnalysis test completed successfully!\n")

if __name__ == "__main__":
    test_data_manager()
    test_missing_values()
    test_basic_stats()
    test_frequency_analysis()
    test_crosstab_analysis()
    print("All tests completed successfully!")
