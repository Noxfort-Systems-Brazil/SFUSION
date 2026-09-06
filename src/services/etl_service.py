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

# File: src/services/etl_service.py
# Author: Gabriel Moraes
# Date: November 2025
# Description:
#    High-Performance ETL Orchestrator and Service.
#    Coordinates parallel sensor processing threads, schema discovery,
#    and batch persistence while managing Qt lifecycle signals.

import os
import sqlite3
import logging
import concurrent.futures
from threading import Lock
from typing import Optional, List, Dict
from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool

from src.etl.storage_repository import ETLStorageRepository
from src.etl.sensor_processor import SensorBatchProcessor
from src.services.neural_transformer import NeuralTransformer
from src.domain.app_state import AppState
from src.utils.i18n import backend_i18n

logger = logging.getLogger(__name__)


class ETLWorkerSignals(QObject):
    finished = Signal(str)
    progress = Signal(int)
    total_calculated = Signal(int)
    error = Signal(str)


class ETLWorker(QRunnable):
    """
    Orchestrator / Facade for ETL Ingestion.
    Follows SOLID architecture by delegating persistence to ETLStorageRepository
    and file transformations to SensorBatchProcessor.
    """

    BATCH_SIZE = 500

    def __init__(
        self,
        db_path: str,
        app_state: AppState,
        storage_repo: Optional[ETLStorageRepository] = None,
        processor: Optional[SensorBatchProcessor] = None
    ):
        super().__init__()
        self.db_path = db_path
        self._app_state = app_state
        self.signals = ETLWorkerSignals()
        self._is_running = True
        self.db_lock = Lock()

        self.storage_repo = storage_repo or ETLStorageRepository(db_path, self.db_lock)
        self.processor = processor or SensorBatchProcessor()

    def stop(self):
        """Signals the worker to abort execution gracefully."""
        self._is_running = False

    def _process_sensor_worker(self, source, folder_schema) -> tuple[int, int]:
        """
        Processes all files for a specific sensor in parallel, batching disk writes.
        """
        source_name = source.name
        source_path = source.path
        section_table = self.storage_repo.get_section_table_name(source_name)

        if not os.path.isdir(source_path):
            return 0, 0

        try:
            all_files = []
            for root, _, filenames in os.walk(source_path):
                for f in filenames:
                    all_files.append(os.path.join(root, f))
            files = sorted(all_files)
        except Exception:
            return 0, 0

        assoc_type_str = getattr(source, 'association_type', "LOCAL")
        if hasattr(assoc_type_str, 'value'):
            assoc_type_str = assoc_type_str.value

        local_files = 0
        local_events = 0
        conn = None

        try:
            conn = self.storage_repo.get_connection()
            raw_storage_batch = []
            events_batch = []

            def flush():
                nonlocal local_files, local_events
                if raw_storage_batch or events_batch:
                    f_count, e_count = self.storage_repo.save_batch(
                        conn, section_table, raw_storage_batch, events_batch
                    )
                    local_files += f_count
                    local_events += e_count
                    raw_storage_batch.clear()
                    events_batch.clear()

            for filename in files:
                if not self._is_running:
                    break

                try:
                    raw_tuple, event_tuples = self.processor.process_file(
                        filename, source_name, folder_schema, assoc_type=assoc_type_str
                    )
                    raw_storage_batch.append(raw_tuple)
                    events_batch.extend(event_tuples)

                    if len(raw_storage_batch) >= self.BATCH_SIZE:
                        flush()

                except sqlite3.Error as e:
                    logger.error(f"ETLWorker [Thread {source_name}]: {backend_i18n.t('errors.etl.db_error', file=os.path.basename(filename), error=str(e))}")
                except Exception as e:
                    logger.error(f"ETLWorker [Thread {source_name}]: {backend_i18n.t('errors.etl.process_error', file=os.path.basename(filename), error=str(e))}")

            flush()

        except Exception as e:
            logger.error(f"ETLWorker: {backend_i18n.t('errors.etl.critical_thread_error', source=source_name, error=str(e))}")
        finally:
            if conn:
                conn.close()

        return local_files, local_events

    @Slot()
    def run(self):
        """Main entry point for QRunnable. Orchestrates Pass 1 (Discovery) and Pass 2 (Ingestion)."""
        logger.info(backend_i18n.t("etl.start_ingestion", db=self.db_path))

        sources = self._app_state.get_all_data_sources()
        if not sources:
            self.signals.finished.emit(self.db_path)
            return

        self.storage_repo.init_database()
        transformer = self.processor.transformer

        try:
            transformer.initialize_encoder()

            total_files = 0
            total_extracted_events = 0

            # =========================================================
            # PASS 1: SCHEMA DISCOVERY (SEQUENTIAL, PROTECTING VRAM)
            # =========================================================
            logger.info(backend_i18n.t("etl.pass1_start"))
            schema_registry = {}

            for source in sources:
                if not self._is_running:
                    break

                source_name = source.name
                source_path = source.path

                if not os.path.isdir(source_path):
                    continue

                try:
                    all_files = []
                    for root, _, filenames in os.walk(source_path):
                        for f in filenames:
                            all_files.append(os.path.join(root, f))
                    files = sorted(all_files)
                except Exception:
                    continue
                if not files:
                    continue

                first_file = next((f for f in files if os.path.getsize(f) > 0), files[0])
                file_full_path = first_file
                first_file_name = os.path.basename(file_full_path)

                try:
                    with open(file_full_path, "rb") as f:
                        raw_content = f.read()

                    raw_text_decoded = raw_content.decode('utf-8', errors='ignore')
                    logger.info(backend_i18n.t("etl.discover_schema", source=source_name, file=first_file_name))

                    assoc_type_str = getattr(source, 'association_type', "LOCAL")
                    if hasattr(assoc_type_str, 'value'):
                        assoc_type_str = assoc_type_str.value

                    folder_schema = transformer.discover_schema(raw_text_decoded, source_name, assoc_type_str)
                    schema_registry[source_name] = folder_schema
                except Exception as e:
                    logger.error(f"ETLWorker: {backend_i18n.t('errors.etl.schema_discovery_failed', source=source_name, error=str(e))}")
                    schema_registry[source_name] = None

            if not self._is_running:
                return

            # =========================================================
            # PASS 2: PHYSICS MATH & DATABASE INGESTION PHASE (PARALLEL)
            # =========================================================
            logger.info(backend_i18n.t("etl.pass2_start"))

            max_threads = max(1, len(sources))
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = []
                for source in sources:
                    if not self._is_running:
                        break
                    folder_schema = schema_registry.get(source.name)
                    futures.append(executor.submit(self._process_sensor_worker, source, folder_schema))

                for future in concurrent.futures.as_completed(futures):
                    try:
                        f_count, e_count = future.result()
                        total_files += f_count
                        total_extracted_events += e_count
                    except Exception as e:
                        logger.error(f"ETLWorker: {backend_i18n.t('errors.etl.future_failed', error=str(e))}")

            logger.info(backend_i18n.t("etl.pass2_completed", files=total_files, events=total_extracted_events))
            transformer.cleanup_encoder()

        except Exception as e:
            logger.critical(f"ETLWorker: {backend_i18n.t('errors.etl.critical_error', error=str(e))}", exc_info=True)
            self.signals.error.emit(str(e))
        finally:
            transformer.cleanup_encoder()
            self.signals.finished.emit(self.db_path)


class ETLService(QObject):
    """
    High-level PySide6 Service that coordinates ETLWorker execution via QThreadPool
    and manages GUI lifecycle signals.
    """
    ingestion_finished = Signal(str)
    ingestion_progress = Signal(int)
    ingestion_error = Signal(str)

    def __init__(self, app_state: AppState):
        super().__init__()
        self._app_state = app_state
        self._thread_pool = QThreadPool.globalInstance()
        self._current_worker: Optional[ETLWorker] = None

    def start_ingestion(self, db_path: str):
        """Starts the ETL worker in the background thread pool."""
        self._current_worker = ETLWorker(db_path, self._app_state)
        self._current_worker.signals.finished.connect(self.ingestion_finished)
        self._current_worker.signals.progress.connect(self.ingestion_progress)
        self._current_worker.signals.error.connect(self.ingestion_error)
        self._thread_pool.start(self._current_worker)

    def stop_ingestion(self):
        """Requests cancellation of the running worker."""
        if self._current_worker:
            self._current_worker.stop()