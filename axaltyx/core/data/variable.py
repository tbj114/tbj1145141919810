#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
变量定义类
"""


class Variable:
    """变量类"""
    
    # 变量类型
    TYPE_NUMERIC = "numeric"
    TYPE_STRING = "string"
    TYPE_DATE = "date"
    
    # 对齐方式
    ALIGN_LEFT = "left"
    ALIGN_RIGHT = "right"
    ALIGN_CENTER = "center"
    
    # 度量尺度
    MEASURE_SCALE = "scale"  # 度量
    MEASURE_ORDINAL = "ordinal"  # 有序
    MEASURE_NOMINAL = "nominal"  # 名义
    
    # 角色
    ROLE_INPUT = "input"
    ROLE_TARGET = "target"
    ROLE_BOTH = "both"
    
    def __init__(self, name="", var_type=TYPE_NUMERIC):
        """初始化变量
        
        Args:
            name: 变量名
            var_type: 变量类型
        """
        self.name = name
        self.type = var_type
        self.width = 8  # 默认宽度
        self.decimals = 2  # 默认小数位
        self.label = ""  # 变量标签
        self.value_labels = {}  # 值标签 {值: 标签}
        self.missing_values = []  # 缺失值
        self.column_width = 100  # 列宽（像素）
        self.align = self.ALIGN_RIGHT if var_type == self.TYPE_NUMERIC else self.ALIGN_LEFT
        self.measure = self.MEASURE_SCALE if var_type == self.TYPE_NUMERIC else self.MEASURE_NOMINAL
        self.role = self.ROLE_INPUT
    
    def to_dict(self):
        """将变量属性转换为字典"""
        return {
            "name": self.name,
            "type": self.type,
            "width": self.width,
            "decimals": self.decimals,
            "label": self.label,
            "value_labels": self.value_labels,
            "missing_values": self.missing_values,
            "column_width": self.column_width,
            "align": self.align,
            "measure": self.measure,
            "role": self.role
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建变量"""
        var = cls()
        var.name = data.get("name", "")
        var.type = data.get("type", cls.TYPE_NUMERIC)
        var.width = data.get("width", 8)
        var.decimals = data.get("decimals", 2)
        var.label = data.get("label", "")
        var.value_labels = data.get("value_labels", {})
        var.missing_values = data.get("missing_values", [])
        var.column_width = data.get("column_width", 100)
        var.align = data.get("align", var.ALIGN_RIGHT if var.type == var.TYPE_NUMERIC else var.ALIGN_LEFT)
        var.measure = data.get("measure", var.MEASURE_SCALE if var.type == var.TYPE_NUMERIC else var.MEASURE_NOMINAL)
        var.role = data.get("role", var.ROLE_INPUT)
        return var
