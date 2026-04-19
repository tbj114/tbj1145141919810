#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理工具
"""

import json
import os
from .singleton import Singleton


class ConfigManager(metaclass=Singleton):
    """配置管理类 - 单例模式"""
    
    def __init__(self):
        """初始化配置"""
        self.config_file = os.path.join(os.path.expanduser("~"), ".axaltyx", "config.json")
        self._config = {}
        self._load()
    
    def _load(self):
        """加载配置文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
        except Exception as e:
            print(f"加载配置失败: {e}")
            self._config = {}
    
    def _save(self):
        """保存配置文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def get(self, key, default=None):
        """获取配置
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return self._config.get(key, default)
    
    def set(self, key, value):
        """设置配置
        
        Args:
            key: 配置键
            value: 配置值
        """
        self._config[key] = value
    
    def save(self):
        """保存配置到文件"""
        self._save()
    
    def clear(self):
        """清空配置"""
        self._config = {}
        self.save()
