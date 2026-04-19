#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
单例模式实现
"""


class Singleton:
    """单例装饰器"""
    
    def __init__(self, cls):
        """初始化单例装饰器"""
        self.cls = cls
        self.instance = None
    
    def __call__(self, *args, **kwargs):
        """调用单例"""
        if not self.instance:
            self.instance = self.cls(*args, **kwargs)
        return self.instance
