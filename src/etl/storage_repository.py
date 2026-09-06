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

# File: src/etl/storage_repository.py
# Author: Gabriel Moraes
# Date: June 2026
# Description:
#    High-Performance ETL Storage Repository.
#    Encapsulates SQLite connection management, WAL concurrency configuration,
#    and thread-safe atomic batch persistence for raw payloads and normalized traffic sections.

import sqlite3
import logging
from threading import Lock
from typing import List, Tuple, Optional
from src.utils.i18n import backend_i18n

logger = logging.getLogger(__name__)


class ETLStorageRepository:
    """
    Data Access Object (DAO) / Repository for ETL operations.
    Follows Single Responsibility Principle (SRP) by handling only database persistence,
    PRAGMA tuning, and thread-safe batch transactions.
    """

    def __init__(self, db_path: str, db_lock: Optional[Lock] = None):
        self.db_path = db_path
        self.db_lock = db_lock or Lock()

    def init_database(self):
        """
        Initializes global database settings (WAL journal mode and busy timeout) safely once
        before worker threads begin concurrent processing.
        """
        with self.db_lock:
            conn = sqlite3.connect(self.db_path, timeout=120.0)
            try:
                cursor = conn.cursor()
                cursor.execute("PRAGMA journal_mode = WAL;")
                cursor.execute("PRAGMA busy_timeout = 120000;")
                conn.commit()
            finally:
                conn.close()

    def get_connection(self) -> sqlite3.Connection:
        """
        Creates and configures a high-throughput SQLite thread connection with cache and busy timeout.
        """
        conn = sqlite3.connect(self.db_path, timeout=120.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA busy_timeout = 120000;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA cache_size = -64000;")
        cursor.execute("PRAGMA temp_store = MEMORY;")
        return conn

    @staticmethod
    def get_section_table_name(source_name: str) -> Optional[str]:
        """Generates a sanitized table name for the sensor section."""
        if not source_name:
            return None
        safe_name = "".join([c if c.isalnum() else "_" for c in source_name]).lower()
        return f"section_{safe_name}"

    def save_batch(
        self,
        conn: sqlite3.Connection,
        section_table: Optional[str],
        raw_storage_batch: List[Tuple[str, str, str, int, str, bytes]],
        events_batch: List[Tuple[str, str, str, str]]
    ) -> Tuple[int, int]:
        """
        Persists raw storage records and section events in a single atomic transaction.
        Returns the count of saved files and events.
        """
        if not raw_storage_batch and not events_batch:
            return 0, 0

        saved_files = 0
        saved_events = 0

        with self.db_lock:
            cursor = conn.cursor()
            if raw_storage_batch:
                cursor.executemany("""
                    INSERT INTO raw_data_storage (
                        source_id, filename, file_extension, 
                        file_size_bytes, file_hash, raw_content
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, raw_storage_batch)
                saved_files = len(raw_storage_batch)

            if events_batch and section_table:
                cursor.executemany(f"""
                    INSERT INTO {section_table} (
                        event_timestamp, sensor_id, data_payload, raw_file_reference
                    ) VALUES (?, ?, ?, ?)
                """, events_batch)
                saved_events = len(events_batch)

            conn.commit()

        return saved_files, saved_events
