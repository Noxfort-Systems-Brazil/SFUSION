# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Gabriel Moraes - Noxfort Systems
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# File: tests/test_etl/test_storage_repository.py
# Author: Gabriel Moraes
# Date: June 2026

import pytest
import sqlite3
import os
from src.etl.storage_repository import ETLStorageRepository


@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_etl.db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE raw_data_storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT,
            filename TEXT,
            file_extension TEXT,
            file_size_bytes INTEGER,
            file_hash TEXT,
            raw_content BLOB
        )
    """)
    cursor.execute("""
        CREATE TABLE section_cam_01 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_timestamp TEXT,
            sensor_id TEXT,
            data_payload TEXT,
            raw_file_reference TEXT
        )
    """)
    conn.commit()
    conn.close()
    return db_file


def test_storage_repository_get_connection(temp_db):
    repo = ETLStorageRepository(temp_db)
    repo.init_database()
    conn = repo.get_connection()
    assert conn is not None
    cursor = conn.cursor()
    res = cursor.execute("PRAGMA journal_mode;").fetchone()
    assert res[0].upper() == "WAL"
    conn.close()


def test_storage_repository_save_batch(temp_db):
    repo = ETLStorageRepository(temp_db)
    conn = repo.get_connection()

    raw_batch = [
        ("cam_01", "file1.json", ".json", 100, "hash1", b"content1"),
        ("cam_01", "file2.json", ".json", 200, "hash2", b"content2")
    ]
    events_batch = [
        ("2026-06-08 00:00:00", "cam_01", '{"speed_val": 10.0}', "file1.json"),
        ("2026-06-08 00:00:10", "cam_01", '{"speed_val": 12.0}', "file2.json")
    ]

    saved_f, saved_e = repo.save_batch(conn, "section_cam_01", raw_batch, events_batch)
    assert saved_f == 2
    assert saved_e == 2

    cursor = conn.cursor()
    raw_count = cursor.execute("SELECT COUNT(*) FROM raw_data_storage;").fetchone()[0]
    events_count = cursor.execute("SELECT COUNT(*) FROM section_cam_01;").fetchone()[0]
    assert raw_count == 2
    assert events_count == 2
    conn.close()


def test_get_section_table_name():
    assert ETLStorageRepository.get_section_table_name("Camera North") == "section_camera_north"
    assert ETLStorageRepository.get_section_table_name("loop-01") == "section_loop_01"
    assert ETLStorageRepository.get_section_table_name("") is None
