#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
变量选择器单元测试
"""

from axaltyx.gui.widgets.variable_list import VariableList
from axaltyx.gui.widgets.transfer_button import TransferButton
from axaltyx.gui.widgets.variable_selector import VariableSelector


def test_variable_list():
    """测试变量列表"""
    print("测试变量列表...")
    
    # 创建变量列表
    var_list = VariableList()
    
    # 测试添加变量
    var_list.add_variable("VAR00001", "numeric")
    var_list.add_variable("VAR00002", "string")
    
    # 测试获取所有变量
    all_vars = var_list.get_all_variables()
    assert len(all_vars) == 2
    assert all_vars[0] == ("VAR00001", "numeric")
    assert all_vars[1] == ("VAR00002", "string")
    print("✓ 变量列表添加和获取测试通过")
    
    # 测试清空
    var_list.clear_all()
    assert len(var_list.get_all_variables()) == 0
    print("✓ 变量列表清空测试通过")


def test_variable_selector():
    """测试变量选择器"""
    print("\n测试变量选择器...")
    
    # 创建变量选择器
    selector = VariableSelector()
    
    # 测试数据
    test_vars = [
        ("VAR00001", "numeric"),
        ("VAR00002", "string"),
        ("VAR00003", "numeric"),
    ]
    
    # 设置变量
    selector.set_variables(test_vars)
    
    # 测试获取可用变量
    available_vars = selector.available_list.get_all_variables()
    assert len(available_vars) == 3
    print("✓ 变量选择器设置测试通过")
    
    # 测试移动所有到右侧
    selector._move_all_right()
    available_count = len(selector.available_list.get_all_variables())
    selected_count = len(selector.selected_list.get_all_variables())
    assert available_count == 0
    assert selected_count == 3
    print("✓ 移动所有到右侧测试通过")
    
    # 测试移动所有到左侧
    selector._move_all_left()
    available_count = len(selector.available_list.get_all_variables())
    selected_count = len(selector.selected_list.get_all_variables())
    assert available_count == 3
    assert selected_count == 0
    print("✓ 移动所有到左侧测试通过")
    
    # 测试移动选中到右侧
    # 模拟选择第一个变量
    item = selector.available_list.item(0)
    selector.available_list.setCurrentItem(item)
    selector._move_selected_right()
    available_count = len(selector.available_list.get_all_variables())
    selected_count = len(selector.selected_list.get_all_variables())
    assert available_count == 2
    assert selected_count == 1
    print("✓ 移动选中到右侧测试通过")
    
    # 测试获取选中变量
    selected_vars = selector.get_selected_variables()
    assert len(selected_vars) == 1
    assert selected_vars[0][0] == "VAR00001"
    print("✓ 获取选中变量测试通过")


def test_transfer_button():
    """测试移动按钮"""
    print("\n测试移动按钮...")
    
    # 创建移动按钮
    buttons = TransferButton()
    
    # 测试信号连接
    # 这里我们只是验证按钮可以创建，信号可以连接
    # 实际的信号触发测试需要 GUI 环境
    print("✓ 移动按钮创建测试通过")


if __name__ == "__main__":
    print("开始变量选择器单元测试...\n")
    test_variable_list()
    test_transfer_button()
    test_variable_selector()
    print("\n✅ 所有单元测试通过！")
