import logging
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLabel,
    QDialogButtonBox,
    QWidget
)

from src.utils.i18n import I18nManager
from src.utils.config import ConfigManager


class SettingsDialog(QDialog):
    """
    Settings dialog view.
    """
    
    def __init__(
        self, 
        i18n: I18nManager,
        config: ConfigManager, 
        parent: QWidget | None = None
    ):
        """
        Initialize the dialog.
        
        :param i18n: Internationalization manager (for UI translation).
        :param config: Configuration manager (to read current settings).
        :param parent: Parent widget (usually MainWindow).
        """
        super().__init__(parent)
        self._i18n = i18n
        self._config = config
        
        # UI references
        self.language_combo = None
        
        self._init_ui()
        logging.info("SettingsDialog (View) initialized.")

    def _init_ui(self):
        """Build UI components."""
        
        t = self._i18n.t
        
        self.setWindowTitle(t("settings_dialog.title"))
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(15)

        # --- Field 1: Language ---
        language_label = QLabel(t("settings_dialog.language.label"))
        self.language_combo = QComboBox()
        self.language_combo.setToolTip(t("settings_dialog.language.tip"))
        
        # Add available languages (text is display name, data is language code)
        self.language_combo.addItem("Português (Brasil)", "pt_BR")
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Español", "es")
        self.language_combo.addItem("Français", "fr")
        self.language_combo.addItem("Русский", "ru")
        self.language_combo.addItem("中文 (Mandarim)", "zh")
        
        # Read current language from config and select it
        current_lang = self._config.get("language", "pt_BR")
        index = self.language_combo.findData(current_lang)
        if index != -1:
            self.language_combo.setCurrentIndex(index)
        
        form_layout.addRow(language_label, self.language_combo)
        
        layout.addLayout(form_layout)

        # --- Buttons (OK, Cancel) ---
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # Translate default buttons
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText(
            t("settings_dialog.button_ok")
        )
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(
            t("settings_dialog.button_cancel")
        )
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)

    # --- Public Methods (Called by Controller) ---

    def get_selected_language(self) -> str:
        """Return the selected language code (e.g. "pt_BR")."""
        if self.language_combo:
            return self.language_combo.currentData()
        return "pt_BR"