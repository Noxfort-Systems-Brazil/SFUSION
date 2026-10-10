import pytest
from src.services.extractors import UniversalExtractor, BaseExtractor
from datetime import datetime


def test_base_extractor_not_implemented():
    base = BaseExtractor()
    with pytest.raises(NotImplementedError):
        base.extract("file.txt", b"")


def test_extract_json_various_timestamps():
    ext = UniversalExtractor()

    # Millis timestamp
    c1 = b'[{"speed": 50, "time": 1700000000000}]'
    r1 = ext.extract("t1.json", c1, "s1")
    assert len(r1) == 1
    assert r1[0]["event_timestamp"] == datetime.fromtimestamp(1700000000)

    # Seconds timestamp
    c2 = b'[{"speed": 50, "time": 1700000000}]'
    r2 = ext.extract("t2.json", c2, "s2")
    assert len(r2) == 1
    assert r2[0]["event_timestamp"] == datetime.fromtimestamp(1700000000)

    # ISO string timestamp
    c3 = b'[{"speed": 50, "date": "2026-06-01T12:00:00Z"}]'
    r3 = ext.extract("t3.json", c3, "s3")
    assert len(r3) == 1
    assert r3[0]["event_timestamp"].year == 2026

    # Malformed timestamp falls back to default
    c4 = b'[{"speed": 50, "timestamp": "not-a-date"}]'
    r4 = ext.extract("t4.json", c4, "s4")
    assert len(r4) == 1
    assert isinstance(r4[0]["event_timestamp"], datetime)


def test_extract_json_dict():
    ext = UniversalExtractor()
    content = b'{"alerts": [{"speed": 50}]}'
    res = ext.extract("test.json", content, "sensor1")
    assert len(res) == 1
    assert res[0]["data_payload"]["speed"] == 50


def test_extract_csv():
    ext = UniversalExtractor()
    content = b'speed,time\n50,160000'
    res = ext.extract("test.csv", content, "sensor2")
    assert len(res) == 1
    assert res[0]["data_payload"]["speed"] == "50"
    assert res[0]["event_timestamp"] == datetime.fromtimestamp(160000)


def test_extract_csv_iso_timestamp():
    ext = UniversalExtractor()
    content = b'speed,date\n80,2026-06-01T15:30:00Z'
    res = ext.extract("test.csv", content, "sensor3")
    assert len(res) == 1
    assert res[0]["data_payload"]["speed"] == "80"
    assert res[0]["event_timestamp"].year == 2026


def test_extract_excel(tmp_path):
    import pandas as pd
    import io
    ext = UniversalExtractor()
    
    df = pd.DataFrame([{"speed": 75, "timestamp": "2026-07-01T10:00:00Z"}])
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    raw_content = buffer.getvalue()
    
    res = ext.extract("data.xlsx", raw_content, "excel_sensor")
    assert len(res) == 1
    assert res[0]["data_payload"]["speed"] == 75
    assert res[0]["sensor_id"] == "excel_sensor"


def test_extract_invalid():
    ext = UniversalExtractor()
    content = b'\x00\x01\x02'
    res = ext.extract("test.bin", content)
    assert isinstance(res, list)
