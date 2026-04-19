#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贝叶斯分析
"""

import numpy as np


class BayesianAnalysis:
    """贝叶斯分析类"""

    @staticmethod
    def bayesian_update(prior, likelihood, evidence):
        """
        贝叶斯更新

        Args:
            prior: 先验概率
            likelihood: 似然度
            evidence: 证据

        Returns:
            float: 后验概率
        """
        return (prior * likelihood) / evidence

    @staticmethod
    def beta_binomial_model(data, alpha_prior=1, beta_prior=1):
        """
        贝塔-二项分布模型

        Args:
            data: 二项分布数据，格式为 (n_trials, n_successes)
            alpha_prior: 贝塔先验的 alpha 参数
            beta_prior: 贝塔先验的 beta 参数

        Returns:
            dict: 包含后验分布参数的字典
        """
        n_trials, n_successes = data
        
        # 计算后验参数
        alpha_post = alpha_prior + n_successes
        beta_post = beta_prior + (n_trials - n_successes)
        
        # 计算后验均值和方差
        mean_post = alpha_post / (alpha_post + beta_post)
        var_post = (alpha_post * beta_post) / ((alpha_post + beta_post) ** 2 * (alpha_post + beta_post + 1))
        
        return {
            'model': 'beta_binomial',
            'prior_params': {'alpha': alpha_prior, 'beta': beta_prior},
            'posterior_params': {'alpha': alpha_post, 'beta': beta_post},
            'posterior_mean': mean_post,
            'posterior_variance': var_post,
            'n_trials': n_trials,
            'n_successes': n_successes
        }

    @staticmethod
    def normal_normal_model(data, mu_prior=0, sigma_prior=1, sigma_likelihood=1):
        """
        正态-正态模型

        Args:
            data: 正态分布数据
            mu_prior: 先验均值
            sigma_prior: 先验标准差
            sigma_likelihood: 似然标准差

        Returns:
            dict: 包含后验分布参数的字典
        """
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        
        n = len(data)
        data_mean = np.mean(data)
        
        # 计算后验参数
        sigma_post_sq = 1 / (1 / (sigma_prior ** 2) + n / (sigma_likelihood ** 2))
        mu_post = sigma_post_sq * (mu_prior / (sigma_prior ** 2) + n * data_mean / (sigma_likelihood ** 2))
        
        return {
            'model': 'normal_normal',
            'prior_params': {'mu': mu_prior, 'sigma': sigma_prior},
            'likelihood_params': {'sigma': sigma_likelihood},
            'posterior_params': {'mu': mu_post, 'sigma': np.sqrt(sigma_post_sq)},
            'data_mean': data_mean,
            'n_samples': n
        }

    @staticmethod
    def markov_chain_monte_carlo(data, model, n_iter=1000, burn_in=200):
        """
        马尔可夫链蒙特卡洛 (MCMC) 方法

        Args:
            data: 观测数据
            model: 模型函数，接受参数返回对数似然
            n_iter: 迭代次数
            burn_in:  burn-in 期

        Returns:
            dict: 包含 MCMC 结果的字典
        """
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        
        # 简单的 Metropolis-Hastings 算法
        current_param = np.random.normal(0, 1)
        samples = []
        
        for i in range(n_iter):
            # 提议新参数
            proposed_param = current_param + np.random.normal(0, 0.1)
            
            # 计算接受概率
            log_likelihood_current = model(data, current_param)
            log_likelihood_proposed = model(data, proposed_param)
            
            acceptance_ratio = np.exp(log_likelihood_proposed - log_likelihood_current)
            acceptance_prob = min(1, acceptance_ratio)
            
            # 接受或拒绝
            if np.random.uniform(0, 1) < acceptance_prob:
                current_param = proposed_param
            
            if i >= burn_in:
                samples.append(current_param)
        
        samples = np.array(samples)
        
        return {
            'model': 'MCMC',
            'n_iter': n_iter,
            'burn_in': burn_in,
            'samples': samples,
            'mean': np.mean(samples),
            'std': np.std(samples),
            'percentiles': {
                '2.5': np.percentile(samples, 2.5),
                '50': np.percentile(samples, 50),
                '97.5': np.percentile(samples, 97.5)
            }
        }
