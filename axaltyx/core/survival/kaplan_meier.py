#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kaplan-Meier 生存分析
"""

import numpy as np


class KaplanMeier:
    """Kaplan-Meier 生存分析类"""

    @staticmethod
    def _filter_data(time, event):
        """过滤无效数据"""
        if not isinstance(time, np.ndarray):
            time = np.array(time)
        if not isinstance(event, np.ndarray):
            event = np.array(event)
        
        if time.ndim != 1 or event.ndim != 1:
            raise ValueError("时间和事件数据必须是一维数组")
        if len(time) != len(event):
            raise ValueError("时间和事件数据长度必须一致")
        
        # 过滤含有 NaN 的数据
        mask = ~np.isnan(time) & ~np.isnan(event)
        time_filtered = time[mask]
        event_filtered = event[mask]
        
        return time_filtered, event_filtered

    @staticmethod
    def fit(time, event):
        """
        执行 Kaplan-Meier 生存分析

        Args:
            time: 生存时间或随访时间
            event: 事件指示变量（1 表示事件发生，0 表示截尾）

        Returns:
            dict: 包含生存分析结果的字典
        """
        # 过滤数据
        time, event = KaplanMeier._filter_data(time, event)
        n_samples = len(time)
        
        if n_samples == 0:
            raise ValueError("没有有效的数据")
        
        # 按时间排序
        sorted_indices = np.argsort(time)
        time = time[sorted_indices]
        event = event[sorted_indices]
        
        # 计算生存函数
        unique_times = np.unique(time)
        n_risk = []  # 风险集大小
        n_events = []  # 事件发生数
        survival_prob = []  # 生存概率
        
        current_risk = n_samples
        current_survival = 1.0
        
        for t in unique_times:
            # 计算在时间 t 的风险集大小
            risk_at_t = current_risk
            
            # 计算在时间 t 的事件发生数
            events_at_t = np.sum((time == t) & (event == 1))
            
            # 更新生存概率
            if risk_at_t > 0:
                survival = current_survival * (1 - events_at_t / risk_at_t)
            else:
                survival = current_survival
            
            n_risk.append(risk_at_t)
            n_events.append(events_at_t)
            survival_prob.append(survival)
            
            # 更新当前风险集大小（减去在时间 t 发生事件的个体）
            current_risk -= events_at_t
            current_survival = survival
        
        # 计算标准误差（Greenwood 公式）
        se = []
        cumulative_variance = 0
        for i in range(len(unique_times)):
            if n_risk[i] > 0 and n_risk[i] != n_events[i]:
                variance_increment = n_events[i] / (n_risk[i] * (n_risk[i] - n_events[i]))
                cumulative_variance += variance_increment
            se.append(survival_prob[i] * np.sqrt(cumulative_variance))
        
        return {
            'n_samples': n_samples,
            'unique_times': unique_times,
            'n_risk': n_risk,
            'n_events': n_events,
            'survival_prob': survival_prob,
            'standard_error': se,
            'median_survival_time': KaplanMeier._calculate_median_survival(unique_times, survival_prob)
        }

    @staticmethod
    def _calculate_median_survival(times, survival_prob):
        """计算中位生存时间"""
        for i, (t, prob) in enumerate(zip(times, survival_prob)):
            if prob <= 0.5:
                # 线性插值
                if i == 0:
                    return t
                else:
                    t_prev = times[i-1]
                    prob_prev = survival_prob[i-1]
                    slope = (t - t_prev) / (prob - prob_prev)
                    median = t_prev + slope * (0.5 - prob_prev)
                    return median
        return None  # 如果生存概率从未低于 0.5

    @staticmethod
    def log_rank_test(groups):
        """
        执行对数秩检验，比较多个生存曲线

        Args:
            groups: 字典，键为组名，值为 (time, event) 元组

        Returns:
            dict: 包含对数秩检验结果的字典
        """
        if len(groups) < 2:
            raise ValueError("至少需要两个组进行比较")
        
        # 收集所有时间点
        all_times = []
        group_data = {}
        
        for group_name, (time, event) in groups.items():
            time_filtered, event_filtered = KaplanMeier._filter_data(time, event)
            group_data[group_name] = {
                'time': time_filtered,
                'event': event_filtered,
                'n': len(time_filtered)
            }
            all_times.extend(time_filtered)
        
        # 按时间排序的唯一时间点
        unique_times = np.unique(all_times)
        
        # 计算每个时间点的期望事件数
        observed = {name: 0 for name in groups.keys()}
        expected = {name: 0 for name in groups.keys()}
        
        for t in unique_times:
            # 计算每个组在时间 t 的风险集大小
            n_risk = {}
            total_risk = 0
            total_events = 0
            
            for name, data in group_data.items():
                # 风险集：生存时间 >= t 的个体
                risk_set = data['time'] >= t
                n_risk[name] = np.sum(risk_set)
                total_risk += n_risk[name]
                
                # 计算在时间 t 的事件数
                events = np.sum((data['time'] == t) & (data['event'] == 1))
                observed[name] += events
                total_events += events
            
            # 计算期望事件数
            if total_risk > 0:
                for name in groups.keys():
                    expected[name] += (n_risk[name] / total_risk) * total_events
        
        # 计算卡方统计量
        chi_square = 0
        for name in groups.keys():
            if expected[name] > 0:
                chi_square += ((observed[name] - expected[name]) ** 2) / expected[name]
        
        # 计算自由度
        df = len(groups) - 1
        
        # 计算 p 值
        p_value = KaplanMeier._calculate_chi_square_p_value(chi_square, df)
        
        return {
            'chi_square': chi_square,
            'df': df,
            'p_value': p_value,
            'observed': observed,
            'expected': expected
        }

    @staticmethod
    def _calculate_chi_square_p_value(chi_square, df):
        """计算卡方分布的 p 值"""
        try:
            from scipy import stats
            p_value = 1 - stats.chi2.cdf(chi_square, df)
            return p_value
        except ImportError:
            return None
