import pytest
from src.domain.app_state import AppState
from src.domain.entities import MapNode, MapEdge, DataSource, AssociationType


@pytest.fixture
def app_state(qapp):
    return AppState()


def test_initial_state(app_state):
    assert len(app_state.get_all_nodes()) == 0
    assert len(app_state.get_all_edges()) == 0
    assert len(app_state.get_all_data_sources()) == 0
    assert not app_state.is_in_association_mode()
    assert not app_state._is_savable()


def test_set_map_data(app_state):
    nodes = [MapNode(id="n1", x=0, y=0)]
    edges = [
        MapEdge(id="e1", from_node="n1", to_node="n2"),
        MapEdge(id="-e1", from_node="n2", to_node="n1")
    ]
    
    app_state.set_map_data(nodes, edges)
    
    assert len(app_state.get_all_nodes()) == 1
    assert len(app_state.get_all_edges()) == 2
    assert app_state.get_node_by_id("n1") == nodes[0]
    assert app_state.get_edge_by_id("e1") == edges[0]
    assert app_state.get_node_by_id("missing") is None
    assert app_state.get_edge_by_id("missing") is None


def test_edge_pair_id(app_state):
    edges = [
        MapEdge(id="roadA", from_node="n1", to_node="n2"),
        MapEdge(id="-roadA", from_node="n2", to_node="n1"),
        MapEdge(id="roadSolo", from_node="n3", to_node="n4")
    ]
    app_state.set_map_data([], edges)

    assert app_state.get_edge_pair_id("roadA") == "-roadA"
    assert app_state.get_edge_pair_id("-roadA") == "roadA"
    assert app_state.get_edge_pair_id("roadSolo") is None


def test_update_element_real_name(app_state):
    node = MapNode(id="n1", x=0, y=0)
    edge = MapEdge(id="e1", from_node="n1", to_node="n2")
    app_state.set_map_data([node], [edge])

    app_state.update_element_real_name("n1", "Prado Junction")
    assert node.real_name == "Prado Junction"

    app_state.update_element_real_name("e1", "Paulista Ave")
    assert edge.real_name == "Paulista Ave"

    # Blank reset to None
    app_state.update_element_real_name("e1", "")
    assert edge.real_name is None

    # Missing element logs warning without raising
    app_state.update_element_real_name("nonexistent", "Name")


def test_add_and_delete_data_source(app_state):
    ds1 = DataSource(path="/tmp/d1", name="Data 1")
    app_state.add_data_source(ds1)
    
    assert len(app_state.get_all_data_sources()) == 1
    assert app_state.get_data_source_by_id("/tmp/d1") == ds1

    # Adding duplicate is rejected
    app_state.add_data_source(ds1)
    assert len(app_state.get_all_data_sources()) == 1

    app_state.set_selected_data_source("/tmp/d1")
    app_state.delete_data_source("/tmp/d1")
    assert len(app_state.get_all_data_sources()) == 0
    assert app_state._selected_source_path is None

    # Deleting nonexistent logs warning without error
    app_state.delete_data_source("/tmp/nonexistent")


def test_toggle_and_update_association_type(app_state):
    ds = DataSource(path="/tmp/d1", name="Data 1", association_type=AssociationType.LOCAL)
    app_state.add_data_source(ds)
    app_state.set_selected_data_source("/tmp/d1")

    # Toggle to GLOBAL
    app_state.toggle_source_association_type("/tmp/d1")
    assert ds.association_type == AssociationType.GLOBAL

    # Toggle back to LOCAL
    app_state.toggle_source_association_type("/tmp/d1")
    assert ds.association_type == AssociationType.LOCAL

    # Update selected source association type
    app_state.update_selected_source_association_type("GLOBAL")
    assert ds.association_type == AssociationType.GLOBAL

    # Invalid type handled gracefully
    app_state.update_selected_source_association_type("INVALID_TYPE")
    assert ds.association_type == AssociationType.GLOBAL

    # Nonexistent source toggle ignored
    app_state.toggle_source_association_type("unknown")


def test_association_mode_and_associate(app_state):
    ds = DataSource(path="/tmp/d1", name="Data 1")
    node = MapNode(id="n1", x=0, y=0)
    app_state.set_map_data([node], [])
    app_state.add_data_source(ds)

    # Enter without selection does nothing
    app_state.enter_association_mode()
    assert not app_state.is_in_association_mode()

    # Select and enter
    app_state.set_selected_data_source("/tmp/d1")
    app_state.enter_association_mode()
    assert app_state.is_in_association_mode()

    # Enter again is idempotent
    app_state.enter_association_mode()
    assert app_state.is_in_association_mode()

    # Associate to node
    app_state.associate_selected_source_to_element("n1")
    assert not app_state.is_in_association_mode()
    assert ds.associated_element_id == "n1"

    # Already associated source cannot enter association mode again
    app_state.set_selected_data_source("/tmp/d1")
    app_state.enter_association_mode()
    assert not app_state.is_in_association_mode()

    # Exit mode
    app_state.set_selected_data_source(None)
    assert not app_state.is_in_association_mode()


def test_editor_associations_and_savable_state(app_state):
    node = MapNode(id="n1", x=0, y=0)
    app_state.set_map_data([node], [])

    ds1 = DataSource(path="/s1", name="Sensor 1", association_type=AssociationType.LOCAL)
    ds2 = DataSource(path="/s2", name="Sensor 2", association_type=AssociationType.LOCAL)
    app_state.add_data_source(ds1)
    app_state.add_data_source(ds2)

    # Initially not savable (no associations)
    assert not app_state._is_savable()

    # Available local sources for n1
    avail = app_state.get_available_local_sources("n1")
    assert len(avail) == 2

    # Assign ds1 to n1 (ds2 is still unassociated -> not savable)
    app_state.set_element_associations("n1", ["/s1"])
    assert ds1.associated_element_id == "n1"
    assert app_state.get_sources_associated_with_element("n1") == [ds1]
    assert not app_state._is_savable()

    # Assign both ds1 and ds2 to n1 (all local sources associated -> savable)
    app_state.set_element_associations("n1", ["/s1", "/s2"])
    assert ds1.associated_element_id == "n1"
    assert ds2.associated_element_id == "n1"
    assert app_state._is_savable()

    # Unassign ds1 by only passing ds2
    app_state.set_element_associations("n1", ["/s2"])
    assert ds1.associated_element_id is None
    assert ds2.associated_element_id == "n1"
    assert not app_state._is_savable()

