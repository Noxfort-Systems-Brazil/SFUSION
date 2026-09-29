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

# File: tests/test_controllers/test_main_controller.py
# Author: Gabriel Moraes
# Date: November 2025

import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import QCoreApplication
from src.main_controller import MainController




@pytest.fixture
def mock_dependencies(qapp):
    main_window = MagicMock()
    map_importer = MagicMock()
    data_importer = MagicMock()
    persistence_service = MagicMock()
    project_service = MagicMock()
    etl_service = MagicMock()
    parquet_service = MagicMock()
    i18n = MagicMock()
    i18n.t.side_effect = lambda key, **kwargs: key

    controller = MainController(
        main_window=main_window,
        map_importer=map_importer,
        data_importer=data_importer,
        persistence_service=persistence_service,
        project_service=project_service,
        etl_service=etl_service,
        parquet_service=parquet_service,
        i18n=i18n,
    )
    return {
        "controller": controller,
        "main_window": main_window,
        "map_importer": map_importer,
        "data_importer": data_importer,
        "persistence_service": persistence_service,
        "project_service": project_service,
        "etl_service": etl_service,
        "parquet_service": parquet_service,
        "i18n": i18n,
    }


def test_on_import_map_success(mock_dependencies):
    controller = mock_dependencies["controller"]
    map_importer = mock_dependencies["map_importer"]
    main_window = mock_dependencies["main_window"]

    with patch("src.main_controller.QFileDialog.getOpenFileName", return_value=("/path/to/test.net.xml", "XML files")):
        controller._on_import_map()
        map_importer.load_map.assert_called_once_with("/path/to/test.net.xml")
        main_window.show_status_message.assert_called_once()


def test_on_import_map_cancelled(mock_dependencies):
    controller = mock_dependencies["controller"]
    map_importer = mock_dependencies["map_importer"]

    with patch("src.main_controller.QFileDialog.getOpenFileName", return_value=("", "")):
        controller._on_import_map()
        map_importer.load_map.assert_not_called()


def test_on_add_source_success(mock_dependencies):
    controller = mock_dependencies["controller"]
    data_importer = mock_dependencies["data_importer"]
    main_window = mock_dependencies["main_window"]

    with patch("src.main_controller.QFileDialog.getExistingDirectory", return_value="/path/to/source_dir"):
        controller._on_add_source()
        data_importer.add_data_source.assert_called_once_with("/path/to/source_dir", "LOCAL")
        main_window.show_status_message.assert_called_once()


def test_on_add_source_cancelled(mock_dependencies):
    controller = mock_dependencies["controller"]
    data_importer = mock_dependencies["data_importer"]

    with patch("src.main_controller.QFileDialog.getExistingDirectory", return_value=""):
        controller._on_add_source()
        data_importer.add_data_source.assert_not_called()


def test_on_open_project(mock_dependencies):
    controller = mock_dependencies["controller"]
    project_service = mock_dependencies["project_service"]
    main_window = mock_dependencies["main_window"]

    with patch("src.main_controller.QFileDialog.getOpenFileName", return_value=("/path/to/project.json", "JSON files")):
        controller._on_open_project()
        project_service.load_project.assert_called_once_with("/path/to/project.json")
        main_window.show_status_message.assert_called_once()


def test_on_save_project(mock_dependencies):
    controller = mock_dependencies["controller"]
    project_service = mock_dependencies["project_service"]
    main_window = mock_dependencies["main_window"]

    with patch("src.main_controller.QFileDialog.getSaveFileName", return_value=("/path/to/project.json", "JSON files")):
        controller._on_save_project()
        project_service.save_project.assert_called_once_with("/path/to/project.json")
        main_window.show_status_message.assert_called_once()


def test_setup_connections(mock_dependencies):
    controller = mock_dependencies["controller"]
    main_window = mock_dependencies["main_window"]
    etl = mock_dependencies["etl_service"]
    parquet = mock_dependencies["parquet_service"]

    controller.setup_connections()
    main_window.open_project_requested.connect.assert_called_once()
    main_window.save_project_requested.connect.assert_called_once()
    main_window.open_map_requested.connect.assert_called_once()
    main_window.add_source_requested.connect.assert_called_once()
    main_window.save_config_requested.connect.assert_called_once()
    etl.ingestion_finished.connect.assert_called_once()
    parquet.export_finished.connect.assert_called_once()


def test_pipeline_save_config_flow(mock_dependencies, tmp_path):
    controller = mock_dependencies["controller"]
    persistence = mock_dependencies["persistence_service"]
    etl = mock_dependencies["etl_service"]
    parquet = mock_dependencies["parquet_service"]
    main_window = mock_dependencies["main_window"]

    target_file = str(tmp_path / "output.parquet")

    with patch("src.main_controller.QFileDialog.getSaveFileName", return_value=(target_file, "Parquet files")), \
         patch("src.main_controller.QMessageBox.information"):
        
        # 1. Start pipeline
        controller._on_save_config()
        persistence.save_configuration.assert_called_once()
        etl.start_ingestion.assert_called_once()
        main_window.set_savable_state.assert_called_with(False)

        # 2. Ingestion finished -> triggers Parquet export
        temp_db = controller._temp_db_path
        controller._on_ingestion_finished(temp_db)
        parquet.export_db_to_parquet.assert_called_once_with(temp_db, target_file)

        # 3. Export finished -> cleanup and unlock UI
        controller._on_export_finished()
        main_window.set_savable_state.assert_called_with(True)


def test_pipeline_save_config_error(mock_dependencies):
    controller = mock_dependencies["controller"]
    persistence = mock_dependencies["persistence_service"]
    main_window = mock_dependencies["main_window"]

    persistence.save_configuration.side_effect = RuntimeError("DB write failed")

    with patch("src.main_controller.QFileDialog.getSaveFileName", return_value=("/tmp/out.parquet", "Parquet files")):
        controller._on_save_config()
        main_window.set_savable_state.assert_called_with(True)
        main_window.show_error_message.assert_called_once()


def test_cleanup_temp_files(mock_dependencies, tmp_path):
    controller = mock_dependencies["controller"]
    db_file = tmp_path / "test.db"
    wal_file = tmp_path / "test.db-wal"
    db_file.write_text("db")
    wal_file.write_text("wal")

    assert db_file.exists()
    assert wal_file.exists()

    controller._cleanup_temp_files(str(db_file))

    assert not db_file.exists()
    assert not wal_file.exists()

