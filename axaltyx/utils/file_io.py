#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件读写模块 - 支持 .axl 文件格式
"""

import json
import gzip
import os
from axaltyx.core.data.dataset import Dataset
from axaltyx.utils.config import ConfigManager


class FileIO:
    """文件读写类"""
    
    @staticmethod
    def save_dataset(dataset, filepath):
        """保存数据集到 .axl 文件
        
        Args:
            dataset: Dataset 对象
            filepath: 文件路径
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 转换数据集为字典
            data = dataset.to_dict()
            
            # 写入压缩的 JSON 文件
            with gzip.open(filepath, 'wt', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 更新数据集的文件名和修改状态
            dataset.filename = filepath
            dataset.modified = False
            
            # 添加到最近文件列表
            FileIO.add_recent_file(filepath)
            
            return True
        except Exception as e:
            print(f"保存文件失败: {e}")
            return False
    
    @staticmethod
    def load_dataset(filepath):
        """从 .axl 文件加载数据集
        
        Args:
            filepath: 文件路径
            
        Returns:
            Dataset: 加载的数据集对象，失败返回 None
        """
        try:
            # 读取压缩的 JSON 文件
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                data = json.load(f)
            
            # 从字典创建数据集
            dataset = Dataset.from_dict(data)
            dataset.filename = filepath
            
            # 添加到最近文件列表
            FileIO.add_recent_file(filepath)
            
            return dataset
        except Exception as e:
            print(f"加载文件失败: {e}")
            return None
    
    @staticmethod
    def create_new_dataset():
        """创建新的空数据集
        
        Returns:
            Dataset: 新的数据集对象
        """
        return Dataset(rows=100, cols=100)
    
    @staticmethod
    def add_recent_file(filepath):
        """添加文件到最近文件列表
        
        Args:
            filepath: 文件路径
        """
        config = ConfigManager()
        recent_files = config.get("recent_files", [])
        
        # 移除已存在的相同文件
        recent_files = [f for f in recent_files if f != filepath]
        
        # 添加到列表开头
        recent_files.insert(0, filepath)
        
        # 限制最近文件数量为 10
        recent_files = recent_files[:10]
        
        # 保存回配置
        config.set("recent_files", recent_files)
        config.save()
    
    @staticmethod
    def get_recent_files():
        """获取最近文件列表
        
        Returns:
            list: 最近文件路径列表
        """
        config = ConfigManager()
        return config.get("recent_files", [])
    
    @staticmethod
    def clear_recent_files():
        """清空最近文件列表"""
        config = ConfigManager()
        config.set("recent_files", [])
        config.save()
