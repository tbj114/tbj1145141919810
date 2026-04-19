#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
描述性统计功能测试
"""

import unittest
import numpy as np
from axaltyx.core.descriptive.descriptives import DescriptiveStats, HistogramGenerator


class TestDescriptiveStats(unittest.TestCase):
    """描述性统计测试"""
    
    def setUp(self):
        """设置测试数据"""
        np.random.seed(42)
        self.test_data = np.random.normal(50, 10, size=100).tolist()
    
    def test_calculate_mean(self):
        """测试均值计算"""
        mean = DescriptiveStats.calculate_mean(self.test_data)
        self.assertIsNotNone(mean)
        self.assertAlmostEqual(mean, np.mean(self.test_data), places=2)
    
    def test_calculate_std_dev(self):
        """测试标准差计算"""
        std_dev = DescriptiveStats.calculate_std_dev(self.test_data)
        self.assertIsNotNone(std_dev)
        self.assertAlmostEqual(std_dev, np.std(self.test_data, ddof=1), places=2)
    
    def test_calculate_variance(self):
        """测试方差计算"""
        variance = DescriptiveStats.calculate_variance(self.test_data)
        self.assertIsNotNone(variance)
        self.assertAlmostEqual(variance, np.var(self.test_data, ddof=1), places=2)
    
    def test_calculate_range(self):
        """测试全距计算"""
        range_val = DescriptiveStats.calculate_range(self.test_data)
        self.assertIsNotNone(range_val)
        self.assertAlmostEqual(range_val, np.max(self.test_data) - np.min(self.test_data), places=2)
    
    def test_calculate_min_max(self):
        """测试最小值和最大值计算"""
        min_val = DescriptiveStats.calculate_min(self.test_data)
        max_val = DescriptiveStats.calculate_max(self.test_data)
        self.assertIsNotNone(min_val)
        self.assertIsNotNone(max_val)
        self.assertAlmostEqual(min_val, np.min(self.test_data), places=2)
        self.assertAlmostEqual(max_val, np.max(self.test_data), places=2)
    
    def test_calculate_statistics(self):
        """测试统计量计算"""
        stats = DescriptiveStats.calculate_statistics(self.test_data)
        self.assertIn('mean', stats)
        self.assertIn('std_dev', stats)
        self.assertIn('variance', stats)
        self.assertIn('range', stats)
        self.assertIn('min', stats)
        self.assertIn('max', stats)
        self.assertIn('kurtosis', stats)
        self.assertIn('skewness', stats)
        self.assertIn('standard_error', stats)
        self.assertIn('count', stats)
        self.assertIn('valid_count', stats)
    
    def test_partial_statistics(self):
        """测试部分统计量计算"""
        options = {'mean': True, 'std_dev': True}
        stats = DescriptiveStats.calculate_statistics(self.test_data, options)
        self.assertEqual(len(stats), 4)  # 加上 count 和 valid_count
    
    def test_create_result_table(self):
        """测试结果表格创建"""
        stats = DescriptiveStats.calculate_statistics(self.test_data)
        table = DescriptiveStats.create_result_table('TestVar', stats)
        self.assertEqual(table['variable'], 'TestVar')
        self.assertEqual(table['statistics'], stats)
    
    def test_histogram_generation(self):
        """测试直方图生成"""
        bin_edges, frequencies = HistogramGenerator.generate_histogram_data(self.test_data, bins=10)
        self.assertIsNotNone(bin_edges)
        self.assertIsNotNone(frequencies)
        self.assertEqual(len(bin_edges), 11)
        self.assertEqual(len(frequencies), 10)
    
    def test_histogram_table(self):
        """测试直方图表格创建"""
        bin_edges, frequencies = HistogramGenerator.generate_histogram_data(self.test_data, bins=5)
        histogram_data = HistogramGenerator.create_histogram_table('TestVar', bin_edges, frequencies)
        self.assertIsInstance(histogram_data, list)
        self.assertEqual(len(histogram_data), 5)
        for item in histogram_data:
            self.assertIn('bin_start', item)
            self.assertIn('bin_end', item)
            self.assertIn('frequency', item)


def main():
    """运行测试"""
    print("开始描述性统计功能测试...")
    print("=" * 50)
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDescriptiveStats)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    print(f"测试结果: {'✅ 通过' if result.wasSuccessful() else '❌ 失败'}")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")


if __name__ == "__main__":
    main()
