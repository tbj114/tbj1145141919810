import json
import os
from pathlib import Path


class LocaleManager:
    _instance = None
    _translations = {}
    _current_locale = 'zh_CN'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_locales()
        return cls._instance

    def _load_locales(self):
        locale_dir = Path(__file__).parent.parent / 'locale'
        for file in locale_dir.glob('*.json'):
            lang = file.stem
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    self._translations[lang] = json.load(f)
            except Exception:
                pass
        if 'zh_CN' in self._translations:
            self._current_locale = 'zh_CN'
        elif self._translations:
            self._current_locale = list(self._translations.keys())[0]

    def set_locale(self, locale_code):
        if locale_code in self._translations:
            self._current_locale = locale_code

    def get(self, key, default=None):
        keys = key.split('.')
        value = self._translations.get(self._current_locale, {})
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                value = default
                break
        return value if value is not None else key

    def get_available_locales(self):
        return list(self._translations.keys())


def tr(key):
    return LocaleManager().get(key)
