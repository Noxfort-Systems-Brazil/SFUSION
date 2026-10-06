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

# File: ui/main_window.py
# Author: Gabriel Moraes
# Date: November 2025
# Description:
#    Main application window interface based on QMainWindow.

import logging
import os  # Necessário para manipular caminhos
from PySide6.QtCore import Qt, QSize, Signal, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QSplitter,
    QMessageBox
)

# Dependencies (other UI parts or utilities)
from ui.map.map_view import MapView
from ui.sources.sources_panel import SourcesPanel
from src.utils.i18n import I18nManager
from ui.editor.editor_panel import EditorPanel
# --- Resource import (Required for icon resolution in executable) ---
from src.utils.resources import resource_path 


class MainWindow(QMainWindow):
    """
    Main application view.
    Contains the toolbar, status bar, and layout
    organizing MapView and SourcesPanel.
    """
    
    # --- SIGNALS ---
    open_project_requested = Signal()
    save_project_requested = Signal()
    settings_requested = Signal()
    
    open_map_requested = Signal()
    add_source_requested = Signal()
    save_config_requested = Signal() # (For "Generate .db" button)

    def __init__(self, i18n: I18nManager, parent: QWidget | None = None):
        """
        Initialize the main window.
        """
        super().__init__(parent)
        self._i18n = i18n
        
        self.editor_panel = None
        self.map_view = None
        self.sources_panel = None
        
        self.action_save = None # (For "Generate .db")
        self.action_save_project = None # (For "Save Project")
        
        # Initialize UI
        self._init_ui()
        logging.info("MainWindow (View) initialized.")

    def _init_ui(self):
        """Build UI components (toolbar, layout)."""
        
        t = self._i18n.t
        
        self.setWindowTitle(t("main_window.window_title"))
        self.setGeometry(100, 100, 1200, 800)

        # --- WINDOW ICON DEFINITION ---
        try:
            # Use resource_path to locate file inside or outside executable
            icon_path = resource_path(os.path.join("assets", "icon", "logo.png"))
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            logging.error(f"Failed to load window icon: {e}")
        # ------------------------------

        # 1. Toolbar
        toolbar = QToolBar(t("main_window.toolbar_name"))
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) 
        self.addToolBar(toolbar)

        # --- Project Actions ---
        action_open_project = QAction(
            QIcon.fromTheme("document-open"),
            t("main_window.action_open_project"), 
            self
        )
        action_open_project.setStatusTip(t("main_window.action_open_project_tip"))
        action_open_project.triggered.connect(self.open_project_requested)
        toolbar.addAction(action_open_project)
        
        self.action_save_project = QAction(
            QIcon.fromTheme("document-save-as"),
            t("main_window.action_save_project"), 
            self
        )
        self.action_save_project.setStatusTip(t("main_window.action_save_project_tip"))
        self.action_save_project.triggered.connect(self.save_project_requested)
        self.action_save_project.setEnabled(False) 
        toolbar.addAction(self.action_save_project)

        toolbar.addSeparator()

        # --- Map and Source Actions ---
        action_open_map = QAction(
            QIcon.fromTheme("folder-open"),
            t("main_window.action_open_map"), 
            self
        )
        action_open_map.setStatusTip(t("main_window.action_open_map_tip"))
        action_open_map.triggered.connect(self.open_map_requested)
        toolbar.addAction(action_open_map)

        action_add_source = QAction(
            QIcon.fromTheme("folder-add"),
            t("main_window.action_add_source"), 
            self
        )
        action_add_source.setStatusTip(t("main_window.action_add_source_tip"))
        action_add_source.triggered.connect(self.add_source_requested)
        toolbar.addAction(action_add_source)

        toolbar.addSeparator()

        # --- "Generate .db" Action ---
        self.action_save = QAction(
            QIcon.fromTheme("document-save"),
            t("main_window.action_save_config"), # "Generate .db"
            self
        )
        self.action_save.setStatusTip(t("main_window.action_save_config_tip"))
        self.action_save.triggered.connect(self.save_config_requested)
        self.action_save.setEnabled(False) 
        toolbar.addAction(self.action_save)
        
        # --- Settings Action ---
        toolbar.addSeparator()
        action_settings = QAction(
            QIcon.fromTheme("preferences-system"),
            t("main_window.action_settings"), 
            self
        )
        action_settings.setStatusTip(t("main_window.action_settings_tip"))
        action_settings.triggered.connect(self.settings_requested)
        toolbar.addAction(action_settings)


        # 2. Status Bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage(t("main_window.status_ready"))

        # 3. Central Widget and Layout (Splitter)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

    # --- View Injection Methods ---

    def set_editor_panel(self, editor_panel: EditorPanel):
        self.editor_panel = editor_panel
        self.splitter.addWidget(self.editor_panel)

    def set_map_view(self, map_view: MapView):
        self.map_view = map_view
        self.splitter.addWidget(self.map_view)

    def set_sources_panel(self, sources_panel: SourcesPanel):
        self.sources_panel = sources_panel
        self.splitter.addWidget(self.sources_panel)
        
        self.splitter.setSizes([250, 700, 250])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 0)

    # --- Feedback Methods (Called by MainController) ---

    def show_status_message(self, message: str, timeout: int = 3000):
        self.statusBar().showMessage(message, timeout)

    def show_error_message(self, title: str, message: str):
        logging.error(f"Displaying error message to user: {title} - {message}")
        QMessageBox.critical(self, title, message)

    def show_info_message(self, title: str, message: str):
        QMessageBox.information(self, title, message)

    @Slot(bool)
    def set_savable_state(self, is_savable: bool):
        """
        Enable or disable 'Generate .db' and 'Save Project' actions.
        """
        if self.action_save:
            self.action_save.setEnabled(is_savable)
            
        if self.action_save_project:
            self.action_save_project.setEnabled(is_savable)

    def closeEvent(self, event):
        """
        Intercept window close and enforce aggressive termination on the OS process.
        Prevents C++/GPU threads (such as SLM) from lingering in zombie mode after exit.
        """
        logging.warning("MainWindow: Aggressive application termination requested (Hard Kill).")
        import os
        os._exit(0)