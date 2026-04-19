#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本分析
"""

import numpy as np
import re
from collections import Counter


class TextAnalysis:
    """文本分析类"""

    @staticmethod
    def tokenize(text):
        """
        文本分词

        Args:
            text: 输入文本

        Returns:
            list: 分词结果
        """
        # 简单的分词方法
        text = text.lower()
        # 使用正则表达式提取单词
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    @staticmethod
    def word_frequency(text):
        """
        词频统计

        Args:
            text: 输入文本

        Returns:
            dict: 词频统计结果
        """
        tokens = TextAnalysis.tokenize(text)
        frequency = Counter(tokens)
        return dict(frequency)

    @staticmethod
    def n_gram(text, n=2):
        """
        n-gram 分析

        Args:
            text: 输入文本
            n: n-gram 的 n 值

        Returns:
            dict: n-gram 统计结果
        """
        tokens = TextAnalysis.tokenize(text)
        n_grams = []
        for i in range(len(tokens) - n + 1):
            n_gram = ' '.join(tokens[i:i+n])
            n_grams.append(n_gram)
        frequency = Counter(n_grams)
        return dict(frequency)

    @staticmethod
    def sentiment_analysis(text):
        """
        简单的情感分析

        Args:
            text: 输入文本

        Returns:
            dict: 情感分析结果
        """
        # 简单的情感词典
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'happy', 'love', 'like'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'sad', 'hate', 'dislike', 'poor', 'worst', 'disappointed'}

        tokens = TextAnalysis.tokenize(text)
        positive_count = sum(1 for token in tokens if token in positive_words)
        negative_count = sum(1 for token in tokens if token in negative_words)

        # 计算情感分数
        total = positive_count + negative_count
        if total > 0:
            sentiment_score = (positive_count - negative_count) / total
        else:
            sentiment_score = 0

        # 情感分类
        if sentiment_score > 0.1:
            sentiment = 'positive'
        elif sentiment_score < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'total_count': total
        }

    @staticmethod
    def text_statistics(text):
        """
        文本统计

        Args:
            text: 输入文本

        Returns:
            dict: 文本统计结果
        """
        # 计算字符数
        char_count = len(text)
        
        # 计算单词数
        tokens = TextAnalysis.tokenize(text)
        word_count = len(tokens)
        
        # 计算句子数
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # 计算平均词长
        if word_count > 0:
            avg_word_length = sum(len(word) for word in tokens) / word_count
        else:
            avg_word_length = 0
        
        # 计算平均句子长度
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
        else:
            avg_sentence_length = 0
        
        # 计算词汇丰富度（不同单词数 / 总单词数）
        if word_count > 0:
            lexical_diversity = len(set(tokens)) / word_count
        else:
            lexical_diversity = 0
        
        return {
            'char_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
            'lexical_diversity': lexical_diversity
        }
