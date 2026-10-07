import json
import logging
import os
from typing import Any
from src.utils.i18n import backend_i18n

class ConfigManager:
    """
    Manages loading and accessing configuration from a JSON file.
    """
    def __init__(self, config_path: str):
        """
        Initializes the manager with the path to the settings file.
        
        Args:
            config_path (str): The absolute path to the settings.json file.
        """
        self.config_path = config_path
        self._config_data = {}
        logging.info(backend_i18n.t("config.init", path=self.config_path))

    def load_config(self):
        """
        Loads the configuration file from disk into memory.
        """
        if not os.path.exists(self.config_path):
            logging.warning(backend_i18n.t("config.load.not_found", path=self.config_path))
            self._config_data = {}
            return

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
            logging.info(backend_i18n.t("config.load.success", path=self.config_path))
        except json.JSONDecodeError as e:
            logging.critical(backend_i18n.t("config.load.parse_error", path=self.config_path, e=str(e)))
            self._config_data = {}
        except Exception as e:
            logging.critical(backend_i18n.t("config.load.read_error", path=self.config_path, e=str(e)))
            self._config_data = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Gets a configuration value by key.
        
        Args:
            key (str): The configuration key (e.g., "default_language").
            default (Any, optional): Value to return if key is not found.
        
        Returns:
            Any: The configuration value or the default.
        """
        return self._config_data.get(key, default)

    def set(self, key: str, value: Any):
        """
        Sets a configuration value in memory.
        Note: This does not automatically save to disk.
        """
        self._config_data[key] = value

    def save_config(self):
        """
        Saves the current in-memory configuration back to the .json file.
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=4)
            logging.info(backend_i18n.t("config.save.success", path=self.config_path))
        except Exception as e:
            logging.critical(backend_i18n.t("config.save.error", path=self.config_path, e=str(e)))