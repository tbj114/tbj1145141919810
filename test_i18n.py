#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from axaltyx.i18n import I18nManager

mgr = I18nManager()
print(f"Current language: {mgr.get_language()}")

# Test Chinese
mgr.set_language("zh_CN")
print(f"Chinese translations:")
print(f"app.app_name: {mgr.t('app.app_name')}")
print(f"menu.file: {mgr.t('menu.file')}")

# Test English
mgr.set_language("en_US")
print(f"\nEnglish translations:")
print(f"app.app_name: {mgr.t('app.app_name')}")
print(f"menu.file: {mgr.t('menu.file')}")
