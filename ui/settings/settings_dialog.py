# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Gabriel Moraes - Noxfort Systems
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# File: ui/settings/settings_dialog.py
# Author: Gabriel Moraes
# Date: November 2025
# Description:
#    Modal dialog for application settings and configuration (e.g. Language).

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
    View (Janela de Diálogo) para as Configurações.
    """
    
    def __init__(
        self, 
        i18n: I18nManager,
        config: ConfigManager, 
        parent: QWidget | None = None
    ):
        """
        Inicializa o diálogo.
        
        :param i18n: O gestor de internacionalização (para traduzir a UI).
        :param config: O gestor de configuração (para ler o estado atual).
        :param parent: O widget "Pai" (normalmente a MainWindow).
        """
        super().__init__(parent)
        self._i18n = i18n
        self._config = config
        
        # Referências da UI
        self.language_combo = None
        
        self._init_ui()
        logging.info("SettingsDialog (View) inicializado.")

    def _init_ui(self):
        """Constrói os componentes da UI."""
        
        t = self._i18n.t
        
        self.setWindowTitle(t("settings_dialog.title"))
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(15)

        # --- Campo 1: Idioma ---
        language_label = QLabel(t("settings_dialog.language.label"))
        self.language_combo = QComboBox()
        self.language_combo.setToolTip(t("settings_dialog.language.tip"))
        
        # --- 1. CORREÇÃO (Adicionar novos idiomas) ---
        # Adiciona os idiomas (o texto é o nome, o "Data" é o código)
        self.language_combo.addItem("Português (Brasil)", "pt_BR")
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Español", "es")
        self.language_combo.addItem("Français", "fr")
        self.language_combo.addItem("Русский", "ru")
        self.language_combo.addItem("中文 (Mandarim)", "zh")
        # --- FIM DA CORREÇÃO ---
        
        # Lê o idioma atual do config.json e define-o
        current_lang = self._config.get("language", "pt_BR")
        index = self.language_combo.findData(current_lang)
        if index != -1:
            self.language_combo.setCurrentIndex(index)
        
        form_layout.addRow(language_label, self.language_combo)
        
        layout.addLayout(form_layout)

        # --- Botões (OK, Cancelar) ---
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # (Traduz os botões padrão)
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText(
            t("settings_dialog.button_ok")
        )
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(
            t("settings_dialog.button_cancel")
        )
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)

    # --- Métodos Públicos (Chamados pelo Controller) ---

    def get_selected_language(self) -> str:
        """Retorna o código do idioma selecionado (ex: "pt_BR")."""
        if self.language_combo:
            return self.language_combo.currentData()
        return "pt_BR"