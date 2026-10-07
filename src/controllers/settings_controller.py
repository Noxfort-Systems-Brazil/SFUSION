import logging
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QDialog, QMessageBox

# UI and Utility dependencies
from ui.settings.settings_dialog import SettingsDialog
from ui.main_window import MainWindow
from src.utils.config import ConfigManager
from src.utils.i18n import I18nManager, backend_i18n


class SettingsController(QObject):
    """
    Controller for the Settings dialog.
    
    Responsibilities:
    - Open the SettingsDialog (View).
    - Listen to 'Save' (OK) from the View.
    - Update ConfigManager (Model/Util) with new configs.
    - Inform the user about the need to restart.
    """
    
    def __init__(
        self, 
        main_window: MainWindow, 
        config: ConfigManager, 
        i18n: I18nManager
    ):
        """
        Initializes the settings controller.
        
        :param main_window: The Main Window (to be parent of the dialog).
        :param config: The configuration manager (to read/save).
        :param i18n: The internationalization manager (to translate UI).
        """
        super().__init__()
        
        self._main_window = main_window
        self._config = config
        self._i18n = i18n
        
        logging.info(backend_i18n.t("controller.settings.init"))

    @Slot()
    def show_settings_dialog(self):
        """
        Public slot: Creates and displays the settings dialog.
        Called by MainController.
        """
        t = self._i18n.t
        
        # 1. Create the View (Dialog)
        dialog = SettingsDialog(self._i18n, self._config, self._main_window)
        
        # 2. Execute the dialog (modal)
        if dialog.exec() == QDialog.Accepted:
            # 3. User clicked "Save"
            self._on_save(dialog)
        else:
            # 4. User clicked "Cancel"
            logging.debug(backend_i18n.t("controller.settings.cancelled"))

    def _on_save(self, dialog: SettingsDialog):
        """Reads data from the View and saves the configuration."""
        t = self._i18n.t
        
        current_lang = self._config.get("language")
        new_lang = dialog.get_selected_language()
        
        lang_changed = (current_lang != new_lang)
        
        # --- Language Saving Logic ---
        if lang_changed:
            self._config.set("language", new_lang)
            logging.info(backend_i18n.t("controller.settings.lang_changed", lang=new_lang))

        # --- (Future: save other configs here) ---
        
        # 5. Save config.json to disk
        try:
            self._config.save_config()
            logging.info(backend_i18n.t("controller.settings.saved"))
        except Exception as e:
            logging.error(backend_i18n.t("controller.settings.save_failed", error=str(e)))
            self._view.show_error_message(
                t("dialog.error.title"),
                t("dialog.error.generic_save", error=str(e))
            )
            return

        # 6. If language changed, notify the user about restart
        if lang_changed:
            self._main_window.show_info_message(
                t("settings_dialog.restart_required.title"),
                t("settings_dialog.restart_required.body")
            )