#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QApplication 初始化
"""

from PyQt6.QtWidgets import QApplication


class AxaltyXApp(QApplication):
    """AxaltyX 应用类"""
    
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("AxaltyX")
        self.setApplicationVersion("1.0.0")


def create_app(argv):
    """创建应用实例
    
    Args:
        argv: 命令行参数
        
    Returns:
        AxaltyXApp: 应用实例
    """
    return AxaltyXApp(argv)
