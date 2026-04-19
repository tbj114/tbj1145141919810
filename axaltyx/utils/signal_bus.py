#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全局信号总线
"""


class SignalBus:
    """信号总线类"""
    
    def __init__(self):
        """初始化信号总线"""
        pass
    
    def emit(self, signal, *args, **kwargs):
        """发送信号"""
        pass
    
    def connect(self, signal, callback):
        """连接信号"""
        pass
