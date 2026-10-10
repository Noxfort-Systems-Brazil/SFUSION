import os
import glob
import logging
from src.utils.i18n import backend_i18n
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox

from ui.main_window import MainWindow
from src.services.map_importer import MapImporter
from src.services.data_importer import DataImporter
from src.services.persistence import PersistenceService
from src.services.project_service import ProjectService
from src.services.etl_service import ETLService 
from src.services.parquet_service import ParquetService
from src.utils.i18n import I18nManager


class MainController(QObject):
    """
    Main controller. Manages toolbar actions (View)
    and orchestrates Services (Services).
    """

    def __init__(
        self,
        main_window: MainWindow,
        map_importer: MapImporter,
        data_importer: DataImporter,
        persistence_service: PersistenceService,
        project_service: ProjectService,
        etl_service: ETLService, 
        parquet_service: ParquetService,
        i18n: I18nManager
    ):
        super().__init__()
        
        self._view = main_window
        self._map_importer = map_importer
        self._data_importer = data_importer
        self._persistence = persistence_service
        self._project = project_service
        self._etl = etl_service
        self._parquet = parquet_service
        self._i18n = i18n

        self._current_path = os.path.expanduser("~")
        
        # State variables for the pipeline
        self._temp_db_path = None
        self._target_parquet_path = None

    def _cleanup_temp_files(self, db_path: str = None):
        """
        Removes temporary SQLite database and all associated WAL/SHM/Journal files.
        """
        target = db_path or self._temp_db_path
        if not target:
            return

        for suffix in ["", "-wal", "-shm", "-journal"]:
            fpath = f"{target}{suffix}"
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                    logging.info(backend_i18n.t("main.temp_db_deleted", file=fpath))
                except OSError as e:
                    logging.warning(backend_i18n.t("main.temp_db_delete_failed", error=str(e)))

    def setup_connections(self):
        """Connects signals from View to Controller methods."""
        self._view.open_project_requested.connect(self._on_open_project)
        self._view.save_project_requested.connect(self._on_save_project)
        self._view.open_map_requested.connect(self._on_import_map)
        self._view.add_source_requested.connect(self._on_add_source)
        
        # The Trigger Button
        self._view.save_config_requested.connect(self._on_save_config)

        # --- PIPELINE CHAIN ---
        # 1. Persistence Finished -> Start ETL
        self._persistence.configuration_saved.connect(self._on_persistence_finished)
        self._persistence.configuration_error.connect(self._on_pipeline_error)

        # 2. ETL Finished -> Start Parquet
        self._etl.ingestion_finished.connect(self._on_ingestion_finished)
        self._etl.ingestion_error.connect(self._on_pipeline_error)
        
        # 3. Parquet Finished -> Delete Temp DB
        self._parquet.export_finished.connect(self._on_export_finished)
        self._parquet.export_error.connect(self._on_pipeline_error)

    # --- Private Slots (Listen to View) ---

    @Slot()
    def _on_open_project(self):
        t = self._i18n.t
        file_path, _ = QFileDialog.getOpenFileName(
            self._view, t("dialog.open_project.title"), self._current_path, t("dialog.open_project.filter")
        )
        if file_path:
            self._current_path = os.path.dirname(file_path)
            try:
                self._project.load_project(file_path)
                self._view.show_status_message(t("main_window.status_project_loaded", name=os.path.basename(file_path)))
            except Exception as e:
                self._view.show_error_message(t("dialog.error.title"), t("dialog.error.generic_load", error=str(e)))

    @Slot()
    def _on_save_project(self):
        t = self._i18n.t
        file_path, _ = QFileDialog.getSaveFileName(
            self._view, t("dialog.save_project.title"), self._current_path, t("dialog.save_project.filter")
        )
        if file_path:
            self._current_path = os.path.dirname(file_path)
            try:
                self._project.save_project(file_path)
                self._view.show_status_message(t("main_window.status_project_saved", name=os.path.basename(file_path)))
            except Exception as e:
                self._view.show_error_message(t("dialog.error.title"), t("dialog.error.generic_save", error=str(e)))

    @Slot()
    def _on_import_map(self):
        t = self._i18n.t
        file_path, _ = QFileDialog.getOpenFileName(
            self._view, t("dialog.open_map.title"), self._current_path, t("dialog.open_map.filter")
        )
        if file_path:
            self._current_path = os.path.dirname(file_path)
            
            try:
                self._map_importer.load_map(file_path)
                self._view.show_status_message(t("main_window.status_map_loaded", name=os.path.basename(file_path)))
            except Exception as e:
                self._view.show_error_message(t("dialog.error.title"), t("dialog.error.generic_load", error=str(e)))

    @Slot()
    def _on_add_source(self):
        """Asks for a folder, loads, and classifies the data source."""
        t = self._i18n.t
        folder_path = QFileDialog.getExistingDirectory(
            self._view,
            t("dialog.add_source.title"),
            self._current_path
        )
        
        if folder_path:
            self._current_path = folder_path
            source_name = os.path.basename(folder_path)
            
            try:
                self._data_importer.add_data_source(folder_path, "LOCAL")
                self._view.show_status_message(t("main_window.status_source_added", name=source_name))
            except Exception as e:
                self._view.show_error_message(t("dialog.error.title"), t("dialog.error.generic_load", error=str(e)))

    @Slot()
    def _on_save_config(self):
        """Trigger button in UI: Starts the 3-step automated pipeline."""
        t = self._i18n.t
        
        file_path, _ = QFileDialog.getSaveFileName(
            self._view,
            t("dialog.save_config.title"),
            self._current_path,
            t("dialog.save_config.filter")
        )
        
        if file_path:
            if not file_path.endswith(".parquet"):
                file_path += ".parquet"

            self._current_path = os.path.dirname(file_path)
            self._target_parquet_path = file_path
            
            # Create a hidden temp DB name based on the target filename
            base_name = os.path.basename(file_path)
            self._temp_db_path = os.path.join(self._current_path, f".temp_sfusion_{base_name}.db")

            logging.info(backend_i18n.t("main.pipeline_init", target=self._target_parquet_path, staging=self._temp_db_path))

            try:
                # Lock UI to prevent multiple clicks
                self._view.set_savable_state(False)
                if self._view.sources_panel:
                    self._view.sources_panel.set_savable_state(False)

                # Clean any leftover temp DB files from a previous interrupted run
                self._cleanup_temp_files(self._temp_db_path)

                self._view.show_status_message(backend_i18n.t("main.status_processing"))

                # Step 1: Save Schema to TEMP DB (Asynchronous: triggers _on_persistence_finished)
                self._persistence.save_configuration(self._temp_db_path)
                
            except Exception as e:
                self._on_pipeline_error(str(e))

    @Slot(str)
    def _on_persistence_finished(self, db_path: str):
        """Automated Step 2: Trigger ETL Ingestion after schema is committed."""
        logging.info("MainController: Schema staging complete, starting ETL ingestion.")
        try:
            self._etl.start_ingestion(db_path)
        except Exception as e:
            self._on_pipeline_error(str(e))

    @Slot(str)
    def _on_ingestion_finished(self, db_path: str):
        """Automated Step 3: Trigger Parquet Export to the user's path."""
        logging.info(backend_i18n.t("main.staging_complete"))
        self._view.show_status_message(backend_i18n.t("main.status_exporting"))
        
        try:
            self._parquet.export_db_to_parquet(db_path, self._target_parquet_path)
        except Exception as e:
            self._on_pipeline_error(str(e))

    @Slot(str)
    def _on_pipeline_error(self, error: str):
        """Centralized error recovery: unlocks UI, cleans temp files and displays message."""
        logging.error(f"MainController: Pipeline execution failed: {error}")
        self._view.set_savable_state(True)
        if self._view.sources_panel:
            self._view.sources_panel.set_savable_state(True)
        self._cleanup_temp_files(self._temp_db_path)
        self._view.show_error_message(self._i18n.t("dialog.error.title"), str(error))

    @Slot()
    def _on_export_finished(self):
        """Automated Step 4: Complete Cleanup."""
        logging.info(backend_i18n.t("main.export_complete"))
        
        # Remove all temp files (.db, -wal, -shm, -journal)
        self._cleanup_temp_files(self._temp_db_path)

        final_name = os.path.basename(self._target_parquet_path) if self._target_parquet_path else "File"
        self._view.show_status_message(backend_i18n.t("main.status_success", name=final_name))
        
        # Unlock UI when finished
        self._view.set_savable_state(True)
        if self._view.sources_panel:
            self._view.sources_panel.set_savable_state(True)
        
        QMessageBox.information(self._view, backend_i18n.t("main.success_title"), backend_i18n.t("main.success_body", path=self._target_parquet_path))