#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widgets 包
包含各种自定义控件组件
"""

from axaltyx.gui.widgets.output_tree import OutputTree, OutputTreeItem
from axaltyx.gui.widgets.output_viewer import OutputViewer
from axaltyx.gui.widgets.transfer_button import TransferButton
from axaltyx.gui.widgets.variable_list import VariableList
from axaltyx.gui.widgets.variable_selector import VariableSelector
from axaltyx.gui.widgets.variable_table import VariableTable

__all__ = [
    "OutputTree",
    "OutputTreeItem",
    "OutputViewer",
    "TransferButton",
    "VariableList",
    "VariableSelector",
    "VariableTable",
]
