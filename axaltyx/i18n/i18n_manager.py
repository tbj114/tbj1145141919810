#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
多语言管理器 - 单例模式
"""

import json
import os


class I18nManager:
    """多语言管理器"""
    
    def __init__(self):
        """初始化多语言管理器"""
        self._lang = "zh_CN"
        self._cache = {}
        self._load_translations()
    
    def _load_translations(self):
        """加载翻译文件"""
        i18n_dir = os.path.dirname(os.path.abspath(__file__))
        for lang in ["zh_CN", "en_US"]:
            lang_dir = os.path.join(i18n_dir, lang)
            if os.path.exists(lang_dir):
                self._cache[lang] = {}
                for json_file in os.listdir(lang_dir):
                    if json_file.endswith(".json"):
                        file_path = os.path.join(lang_dir, json_file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            # 从文件名提取命名空间（去掉 .json 后缀）
                            namespace = json_file[:-5]
                            # 保持嵌套结构
                            self._cache[lang][namespace] = data
    
    def set_language(self, lang: str) -> None:
        """设置语言"""
        if lang in self._cache:
            self._lang = lang
    
    def t(self, key: str, **kwargs) -> str:
        """翻译函数"""
        # 解析 key，支持嵌套结构
        keys = key.split(".")
        value = self._cache.get(self._lang, {})
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return key  # 如果找不到，返回原始 key
        
        # 处理占位符
        if isinstance(value, str) and kwargs:
            return value.format(**kwargs)
        
        return value
    
    def get_language(self) -> str:
        """获取当前语言"""
        return self._lang
