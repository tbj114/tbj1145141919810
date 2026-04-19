#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多语言管理器 - 单例模式
"""


class I18nManager:
    """多语言管理器"""
    
    def __init__(self):
        """初始化多语言管理器"""
        self._lang = "zh_CN"
        self._cache = {}
    
    def set_language(self, lang: str) -> None:
        """设置语言"""
        pass
    
    def t(self, key: str, **kwargs) -> str:
        """翻译函数"""
        pass
    
    def get_language(self) -> str:
        """获取当前语言"""
        pass
