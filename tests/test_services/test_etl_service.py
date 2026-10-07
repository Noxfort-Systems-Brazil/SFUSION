import os
import pytest
from unittest.mock import MagicMock, patch
from src.services.etl_service import ETLWorker, ETLService
from src.domain.app_state import AppState
from src.domain.entities import DataSource, AssociationType
from src.core.schemas import KinematicMap


@pytest.fixture
def etl_setup(tmp_path, qapp):
    db_path = str(tmp_path / "test_etl.db")
    app_state = AppState()
    storage_repo = MagicMock()
    processor = MagicMock()

    worker = ETLWorker(
        db_path=db_path,
        app_state=app_state,
        storage_repo=storage_repo,
        processor=processor
    )
    return {
        "db_path": db_path,
        "app_state": app_state,
        "storage_repo": storage_repo,
        "processor": processor,
        "worker": worker,
        "tmp_path": tmp_path
    }


def test_etl_worker_run_empty_sources(etl_setup):
    worker = etl_setup["worker"]
    db_path = etl_setup["db_path"]

    finished_signals = []
    worker.signals.finished.connect(lambda p: finished_signals.append(p))

    worker.run()
    assert finished_signals == [db_path]


def test_etl_worker_run_with_sources(etl_setup):
    setup = etl_setup
    worker = setup["worker"]
    app_state = setup["app_state"]
    processor = setup["processor"]
    storage_repo = setup["storage_repo"]
    tmp_path = setup["tmp_path"]

    # Create dummy sensor folder with a file
    sensor_dir = tmp_path / "sensor_folder"
    sensor_dir.mkdir()
    sample_file = sensor_dir / "sample.json"
    sample_file.write_text('{"speed": 50}')

    source = DataSource(name="sensor_folder", path=str(sensor_dir), association_type=AssociationType.LOCAL)
    app_state.add_data_source(source)

    transformer = MagicMock()
    processor.transformer = transformer
    transformer.discover_schema.return_value = KinematicMap(speed_col="speed", speed_unit="km/h")
    processor.process_file.return_value = (
        ("hash", 100, b"raw"),
        [("hash", "2026-01-01T00:00:00Z", "sensor_folder", 50.0, 0.0, 0.0, None, None, '{"speed": 50}')]
    )

    storage_repo.save_batch.return_value = (1, 1)

    finished_signals = []
    worker.signals.finished.connect(lambda p: finished_signals.append(p))

    worker.run()

    storage_repo.init_database.assert_called_once()
    transformer.initialize_encoder.assert_called_once()
    transformer.cleanup_encoder.assert_called()
    assert len(finished_signals) == 1


def test_etl_worker_stop(etl_setup):
    worker = etl_setup["worker"]
    assert worker._is_running
    worker.stop()
    assert not worker._is_running


def test_etl_service_lifecycle(tmp_path, qapp):
    app_state = AppState()
    service = ETLService(app_state)
    db_path = str(tmp_path / "service_test.db")

    with patch.object(service._thread_pool, "start") as mock_start:
        service.start_ingestion(db_path)
        assert service._current_worker is not None
        mock_start.assert_called_once_with(service._current_worker)

        service.stop_ingestion()
        assert not service._current_worker._is_running
