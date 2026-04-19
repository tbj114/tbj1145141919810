#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
单例模式实现
"""


class Singleton(type):
    """单例元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """调用单例"""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
