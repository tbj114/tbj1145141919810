#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Windows 打包脚本
"""

import os
import shutil
import subprocess


def build_exe():
    """构建可执行文件"""
    print("Building executable...")
    cmd = [
        "pyinstaller",
        "--name=AxaltyX",
        "--onefile",
        "--windowed",
        "--icon=../axaltyx/resources/icons/app_icon.ico",
        "--add-data=../axaltyx/i18n;axaltyx/i18n",
        "--add-data=../axaltyx/resources;axaltyx/resources",
        "../axaltyx/main.py"
    ]
    subprocess.run(cmd, cwd=os.path.dirname(__file__))


def build_installer():
    """构建安装包"""
    print("Building installer...")
    cmd = [
        "iscc",
        "AxaltyX.iss"
    ]
    subprocess.run(cmd, cwd=os.path.dirname(__file__))


if __name__ == "__main__":
    build_exe()
    build_installer()
