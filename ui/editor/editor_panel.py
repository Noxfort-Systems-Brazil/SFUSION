# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Noxfort Systems
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

# File: ui/editor/editor_panel.py
# Author: Gabriel Moraes
# Date: November 2025
# Description:
#    Editor panel for Node/Edge metadata editing.

import logging
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    # 1. Import QListWidget and QListWidgetItem
    QListWidget,
    QListWidgetItem
)

from src.utils.i18n import I18nManager
from src.domain.entities import DataSource


class EditorPanel(QWidget):
    """
    Left-side panel view (Editor).
    Allows the user to view ID, edit "Real Name",
    and associate multiple local data sources (Checkboxes).
    """
    
    # Signals for InfoController
    save_clicked = Signal(str)
    close_clicked = Signal()
    
    # 2. Signal 'association_changed' REMOVED
    # (Logic is now read only when clicking "Save")

    def __init__(self, i18n: I18nManager, parent: QWidget | None = None):
        super().__init__(parent)
        
        self._i18n = i18n
        self._current_element_id = None
        
        # 3. Flag '_updating_ui' REMOVED
        
        self._init_ui()
        self.hide()
        logging.info("EditorPanel (View) initialized.")

    def _init_ui(self):
        """Build UI components."""
        t = self._i18n.t
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        group_box = QGroupBox(t("info_panel.title"))
        main_layout.addWidget(group_box)
        
        content_layout = QVBoxLayout(group_box)

        # --- Form (ID and Name only) ---
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Field 1: SUMO ID
        self.sumo_id_label = QLabel(t("info_panel.sumo_id"))
        self.sumo_id_value = QLineEdit()
        self.sumo_id_value.setReadOnly(True)
        # (Enhanced ID styling)
        self.sumo_id_value.setStyleSheet("""
            QLineEdit {
                background-color: #EEEEEE;
                color: #2c3e50;
                font-weight: bold;
                font-size: 13px;
                padding: 3px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
            }
        """)
        form_layout.addRow(self.sumo_id_label, self.sumo_id_value)

        # Field 2: Real Name
        self.real_name_label = QLabel(t("info_panel.real_name"))
        self.real_name_input = QLineEdit()
        self.real_name_input.setPlaceholderText(t("info_panel.real_name_placeholder"))
        form_layout.addRow(self.real_name_label, self.real_name_input)
        
        content_layout.addLayout(form_layout)

        # --- 4. REPLACEMENT (ComboBox to CheckBox list) ---
        
        # Label for list
        self.source_label = QLabel(t("info_panel.data_source"))
        content_layout.addWidget(self.source_label)
        
        # The List
        self.source_list_widget = QListWidget()
        self.source_list_widget.setToolTip(t("info_panel.data_source_tip"))
        self.source_list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
            }
        """)
        # Set minimum height for list
        self.source_list_widget.setMinimumHeight(100)
        
        # Add list to layout
        content_layout.addWidget(self.source_list_widget)
        # --- END OF REPLACEMENT ---
        

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        button_layout.addSpacerItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        self.close_button = QPushButton(t("info_panel.button_close"))
        self.close_button.clicked.connect(self.close_clicked)
        button_layout.addWidget(self.close_button)

        self.save_button = QPushButton(t("info_panel.button_save"))
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(self._on_save_clicked)
        button_layout.addWidget(self.save_button)
        
        content_layout.addLayout(button_layout)
        
        self.setMinimumWidth(250)

    # --- Internal Slots ---

    def _on_save_clicked(self):
        """Emit real name. (The Controller will read the checkboxes)."""
        new_name = self.real_name_input.text()
        self.save_clicked.emit(new_name)

    # 5. Slot '_on_combo_changed' REMOVED

    # --- Public Methods (Called by Controller) ---

    # 6. Method 'update_sources_list' MODIFIED
    @Slot(list, set)
    def update_sources_list(self, 
                            available_sources: list[DataSource], 
                            associated_source_ids: set[str]):
        """
        Populate QListWidget with checkboxes for available sources.
        """
        self.source_list_widget.clear()
        
        if not available_sources:
            # (Optional: Add "No local source available" item)
            return

        for source in available_sources:
            item = QListWidgetItem(source.name)
            item.setData(Qt.UserRole, source.path) # Store ID
            
            # Make item checkable as a checkbox
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            
            # Check the checkbox if ID is in associated set
            if source.path in associated_source_ids:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
                
            self.source_list_widget.addItem(item)

    # 7. Method 'set_current_source' REMOVED (logic is now in update_sources_list)

    # 8. NEW METHOD (for Controller to read data)
    def get_selected_source_ids(self) -> list[str]:
        """
        Read checkbox list and return IDs of checked items.
        """
        selected_ids = []
        for i in range(self.source_list_widget.count()):
            item = self.source_list_widget.item(i)
            if item.checkState() == Qt.Checked:
                selected_ids.append(item.data(Qt.UserRole))
        return selected_ids

    # 9. Method signature of 'show_data' MODIFIED (no longer needs 'source_id')
    @Slot(str, str, str)
    def show_data(self, title: str, sumo_id: str, real_name: str | None):
        """Update text fields with element data."""
        
        group_box = self.findChild(QGroupBox)
        if group_box:
            group_box.setTitle(title)
        
        self.sumo_id_value.setText(sumo_id)
        
        if real_name:
            self.real_name_input.setText(real_name)
        else:
            self.real_name_input.clear()
            
        self.real_name_input.setFocus()
        self.real_name_input.selectAll()