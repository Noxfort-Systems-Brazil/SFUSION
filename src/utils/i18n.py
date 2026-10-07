import json
import os
import logging
from typing import Any

class I18nManager:
    """
    Manages loading and accessing translation .json files.
    """
    
    def __init__(self, locale_dir="locale", language="pt_BR"):
        self.locale_dir = locale_dir
        self.language = language
        self._translations = {}
        self.load_locale(language)

    def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '.') -> dict:
        """
        Flattens a nested dictionary.
        Ex: { "a": { "b": "c" } } -> { "a.b": "c" }
        """
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    def load_locale(self, language):
        """Loads and flattens the language (locale) file."""
        file_path = os.path.join(self.locale_dir, f"{language}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Load the nested JSON
                nested_data = json.load(f) 
                # Convert to flat format
                self._translations = self._flatten_dict(nested_data) 
                
            logging.info(f"Translations loaded from: {file_path}")
        except FileNotFoundError as e:
            try:
                from src.utils.i18n import backend_i18n
                error_msg = backend_i18n.t("errors.i18n.load_failed", lang=language, error="File not found")
            except Exception:
                error_msg = f"Translation file not found: {file_path}"
            logging.error(error_msg)
            self._translations = {}
        except json.JSONDecodeError as e:
            try:
                from src.utils.i18n import backend_i18n
                error_msg = backend_i18n.t("errors.i18n.load_failed", lang=language, error=str(e))
            except Exception:
                error_msg = f"Error decoding JSON: {file_path}"
            logging.error(error_msg)
            self._translations = {}

    def t(self, key: str, **kwargs) -> str:
        """
        Gets the translation for a flat key (e.g., "main_window.title").
        """
        try:
            value = self._translations[key]
            
            if kwargs:
                value = value.format(**kwargs)
            return value
        except KeyError:
            logging.warning(f"Translation key not found: '{key}'")
            return key
        except Exception as e:
            logging.error(f"Error formatting key '{key}': {e}")
            return key

# Global instance for backend translations.
backend_i18n = I18nManager(locale_dir="locale_backend", language="pt_BR")