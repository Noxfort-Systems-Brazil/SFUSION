import pytest
from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsPathItem
from ui.map.map_view import MapView


@pytest.fixture
def map_view(qapp):
    view = MapView()
    view.resize(400, 300)
    return view


def test_map_view_initialization(map_view):
    assert map_view.scene is not None
    assert map_view.scene.backgroundBrush().color() == Qt.white
    assert not map_view._is_panning
    assert map_view._last_pan_point is None


def test_fit_map_in_view(map_view):
    # Empty scene: does not raise
    map_view.fit_map_in_view()

    # Scene with items
    item = map_view.scene.addEllipse(0, 0, 100, 100)
    map_view.fit_map_in_view()
    assert map_view.scene.itemsBoundingRect().isValid()


def test_set_zoom_limits(map_view):
    # Should log without error
    map_view.set_zoom_limits(0.5, 5.0)


def test_wheel_zoom(map_view):
    transform_before = map_view.transform()

    # Zoom in
    wheel_in = QWheelEvent(
        QPointF(50, 50),
        QPointF(50, 50),
        QPoint(0, 0),
        QPoint(0, 120),
        Qt.NoButton,
        Qt.NoModifier,
        Qt.ScrollUpdate,
        False
    )
    map_view.wheelEvent(wheel_in)
    assert map_view.transform().m11() > transform_before.m11()

    # Zoom out
    wheel_out = QWheelEvent(
        QPointF(50, 50),
        QPointF(50, 50),
        QPoint(0, 0),
        QPoint(0, -120),
        Qt.NoButton,
        Qt.NoModifier,
        Qt.ScrollUpdate,
        False
    )
    map_view.wheelEvent(wheel_out)


def test_mouse_pan_interaction(map_view):
    # Middle click starts pan
    press_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        QPointF(50, 50),
        QPointF(50, 50),
        Qt.MiddleButton,
        Qt.MiddleButton,
        Qt.NoModifier
    )
    map_view.mousePressEvent(press_event)
    assert map_view._is_panning
    assert map_view._last_pan_point == QPoint(50, 50)

    # Mouse move updates scrollbars
    move_event = QMouseEvent(
        QMouseEvent.Type.MouseMove,
        QPointF(60, 70),
        QPointF(60, 70),
        Qt.MiddleButton,
        Qt.MiddleButton,
        Qt.NoModifier
    )
    map_view.mouseMoveEvent(move_event)
    assert map_view._last_pan_point == QPoint(60, 70)

    # Release ends pan
    release_event = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        QPointF(60, 70),
        QPointF(60, 70),
        Qt.MiddleButton,
        Qt.NoButton,
        Qt.NoModifier
    )
    map_view.mouseReleaseEvent(release_event)
    assert not map_view._is_panning


def test_scene_click_signals(map_view):
    node_clicks = []
    edge_clicks = []
    empty_clicks = []

    map_view.nodeClicked.connect(lambda nid: node_clicks.append(nid))
    map_view.edgeClicked.connect(lambda eid: edge_clicks.append(eid))
    map_view.emptySpaceClicked.connect(lambda: empty_clicks.append(True))

    # Add a node item and an edge item to the scene
    node_item = QGraphicsEllipseItem(10, 10, 20, 20)
    node_item.setData(0, "node")
    node_item.setData(1, "node_junction_1")
    map_view.scene.addItem(node_item)

    edge_item = QGraphicsEllipseItem(50, 50, 20, 20)
    edge_item.setData(0, "edge")
    edge_item.setData(1, "edge_road_42")
    map_view.scene.addItem(edge_item)

    # Click on empty space
    map_view._on_scene_clicked(QPoint(200, 200))
    assert len(empty_clicks) == 1

    # Click on node item
    map_view._on_scene_clicked(map_view.mapFromScene(QPointF(20, 20)))
    assert node_clicks == ["node_junction_1"]

    # Click on edge item
    map_view._on_scene_clicked(map_view.mapFromScene(QPointF(60, 60)))
    assert edge_clicks == ["edge_road_42"]
