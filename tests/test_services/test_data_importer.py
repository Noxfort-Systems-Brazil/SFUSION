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

# File: tests/test_services/test_data_importer.py
# Author: Gabriel Moraes
# Date: November 2025

import os
import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import QCoreApplication
from src.services.data_importer import DataImportWorker, DataImporter
from src.domain.app_state import AppState
from src.domain.entities import AssociationType

@pytest.fixture(scope="session")
def qapp():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    yield app

@pytest.fixture
def app_state(qapp):
    return AppState()

def test_analyze_folder_success():
    with patch('os.listdir', return_value=['data.csv', 'info.JSON', 'map.net.xml', 'other.txt']):
        worker = DataImportWorker('/fake/path', AppState(), 'GLOBAL')
        types = worker._analyze_folder('/fake/path')
        assert 'CSV' in types
        assert 'JSON' in types
        assert 'XML' not in types

def test_analyze_folder_errors():
    worker = DataImportWorker('/fake/path', AppState(), 'GLOBAL')
    with patch('os.listdir', side_effect=FileNotFoundError):
        assert worker._analyze_folder('/fake/path') == []
    with patch('os.listdir', side_effect=NotADirectoryError):
        assert worker._analyze_folder('/fake/path') == []

def test_worker_run(app_state):
    worker = DataImportWorker('/fake/path', app_state, 'GLOBAL')
    with patch.object(worker, '_analyze_folder', return_value=['CSV']):
        worker.run()
        sources = app_state.get_all_data_sources()
        assert len(sources) == 1
        assert sources[0].path == '/fake/path'
        assert sources[0].file_types == ['CSV']
        assert sources[0].association_type == AssociationType.GLOBAL

def test_data_importer_add_source(app_state):
    importer = DataImporter(app_state)
    with patch('os.path.isdir', return_value=True):
        with patch.object(importer._thread_pool, 'start') as mock_start:
            importer.add_data_source('/fake/path', 'GLOBAL')
            mock_start.assert_called_once()
            
    with patch('os.path.isdir', return_value=False):
        with patch.object(importer._thread_pool, 'start') as mock_start:
            importer.add_data_source('/bad/path', 'GLOBAL')
            mock_start.assert_not_called()
