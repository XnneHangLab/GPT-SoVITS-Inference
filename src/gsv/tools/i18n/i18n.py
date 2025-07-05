import os
import json
import locale
from pathlib import Path

def load_language_list(language, locale_paths):
    language_map = {}
    for locale_path in locale_paths:
        lang_file = os.path.join(locale_path, f"{language}.json")
        if os.path.exists(lang_file):
            with open(lang_file, 'r', encoding='utf-8') as f:
                language_map.update(json.load(f))
    return language_map

class I18nAuto:
    def __init__(self, language=None, locale_paths=[], locale_path=str(Path(__file__).parent.parent.parent.parent.parent / "i18n" / "locale")):
        if language in ["auto", None]:
            language = locale.getdefaultlocale()[0]
        if not any(os.path.exists(os.path.join(locale_path, f"{language}.json")) for locale_path in locale_paths):
            language = "zh_CN"
        self.language = language
        if len(locale_paths):
            self.language_map = load_language_list(language, locale_paths)
        else:
            self.language_map = load_language_list(language, [locale_path])

    def __call__(self, key):
        return self.language_map.get(key, key)

    def __repr__(self):
        return "Use Language: " + self.language
