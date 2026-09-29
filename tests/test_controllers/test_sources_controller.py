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

# File: tests/test_controllers/test_sources_controller.py
# Description: Tests for the SourcesController.

import pytest
from unittest.mock import MagicMock
from PySide6.QtCore import Qt
from src.controllers.sources_controller import SourcesController
from src.domain.entities import DataSource, AssociationType


@pytest.fixture
def sources_controller_setup(qapp, mock_i18n):
    app_state = MagicMock()
    view = MagicMock()

    controller = SourcesController(
        app_state=app_state,
        view=view,
        i18n=mock_i18n
    )
    controller.setup_connections()

    return {
        "controller": controller,
        "app_state": app_state,
        "view": view,
        "i18n": mock_i18n
    }


def test_setup_connections(sources_controller_setup):
    setup = sources_controller_setup
    view = setup["view"]
    app_state = setup["app_state"]

    view.source_selection_changed.connect.assert_called_once()
    view.source_delete_requested.connect.assert_called_once()
    view.source_modify_type_requested.connect.assert_called_once()
    app_state.data_sources_changed.connect.assert_called_once()
    app_state.data_association_changed.connect.assert_called_once()


def test_on_source_selected(sources_controller_setup):
    setup = sources_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]
    view = setup["view"]

    source = DataSource(name="GPS Tracker", path="/data/gps", association_type=AssociationType.GLOBAL)
    app_state.get_data_source_by_id.return_value = source

    controller._on_source_selected("/data/gps")
    app_state.set_selected_data_source.assert_called_once_with("/data/gps")
    view.set_association_type.assert_called_once_with("GLOBAL")

    # When source not found, fallback to LOCAL
    app_state.get_data_source_by_id.return_value = None
    controller._on_source_selected("invalid_id")
    view.set_association_type.assert_called_with("LOCAL")


def test_on_source_delete(sources_controller_setup):
    setup = sources_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]

    controller._on_source_delete("/data/source_to_delete")
    app_state.delete_data_source.assert_called_once_with("/data/source_to_delete")


def test_on_source_modify_type(sources_controller_setup):
    setup = sources_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]

    controller._on_source_modify_type("/data/source_to_modify")
    app_state.toggle_source_association_type.assert_called_once_with("/data/source_to_modify")


def test_model_updates_view(sources_controller_setup):
    setup = sources_controller_setup
    controller = setup["controller"]
    view = setup["view"]

    sources = [DataSource(name="S1", path="/s1")]
    controller._on_model_sources_updated(sources)
    view.update_sources_list.assert_called_once_with(sources)

    # Association updated matching current item in view
    mock_item = MagicMock()
    mock_item.data.return_value = "/s1"
    view.sources_list_widget.currentItem.return_value = mock_item

    controller._on_model_association_updated("/s1", "GLOBAL")
    view.set_association_type.assert_called_with("GLOBAL")
