import gzip
import pytest
from unittest.mock import patch, MagicMock
from lxml import etree
from src.services.map_importer import MapImportWorker, NetXMLParserTarget, MapImporter
from src.domain.app_state import AppState


@pytest.fixture
def app_state(qapp):
    return AppState()


def test_net_xml_parser_target():
    target = NetXMLParserTarget()

    target.start("junction", {"id": "n1", "x": "10.5", "y": "20.5"})
    assert len(target.nodes) == 1
    assert target.nodes[0].id == "n1"

    # Missing attributes handled safely
    target.start("junction", {"id": "bad_node"})
    assert len(target.nodes) == 1

    target.start("edge", {"id": "e1", "from": "n1", "to": "n2"})
    target.start("lane", {"shape": "10.5,20.5 30.0,40.0"})
    target.end("edge")

    assert len(target.edges) == 1
    assert target.edges[0].id == "e1"
    assert len(target.edges[0].shape) == 2
    assert target.edges[0].shape[0] == (10.5, 20.5)

    # Calling data and close
    target.data("some text")
    assert target.close() == "Parsing finished"


def test_parse_real_net_xml_and_gz(tmp_path, app_state):
    xml_content = b"""<net>
    <junction id="j1" x="1.0" y="2.0" type="priority"/>
    <edge id="e1" from="j1" to="j2">
        <lane shape="1.0,2.0 3.0,4.0"/>
    </edge>
</net>"""

    # 1. Plain .net.xml
    xml_file = tmp_path / "test.net.xml"
    xml_file.write_bytes(xml_content)

    worker = MapImportWorker(str(xml_file), app_state)
    nodes, edges = worker._parse_net_xml(str(xml_file))
    assert len(nodes) == 1
    assert len(edges) == 1
    worker.run()
    assert len(app_state.get_all_nodes()) == 1

    # 2. Compressed .net.xml.gz
    gz_file = tmp_path / "test.net.xml.gz"
    with gzip.open(gz_file, "wb") as f:
        f.write(xml_content)

    nodes_gz, edges_gz = worker._parse_net_xml(str(gz_file))
    assert len(nodes_gz) == 1
    assert len(edges_gz) == 1


def test_map_import_worker_errors(tmp_path, app_state):
    # Syntax error file
    bad_file = tmp_path / "bad.net.xml"
    bad_file.write_text("<net><unclosed></net>")

    worker = MapImportWorker(str(bad_file), app_state)
    worker.run()  # Catches XMLSyntaxError gracefully

    # Nonexistent file
    worker_missing = MapImportWorker(str(tmp_path / "missing.xml"), app_state)
    worker_missing.run()


def test_map_importer_load_map(app_state):
    importer = MapImporter(app_state)
    with patch.object(importer._thread_pool, "start") as mock_start:
        importer.load_map("/fake/map.net.xml")
        mock_start.assert_called_once()

    with patch.object(importer._thread_pool, "start") as mock_start:
        importer.load_map("")
        mock_start.assert_not_called()
